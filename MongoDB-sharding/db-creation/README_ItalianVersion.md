# MongoDB Sharding with Docker
L'idea è quella di creare uno sharded cluster in mongodb. In particolare dato il volume di dati trattato nel nostro caso vogliamo creare tre differenti zoned-based shard in cui caricare i dati. I componenti mongo sono:
- **Config Server** (3 replica set): mongocfg1,mongocfg12,mongocfg13
- 3 shards (ognuno è un replica set con 3 membri ):
  - **Shard1**: conterrà i dati dei mesi tra Gennaio ed Aprile. (mongoshard11,mongoshard12,mongoshard13) 
  - **Shard2**: conterrà i dati dei mesi tra Maggio ed Agosto. (mongoshard21,mongoshard22,mongoshard23)
  - **Shard3**: conterrà i dati dei mesi tra Settembre e Dicembre. (mongoshard31,mongoshard32,mongoshard33)
- 1 router (mongos): mongos1

## Creazione sharding
Per creare lo Sharded Cluster velocemente è sufficiente eseguire da questa cartella il comando shell:
```sh
docker-compose up -d
```
Dopo l'esecuzione di questo comando, tutti i nodi verranno avviati e costruiti in automatico. La prima esecuzione di questo comando richiederà maggior tempo in quanto sarà necessario costruire da zero tutti i nodi neccessari oltre che avviarli.

### Test architettura 
Una volta avviati tutti i componenti dello Sharded Cluster per verificare che sia tutto funzionane sarà necessario eseguire alcuni comandi comandi shell:
```sh
> docker exec -it mongos1 /bin/bash
> mongo
mongos> sh.status()
```
I primi due comandi permettono di entrare nella shell di mongo, mentre l'ultimo comando stampa nella shell lo stato della configurazione degli shard. 
Se tutto ha funzionato correttamente dovrebbe essere visualizzato un output simile a video:
```sh
--- Sharding Status ---
  sharding version: {
        "_id" : 1,
        "minCompatibleVersion" : 5,
        "currentVersion" : 6,
        "clusterId" : ObjectId("604b767e7835ca21907fe7be")
  }
  shards:
        {  "_id" : "shard1",  "host" : "shard1/mongoshard11:27017,mongoshard12:27017,mongoshard13:27017",  "state" : 1,}
        {  "_id" : "shard2",  "host" : "shard2/mongoshard21:27017,mongoshard22:27017,mongoshard23:27017",  "state" : 1}
        {  "_id" : "shard3",  "host" : "shard3/mongoshard31:27017,mongoshard32:27017,mongoshard33:27017",  "state" : 1 }
  active mongoses:
        "4.4.4" : 1
  autosplit:
        Currently enabled: yes
  balancer:
        Currently enabled:  yes
        Currently running:  no
        Failed balancer rounds in last 5 attempts:  0
        Migration Results for the last 24 hours:
                No recent migrations
  ... other information ...
```

Una volta configurato il database sarà possibile accedervi alla porta 27027.
Altre informazioni più complete sulla costruzione dello sharding è possibile trovarle [qui](https://github.com/kayne87/mongodb-sharding-docker)

## Creazione database e sharding zone
Per creare un nuovo database sarà sufficiente, dalla shell mongo precedentemente aperta, digitare i seguenti comandi:
```sh
mongos> use BTS
mongos> sh.enableSharding("BTS")
mongos> sh.shardCollection("BTS.flight", {month:1})
```
In questo modo verrà creato un nuovo database di nome **BTS** al cui interno è presente la collezione **flight** il cui indice sarà basato sul campo month.
Una volta creata la collezione è già possibile utilizzare il database utilizzando le classiche operazione [CRUD](https://docs.mongodb.com/manual/crud/) di MongoDB.
Nel nostro caso abbiamo però creato anche delle zone prefissate per il caricamento dei dati in modo da sapere con esattezza quali dati venissero caricati in ogni shard. Per farlo è necessario effettuare alcuni passaggi:
1. Disabilitare il bilanciamento automatico per impedire la migrazione dei blocchi nel cluster :
```sh
mongos> sh.disableBalancing("BTS.flight")
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
# non è obbligatorio ma è meglio controllare che il precedente comando sia andato a buon fine
mongos> sh.isBalancerRunning()
false
```
2. Aggiungere i tag agli shard. Una zona può essere associata ad un particolare shard  sotto forma di tag, utilizzando sh.addShardTag(), quindi verrà aggiunto un tag a ogni shard. 
```sh
mongos> sh.addShardTag("shard1", "month4")
mongos> sh.addShardTag("shard2", "month8")
mongos> sh.addShardTag("shard3", "month12")
# Possiamo vedere le zone assegnate sotto forma di tag come richiesto per ogni shard 
mongos> sh.status()
shards:
        {  "_id" : "shard1",  "host" : "shard1/mongoshard11:27017,mongoshard12:27017,mongoshard13:27017",  "state" : 1,  "tags" : [ "month4" ] }
        {  "_id" : "shard2",  "host" : "shard2/mongoshard21:27017,mongoshard22:27017,mongoshard23:27017",  "state" : 1,  "tags" : [ "month8" ] }
        {  "_id" : "shard3",  "host" : "shard3/mongoshard31:27017,mongoshard32:27017,mongoshard33:27017",  "state" : 1,  "tags" : [ "month12" ] }
```
3. Definire il range per ogni zona. Nel caso di MongoDB il limite superiore è esclusivo.
```sh
# Range 1-4 per il primo shard. (Mesi: Gennaio-Aprile)
mongos> sh.addTagRange("BTS.flight", {month:1}, {month:5}, "month4")
{ "ok" : 1 }
# Range 5-8 per il secondo shard. (Mesi: Maggio-Agosto)
mongos> sh.addTagRange("BTS.flight", {month:5}, {month:9}, "month8")
{ "ok" : 1 }
# Range 9-12 per il terzo shard. (Mesi: Settembre-Dicembre)
mongos> sh.addTagRange("BTS.flight", {month:9}, {month:13}, "month12")
{ "ok" : 1 }
```
4. Riabilitare il bilanciamento del database
```sh
mongos> sh.enableBalancing("BTS.flight")
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
mongos> sh.isBalancerRunning()
true
```
### Test sharding zone
Per verificare che le zone siano state create correttamente è sufficiente provare a caricare alcuni documenti di test e controllare in quali shard vengono salvati. 
```sh
mongos> use BTS
# carico quattro documenti tutti nel primo shard
mongos> db.flight.insert({"year": 2021,"month": 1})
mongos> db.flight.insert({"year": 2021,"month": 2})
mongos> db.flight.insert({"year": 2021,"month": 3})
mongos> db.flight.insert({"year": 2021,"month": 4})
# carico un documento nel secondo shard
mongos> db.flight.insert({"year": 2021,"month": 5})
# carico un documento nel terzo shard
mongos> db.flight.insert({"year": 2021,"month": 12})
```
Per controllare la distribuzione dei documenti basta eseguire il comando:
```sh
mongos> db.flight.getShardDistribution()
```
che riporta a video la distribuzione dei vari shard e altri dettagli utili.
Se il test è andato a buon fine è possibile eliminare tutti i documenti di prova:
```sh
mongos> db.flight.remove({})
```

## Altri comandi utili
```sh
# Per stoppare e cancellare tutti i container docker avviati:
docker-compose rm -sv #Da eseguire nella cartella iniziale in cui sono stati avviati!

# Per visualizzare i logs di un particolare container, in questo caso mongos1
docker logs mongos1

# per eliminare un particolare database. Da eseguire all'interno della shell mongo.
mongos> use NomeDatabase
mongos> db.dropDatabase()
```

# MongoDB Sharding with Docker
>The italian version of this file can be found [here](./README_ItalianVersion.md)

The idea is to create a sharded cluster in mongodb. In particular, given the volume of data processed in our case (>4GB), we want to create three different zoned-based shards in which loads  the data. The Mongo Components will be:
- **Config Server** (3 member replica set): mongocfg1,mongocfg12,mongocfg13
- 3 shards (each a 3 member replica set):
  - **Shard1**: it will contain the data for the months between January and April. (mongoshard11,mongoshard12,mongoshard13) 
  - **Shard2**: it will contain the data for the months between May and August. (mongoshard21,mongoshard22,mongoshard23)
  - **Shard3**: it will contain the data for the months between September and December. (mongoshard31,mongoshard32,mongoshard33)
- 1 routers (mongos): mongos1

## Sharding creation
To create the Sharded Cluster quickly you can execute the shell command from the root of this folder: 
```sh
docker-compose up -d
```
After executing this command, all nodes will be started and built automatically. The first execution of this command will take more time as it will be necessary to build all the necessary nodes from scratch as well as start them. 

### Architecture test
Once all the components of the Sharded Cluster have been started, to verify that everything is working, you will need to execute some shell commands: 
```sh
> docker exec -it mongos1 /bin/bash
> mongo
mongos> sh.status()
```
The first two commands allow you to enter the mongo shell, while the last command prints the status of the shard configuration in the shell.
If everything worked fine you should see an output like this: 
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

Once the database has been configured, it will be accessible on port 27027.
More complete information on the construction of the sharding can be found [here](https://github.com/kayne87/mongodb-sharding-docker)

## Database creation and sharding zones 
To create a new database it will be sufficient, from the previously opened mongo shell, to type the following commands: 
```sh
mongos> use BTS
mongos> sh.enableSharding("BTS")
mongos> sh.shardCollection("BTS.flight", {month:1})
```
This will create a new database named **BTS** containing the **flight** collection whose index will be based on the month field.
Once the collection has been created, it is already possible to use the database using the classic MongoDB [CRUD](https://docs.mongodb.com/manual/crud/) operation.
In our case, however, we have also created preset zones for loading data in order to know exactly which data was loaded into each shard. To do this, you need to perform a few steps:

1. Disable automatic balancing to prevent block migration in the cluster: 
```sh
mongos> sh.disableBalancing("BTS.flight")
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
# It is not mandatory but it is better to check that the previous command was successful 
mongos> sh.isBalancerRunning()
false
```
2. Add tags to shards. A zone can be associated with a particular shard in the form of a tag, using sh.addShardTag(), then a tag will be added to each shard. 
```sh
mongos> sh.addShardTag("shard1", "month4")
mongos> sh.addShardTag("shard2", "month8")
mongos> sh.addShardTag("shard3", "month12")
# We can check associated zones in the form of tags as required for each shard
mongos> sh.status()
shards:
        {  "_id" : "shard1",  "host" : "shard1/mongoshard11:27017,mongoshard12:27017,mongoshard13:27017",  "state" : 1,  "tags" : [ "month4" ] }
        {  "_id" : "shard2",  "host" : "shard2/mongoshard21:27017,mongoshard22:27017,mongoshard23:27017",  "state" : 1,  "tags" : [ "month8" ] }
        {  "_id" : "shard3",  "host" : "shard3/mongoshard31:27017,mongoshard32:27017,mongoshard33:27017",  "state" : 1,  "tags" : [ "month12" ] }
```
3. Define the range for each zone. In the case of MongoDB the upper limit is exclusive. 
```sh
# Range 1-4 for the first shard. (Month: January-April)
mongos> sh.addTagRange("BTS.flight", {month:1}, {month:5}, "month4")
{ "ok" : 1 }
# Range 5-8 for the second shard. (Months: May-August)
mongos> sh.addTagRange("BTS.flight", {month:5}, {month:9}, "month8")
{ "ok" : 1 }
# Range 9-12 for the third shard. (Months: September-December) 
mongos> sh.addTagRange("BTS.flight", {month:9}, {month:13}, "month12")
{ "ok" : 1 }
```
4. Re-enable database balancing 
```sh
mongos> sh.enableBalancing("BTS.flight")
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
mongos> sh.isBalancerRunning()
true
```
### Test sharding zone
To verify that the zones have been created correctly, just try to load some test documents and check in which shards they are saved. 
```sh
mongos> use BTS
# Upload four documents in the first shard
mongos> db.flight.insert({"year": 2021,"month": 1})
mongos> db.flight.insert({"year": 2021,"month": 2})
mongos> db.flight.insert({"year": 2021,"month": 3})
mongos> db.flight.insert({"year": 2021,"month": 4})
# Upload a document in the second shard
mongos> db.flight.insert({"year": 2021,"month": 5})
# Upload a document in the third shard
mongos> db.flight.insert({"year": 2021,"month": 12})
```
To check the documents distribution just run the command which shows a video of the distribution of the various shards and other useful details.: 
```sh
mongos> db.flight.getShardDistribution()
```
If the test was successful, you can delete all the test documents: 
```sh
mongos> db.flight.remove({})
```

## Altri comandi utili
```sh
# To stop and delete all started docker containers 
docker-compose rm -sv #Da eseguire nella cartella iniziale in cui sono stati avviati!

# To shows logs for a specific container, in this case mongos1
docker logs mongos1

# To delete a specific database, to be run inside the mongo shell. 
mongos> use NomeDatabase
mongos> db.dropDatabase()
```

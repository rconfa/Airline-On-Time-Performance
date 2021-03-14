# Testing MongoDB sharding:
Nel [file excel](.//execution-time.xlsx) si possono vedere i risultati del caricamento dei dati su MongoDB con le relative percentuali e numero di documenti caricati in ogni shard passo passo.
\'E anche possibile verificare il tempo di esecuzione di quattro differenti query anch'esse eseguite passo passo durante il caricamento.

> Gli stessi risultati possono essere visti nel formato [pdf](.//execution-time.pdf)

# Query eseguite
Sono state eseguite quattro differenti tipologie di query per verificare il tempo di esecuzione durante il caricamento: 
- **Query1**: Restituisce il ritardo medio totale
- **Query2**: Restituisce il ritardo medio totale di una specifica compagnia aerea  (EV)
- **Query3**: Restituisce il ritardo medio totale di una specifica tratta area (SFO-LAX)
- **Query4**: Restituisce il ritardo medio totale di un'anno specifico  (2018)

Durante l'esecuzione abbiamo corretto leggermente la seconda query per filtrare precedentemente i documenti necessari ottenendo lo stesso risultato ma riducendo in modo significativo il tempo di esecuzione
come si può vedere dalla tabella di excel.
<br>
Dai risultati delle query si può notare che il tempo non cresce linearmente rispetto alla mole di dati che viene caricata nel database, lo sharding funziona quindi correttamente.

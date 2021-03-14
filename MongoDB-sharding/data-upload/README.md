# Testing time on MongoDB sharding:
In the [excel file](.//execution-time.xlsx) you can see the results of loading data on mongo with the relative percentages and documents loaded in each shard step by step.
It is also possible to view the execution time of four different queries also executed step by step. 

> You can see the same results in the pdf format [here](.//execution-time.pdf). Moreover you can see the italian version of this file [here](README_ItalianVersion.md)
# Type of query
We ran four different types of queries to check execution time as data was loaded:
- **Query1**: get the total average on arriving delays
- **Query2**: get the total average on arriving delays for a specific airline (EV)
- **Query3**: get the total average on arriving delays for a specific air route (SFO-LAX)
- **Query4**: get the total average on arriving delays for a specific year (2018)

During the execution we change a little bit the second query to previously filter the necessary documents  and we have achieved the same result by significantly reducing the execution time as you can see from excel's table.
<br>
From the results of the queries it can be seen that the execution time is not linear with respect to loading the data into the database, so the scharding works correctly! 

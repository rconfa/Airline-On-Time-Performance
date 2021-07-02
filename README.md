

<h1 align="center">Data Management and Visualization <br /> Airline on-time performance project </h1>

## Overview
Final project of "Data Management and Data Visualization" courses in which we tried to answer the following question:  "Is there a better time or airline to travel? Are there any differences between years?" <br />
To answer this question, we used flight data from US airlines in the years 2018-2019. These data are publicly available on the USA government [website](https://www.bts.gov/), for more information we have decided to integrate this data with other sources that would allow you to create more complete views. For example, the data on the altitude and on the full name of the airports were integrated using the unique code of the airport obtained from the BTS website. <br />
Once we obtained consistent files on a quantitative and qualitative level for the data, we concentrated on saving on mongoDb by implementing three different shards to divide the data thus managing the high amount of data (~5GB). <br />
In the end we concentrated on the data visualization part trying to create valid infographics to answer the initial questions and that they were.

## Software
The project was carried out with the use of Python for implementing the scripting used in Data Management part and Tableau as software for building visualizations about data.

## File
  * [Report](./Report/report.pdf): It describes all the steps and choices made in italian languages.
  * [Script](./script): Contains all python script implemented for this project.
  * [File](./CSV-File): Contains all files used in this project, either for data management part or data visualization part.
  * [Sharding](./MongoDB-sharding): Contains the docker compose used for building shard in MongoDB and a report of the execution time got for four different queries during the uploading. It also contains the description of the sharding strategy that we have used.
  * [Json](./Json-schema): Contains schema for json files and some sample files.

## About us

#### Riccardo Confalonieri - Data Science Student @ University of Milano-Bicocca
  * r.confalonieri5@campus.unimib.it
  * [GitHub](https://github.com/rconfa)

#### Rebecca picarelli - Data Science Student @ University of Milano-Bicocca
  * r.picarelli1@campus.unimib.it

#### Silvia Ranieri - Data Science Student @ University of Milano-Bicocca
  * s.ranieri7@campus.unimib.it

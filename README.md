# nba-stats
A Python based NBA data collection and data analysis project.

analysis:
  - This directory contains the python program to compute NBA ELO scores for each team each season. The ELO scores are stored in MongoDB in the games collection. 

crawling:
  - I collected NBA salary data and player yearly summary data from ESPN. These two programs can collect such data by year.

rapid-api-nba:
  - I used NBA dta from rapid api end points. These Python programs collect data from Rapid API endpoints and save data into MongoDB locally for later use. 

server:
  - This is a simple flask server serves NBA data to UI with Restful APIs. 
  - The data are stored in MongoDB and APIs return JSON formatted data.

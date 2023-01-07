# Spariky ETL Pipeline for Data Modeling with PostgreSQL

# Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

This project is an ETL (extract, transform, and load) pipeline for data modeling using Python and PostgreSQL. The goal of the project is to read data from multiple JSON files sources, transform the data into a suitable format for data modeling, and then load the data into a PostgreSQL database for further analysis and visualization.

The following libraries are used in this project:

* psycopg2 for connecting to and interacting with the PostgreSQL database
* pandas for reading and manipulating data

To use this project, you will need to have Python and PostgreSQL installed on your machine. You will also need to have access to the data sources and have the necessary credentials to connect to them.

To run the ETL pipeline, simply run the etl.py script. The script will extract the data from the sources, transform the data, and load it into the PostgreSQL database. You may need to modify the script to specify the correct credentials and file paths for your setup.

Once the data has been loaded into the PostgreSQL database, you can use SQL queries and other tools to analyze and visualize the data as needed.

# Data Sources

Now we will discuss about the JSON sources to accomplish the pipeline goal

## Song Dataset
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are file paths to two files in this dataset.

song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

## Log Dataset
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.

log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json




# Data Model

![Modelo](https://cdn.pixabay.com/photo/2017/03/18/01/07/willow-catkin-2152984_960_720.jpg](https://github.com/pspedro19/Spariky-Data-Modeling-ETL-Pipeline/blob/main/Images/Model.png)



# ETL Process



Extracting data from the sources

Cleaning and transforming the data
Loading the data into the PostgreSQL database
Running the Code
Include instructions for how to run the etl.py script and any dependencies that need to be installed. You may also want to include instructions for how to set up the PostgreSQL database and any necessary tables or schemas.

# Further Analysis



# Future Work


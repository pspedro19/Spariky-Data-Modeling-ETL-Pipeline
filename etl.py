import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):

    """This function process a song file and insert the song and artist data into our database. The function takes in two arguments:

        #cur: a cursor object for interacting with the database
        #filepath: a string representing the file path of the song file

    #This function reads in the song file using the pd.read_json() function
    #and stores the data in a Pandas DataFrame called df.
    # It then extracts the relevant data for the song and artist records from the DataFrame
    # and inserts them into the database using the cur.execute() function and the provided SQL insert statements song_table_insert and artist_table_insert."""


    # open song file
    df = pd.read_json(filepath, lines=True)


    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):

    """This function takes in two arguments:

            cur: a cursor object for interacting with the database
            filepath: a string representing the file path of the JSON folders file

        This function processes a log file containing user activity data and inserts data about the users,
        time, and songplays into the database. It reads in the log file, 
        filters the data to include only certain user actions, converts timestamps to datetime format,
        and creates and inserts records for the time, users, and songplays. It also queries the song and artist tables to obtain data about the songs that were played."""

    # open log file
    df =  pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = [df.ts.values, t.dt.hour.values, t.dt.day.values, t.dt.isocalendar().week, t.dt.month.values, t.dt.year.values, t.dt.weekday.values]
    column_labels =  ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))
    time_df['start_time'] = pd.to_datetime(time_df['start_time'], unit='ms')

    #this for funciton quey all rows to insert it in the time table
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # convert dataframe timestamp column to datetime
    df["ts"] = pd.to_datetime(df["ts"], unit='ms')
    
    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]

        cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
    """
    cur: a cursor object for interacting with the database
    conn: a connection object for the database
    filepath: a string representing the file path of the directory containing the data files
    func: a function that processes a single data file and inserts the data into the database


    This function first retrieves a list of all the files in the specified directory with the .json file extensio
    using os.walk() and glob.glob(). It then prints out the total number of files found.

    Next, it iterates over the list of files and passes each file to the func function for processing.
     It also commits the changes to the database after each file is processed and prints out the number of files
      that have been processed out of the total number of files.
    """


    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():


    """
    The main function processes data stored in JSON files in the song_data
    and log_data directories and loads the data into a PostgreSQL database
    using the psycopg2 library and the process_song_file and process_log_file functions.
    The process_song_file function reads in a JSON file containing song data, 
    extracts data about songs and artists, and inserts the data into the database.
   
    The process_log_file function reads in a JSON file containing log data, 
    filters the data, converts timestamps to datetime format, and creates and inserts records for the time,
    users, and songplays into the database. It also queries the song and artist tables to obtain data about
    the songs that were played and inserts records for songplays into the database.
    """


    conn = psycopg2.connect("host=localhost dbname=sparkifydb user=postgres password=password")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
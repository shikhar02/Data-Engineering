import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
    """
        Discription: This function will read song file data which is in json format,
        select the relevant features for dimension tables
        'songs' and 'artists', transform data into a list
        and insert the list into the database.
       
        Arguments:
        cur: the cursor object. 
        filepath: song data file path. 

        Returns:
            None
    """
    
    # open song file
    df = pd.read_json(filepath,lines=True)

    # insert song record
    song_data = list(df[['song_id','title','artist_id','year','duration']].values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    
    """
        Discription: This function will read log file data which is in json format,
        select the relevant features for dimension tables
        'users', 'time_table_create', and 'songplays', transform the data into a list
        and insert the list into the database.

        Arguments:
        cur: the cursor object. 
        filepath: log data file path. 

        Returns:
            None
    """
    
    # open log file
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'],unit='ms')
    
    # insert time data records
    #time_data= 
    #column_labels= 
    time_df = pd.DataFrame(data={'start_time':t,'hour':t.dt.hour,'day':t.dt.day,
                             'week':t.dt.week,'month':t.dt.month,'year':t.dt.year,
                            'weekday':t.dt.weekday})

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

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
        songplay_data=(pd.to_datetime(row.ts,unit='ms'),row.userId,row.level,
        songid,artistid,row.sessionId,row.location,row.userAgent)      
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    
    """ 
        Description: This function will act as a connector to the above functions
        'process_song_file' and 'process_log_file' by passing in arguments like filepath, cursor
        using another argument func.
    
        Arguments:
        cur: The cursor object
        conn: Connection to the database
        filepath: Location of the file containing data in json format in the song file data and log file data.
        func: This will pass arguments for above two functions 'process_song_file' and 'process_log_file'.


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
        Discription: This function will connect to the database, and assign a cursor to execute the queries.
        Also, arguments will be pass in function process_data.

    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
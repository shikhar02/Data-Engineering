# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays
                        (songplay_id SERIAL PRIMARY KEY,
                        start_time TIMESTAMP,
                        user_id int NOT NULL,
                        level varchar,
                        song_id varchar,
                        artist_id varchar(50),
                        session_id int,
                        location varchar(50),
                        user_agent varchar(500));
                        """)

user_table_create = ("""CREATE TABLE IF NOT EXISTS users
                    (user_id INT PRIMARY KEY not null,
                    first_name varchar(50) not null,
                    last_name varchar(50) not null,
                    gender varchar not null,
                    level varchar not null);""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs
                    (song_id varchar(50) PRIMARY KEY not null,
                    title varchar(100) not null,
                    artist_id varchar(50) not null,
                    year int not null,
                    duration float not null);
                    """)

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists
                      (artist_id varchar(500) PRIMARY KEY not null,
                      artist_name varchar(500) not null,
                      artist_location varchar(500),
                      artist_latitude float,
                      artist_longitude float);
                      """)

time_table_create = ("""CREATE TABLE IF NOT EXISTS time
                    (start_time TIMESTAMP PRIMARY KEY,
                    hour INT NOT NULL,
                    day INT NOT NULL,
                    week INT NOT NULL,
                    month INT NOT NULL,
                    year INT NOT NULL,
                    weekday INT NOT NULL);
                    """)

# INSERT RECORDS

#Fact Table
songplay_table_insert = ("""INSERT INTO songplays
                        (start_time,user_id,level,song_id,artist_id,
                        session_id,location,user_agent)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                        """)

#Dimension Tables
user_table_insert = ("""INSERT INTO users
                    (user_id, first_name, last_name, gender, level)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE
                    SET level=EXCLUDED.level
                    """)

song_table_insert = ("""INSERT INTO songs
                    (song_id, title, artist_id, year, duration)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (song_id) DO NOTHING
                    """)

artist_table_insert = ("""INSERT INTO artists
                      (artist_id, artist_name, artist_location, artist_latitude, artist_longitude)
                      VALUES (%s, %s, %s, %s, %s)
                      ON CONFLICT DO NOTHING
                      """)


time_table_insert = ("""INSERT INTO time
                    (start_time, hour, day, week, month, year, weekday)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (start_time)
                    DO NOTHING
                    """)

# FIND SONGS
song_select = ("""SELECT songs.song_id, artists.artist_id FROM songs
                JOIN artists ON songs.artist_id=artists.artist_id
                WHERE songs.title = %s
                AND artists.artist_name = %s
                AND songs.duration = %s;
                """)

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
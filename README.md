SUMMARY
===============

In this project, my main objective was to do data modeling with Postgres and build an ETL pipeline in order to help a startup ***'Sparkify'*** to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. I made a Postgres database tables designed to optimize queries on song play analysis. The main goal of the startup Sparkify's analytics team was to understand what songs users were listening to.


Designing database schema and creating an ETL pipeline.
===============

Database schema was designed in such a way that the analysis as well as data retrieval part become easy for the analytics team of sparkify. My database schema design consisted of two types of tables 'Dimension Table' and 'Fact Table'. With the help of the queries given by the Sparkify, I made 4 dimension tables and 1 fact table. Dimension Tables were 'songs' table, 'artists' table, 'users' table, and 'time_table_insert' table. Fact table was 'songplays'.

***Steps gone into creating an ETL pipeline were:***

- Established a connection to our database.

- Processed 'song' data and extracted desired features for dimension tables 'songs' and 'artists' and transformed the data into a list which was than inserted into our database tables 'songs' and 'artists'.

- Processed 'log' data and again extracted the desired features for 2 dimension tables ('time_table_insert','users') and one fact table ('songplays'). Moreover, converted the data into a list and inserted it into the database. Removed one quality issue from 'ts' column in 'time_table_insert' table by converting the datatype from integer to datetime. Also, used panda's [`dt` attribute](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.html) to extract timestamp, hour, day, week of year, month, year, and weekday from 'ts' feature for our 'time' table.

- For fact table 'songplays', I tried to join 'log' data with 'song' data on common song_id and artist_id by comparing the duration, artist name and title in 'song' data with 'log' data but since our data is only a subset of a very large dataset, I got only one row with song_id and artist_id as not null. Rest of the rows had null values for both 'song_id' and 'artist_id'.


Forming and Running Python Scripts
===============

In order to test the insertion of data in database after running each query, I used terminal to run python scripts (.py) using the command 'python create_tables.py'.

I made three python script files (.py):

- **sql_queries.py**- This python script consisted of all the SQL queries like dropping the tables, creating the tables, inserting data and selecting the data.

- **create_tables.py**- The main purpose of this python script was to create a database and run the queries in 'sql_queries.py' python script.

- **etl.py**- This python script file was used to performed ETL operation on 'song' data and 'log' data and store the obtained data in our database.


Example Queries
===============

1- songplay_table_create = ***('CREATE TABLE IF NOT EXISTS songplays (songplay_id serial PRIMARY KEY, start_time TIMESTAMP,  user_id int, level varchar, song_id varchar,  artist_id varchar(50), session_id int, location varchar(50), user_agent varchar(500));')***

2- user_table_insert = ***('INSERT INTO users(user_id, first_name, last_name, gender, level)
                    VALUES (%s, %s, %s, %s, %s) \
                    ON CONFLICT (user_id) DO UPDATE \
                    SET level=EXCLUDED.level')***

3- song_select = ***('SELECT songs.song_id, artists.artist_id FROM songs \
                JOIN artists ON songs.artist_id=artists.artist_id \
                WHERE songs.title = %s \
                      AND artists.artist_name = %s \
                      AND songs.duration = %s;')***

import csv
import sqlite3
import pandas as pd

csv_file = 'scrobbles-SndBxs.csv'
db_file = 'project.db'


conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Load csv data
def load_csv(csv_file, db_file):
    with open(csv_file, 'r', encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        cursor.execute( '''
        CREATE TABLE IF NOT EXISTS userInformation (
            artist_name TEXT NOT NULL,
            times_played INTEGER NOT NULL DEFAULT 0,
            most_listened_albums TEXT,
            most_listened_days TEXT,
            most_listened_songs TEXT,
            average_listen_duration REAL,
            total_listen_time INTEGER,
            skipped_tracks INTEGER DEFAULT 0
        );
        ''')

def get_top_artist(cursor):
    df = pd.read_csv(csv_file)
    df.to_sql('userInformation', conn, if_exists='replace', index=False)
    query = '''
    SELECT artist, COUNT(*) as times_played
    FROM userInformation
    GROUP BY artist
    ORDER BY times_played DESC
    LIMIT 1;
    '''
    cursor.execute(query)

    


load_csv(csv_file, db_file)
get_top_artist(cursor)

conn.commit()
conn.close()
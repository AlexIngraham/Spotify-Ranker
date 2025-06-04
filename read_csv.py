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
        cursor.execute('''
                      UPDATE userInformation
                      SET utc_time = substr(utc_time, 1, instr(utc_time, ',') -1)
                      WHERE instr(utc_time, ',') > 0;
                      ''')
        conn.commit()

def get_top_artist(cursor, limit = 10):
    query = '''
    SELECT artist, COUNT(*) as times_played
    FROM userInformation
    GROUP BY artist
    ORDER BY times_played DESC
    LIMIT ?;
    '''
    cursor.execute(query, (limit,))
    return cursor.fetchall()

def get_top_tracks(cursor, limit = 10):
    query = '''
    SELECT track, COUNT(*) as times_played
    FROM userInformation
    GROUP BY track
    ORDER BY times_played DESC
    LIMIT ?;
    '''
    cursor.execute(query, (limit,))
    return cursor.fetchall()

def get_top_albums(cursor, limit = 10):
    query = '''
    SELECT album, COUNT(*) as times_played
    FROM userInformation
    GROUP BY album
    ORDER BY times_played DESC
    LIMIT ?;
    '''
    cursor.execute(query, (limit,))
    return cursor.fetchall()

def most_played_days(cursor, limit = 10):
    query = '''
    SELECT utc_time, COUNT(*) as times_played
    FROM userInformation
    GROUP BY utc_time
    ORDER BY times_played DESC
    LIMIT ?;
    '''
    cursor.execute(query, (limit,))
    return cursor.fetchall()

load_csv(csv_file, db_file)
get_top_artist(cursor)
get_top_tracks(cursor)
get_top_albums(cursor)

print("Top Artists: :", get_top_artist(cursor))
print("\n")
print("Top Tracks: :", get_top_tracks(cursor))
print("\n")
print("Top Albums: :", get_top_albums(cursor))
print("\n")
print("Most Played Days: :", most_played_days(cursor))

conn.commit()
conn.close()
import sqlite3


try:
    con = sqlite3.connect('project.db')
    cursor = con.cursor()
    query = 'Select sqlite_version();'
    cursor.execute(query)
    result = cursor.fetchall()
    print('SQLite Version is {}'.format(result))
    cursor.close()
    print("SQLite connection opened successfully")
    # Create a table
    create_table_query = '''
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
    '''
    cursor.execute(create_table_query)
    con.commit()


except sqlite3.Error as error:
    print("Error: ", error)

finally:
    if con:
        con.close()
        print("SQLite connection closed")
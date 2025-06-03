import sqlite3

try:

    con = sqlite3.connect('project.db')
    cursor = con.cursor()
    query = 'Select sqlite_version();'
    cursor.execute(query)
    result = cursor.fetchall()
    print('SQLite Version is {}'.format(result))
    cursor.close()


except sqlite3.Error as error:
    print("Error: ", error)

finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("SQLite connection closed")
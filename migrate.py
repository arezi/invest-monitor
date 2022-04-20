





# ------


import sqlite3
import os


db_file = os.environ['INVEST_MONITOR_DB'] if 'INVEST_MONITOR_DB' in os.environ else 'demo.db'
#db_file = ':memory:'
#db_file = 'test.db'

if db_file == 'demo.db' and os.path.exists(db_file):
    os.remove(db_file)


conn = sqlite3.connect(db_file)

with conn:
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT MAX(version) FROM db_changelog")
        current_version = cursor.fetchone()[0]
        print("Current database version: "+current_version)
    except sqlite3.Error:
        print("New database")
        current_version = '000'


    updated = False

    for file in sorted(os.listdir('migrations')):
        if current_version >= file.split('.')[0]:
            continue

        if file == 'demo_data.sql' and not (db_file == 'demo.db' or db_file == ':memory:'):
            continue

        with open(os.path.join('migrations',file), 'rt') as f:
            sql = f.read()
        try:
            cursor.executescript(sql)
            print("Executed: "+file)
            updated = True
        except sqlite3.Error as exc:
            print("ERROR - %s: %s" % (file, str(exc)))
            quit()

# conn.close()


if updated:
    print("Database updated!" if current_version != '000' else 'Database %s created!'%db_file)
else:
    print('No changes applied.')


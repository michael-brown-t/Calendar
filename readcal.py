import os
import sqlite3

DBPATH = 'calendar.db'
conn = sqlite3.connect(DBPATH)

with conn:    
    cur = conn.cursor()    
    cur.execute("SELECT * FROM tbl_events")
    rows = cur.fetchall()
    for row in rows:
        print row
        print ("doing something")

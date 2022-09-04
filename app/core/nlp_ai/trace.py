import sqlite3
from sqlite3 import Error
from datetime import datetime 
import traceback

database = r"../../../database.db"

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def insert_log(conn, text, log):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = """ INSERT INTO logs (texte,trace) VALUES(?,?) """
    cur = conn.cursor()
    cur.executemany(sql, [(text, log)])
    conn.commit()
    return cur.lastrowid

def init_log_db():
    try:
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE logs (texte text, trace text)""")
        conn.commit()
        conn.close()
    except Exception as e:
    	print('>>>>>>>>>>>>>>>>>>>>')
    	print(e)

#def save_log(text, log):
    #create table if not exist
#    init_log_db()

    # create a database connection
#    conn = create_connection(database)

#    with conn:
#        log_id = insert_log(conn, text, log)
        
def save_log(text, log):
    with open('trace.log', 'a') as f:
        trace = {'date': str(datetime.now()), 'text': text, 'error': log, 'trace':traceback.format_exc()}
        f.write(str(trace))
        f.write('\n\n')
 
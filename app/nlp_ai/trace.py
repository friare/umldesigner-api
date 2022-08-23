import sqlite3
from sqlite3 import Error

database = r"../../database.db"

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

def insert_log(conn, log_data):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO logs (texte,trace) VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, log_data)
    conn.commit()
    return cur.lastrowid

def init_log_db():
    try:
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE logs (texte text, trace text)""")
        conn.commit()
        conn.close()
    except:
        pass

def save_log(text, log):
    #create table if not exist
    init_log_db()

    # create a database connection
    conn = create_connection(database)

    with conn:
        log_data = (text, log);
        log_id = insert_log(conn, log_data)
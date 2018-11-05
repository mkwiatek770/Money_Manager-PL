from psycopg2 import connect


def create_connection(username="postgres", password="coderslab"):
    '''This method creates connection with database'''
    cnx = connect(
        user=username,
        password=password,
        host="localhost",
        database="sync_db"
    )

    cursor = cnx.cursor()
    cnx.autocommit = True 

    return cnx, cursor

def close_connection(cursor, cnx):
    '''Closing connection with database'''
    cursor.close()
    cnx.close()

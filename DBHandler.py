import mysql
import mysql.connector
from mysql.connector import errorcode

DBNAME = 'linkedin'
DB_USERNAME = 'barak'
DB_PASSWORD = 'barak'
DB_HOST = '127.0.0.1'

config = {
    'user': DB_USERNAME,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'database': DBNAME,
    'raise_on_warnings': True
}


def connect_to_db():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        print('connected successfully')
        return cursor, cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def close_connection(cnx):
    cnx.close()

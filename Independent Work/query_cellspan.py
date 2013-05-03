from os import environ
from os import path
from MySQLdb import connect
from MySQLdb import cursors
import datetime
from operator import itemgetter
import pickle

# define constants 
global tower_count
global person_count
global number_count
tower_count = 32656
person_count = 97 # usually 97
number_count = 3764 # max phonenumber_oid
global sem_start1
global sem_end1
global sem_start2
global sem_end2
sem_start1 = datetime.datetime(2004, 8, 30, 0, 0, 0, 0)
sem_end1 = datetime.datetime(2004, 12, 17, 11, 59, 59, 0)
sem_start2 = datetime.datetime(2005, 2, 1, 0, 0, 0, 0)
sem_end2 = datetime.datetime(2005, 5, 20, 11, 59, 59, 0)


def query_cellspan():
    
    # establish connection to database
    HOST = 'publicdb.cs.princeton.edu'
    PORT = 3306
    DATABASE = 'tzha'
    USER = 'tzha'
    PASSWORD = 'T1@nT1@n'
    
    host = HOST
    if 'DB_SERVER_HOST' in environ:
        host = environ['DB_SERVER_HOST']
    connection = connect(host = host, port = PORT, user = USER, passwd = PASSWORD,
                         db = DATABASE)
    global cursor
    cursor = connection.cursor(cursors.DictCursor)

    for i in range(1, person_count + 1):
        # open file
        filename = "cellspan{0}-1".format(i)
        file = open(filename, 'w+')

        # make query
        query = ('select * from cellspan where person_oid = ' + str(i)
                + ' and starttime > "' + str(sem_start1)
                + '" and starttime < "' + str(sem_end1) + '"')
        cursor.execute(query)

        # write to file
        line = cursor.fetchone()
        while (line):
            pickle.dump(line, file)
            line = cursor.fetchone()

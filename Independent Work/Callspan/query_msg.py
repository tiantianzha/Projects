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


def query_callspan():
    
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
        filename = "call{0}-1".format(i)
        file = open(filename, 'w+')

        # make query
        query = ('select * from callspan where person_oid = ' + str(i)
                + ' and starttime > "' + str(sem_start1)
                + '" and starttime < "' + str(sem_end1) + '"')
        cursor.execute(query)

        # write to file
        line = cursor.fetchone()
        while (line):
            pickle.dump(line, file)
            line = cursor.fetchone()

def read_callspan():
    global log_msg
    log_msg = [dict() for i in range(person_count + 1)]
    global exists1
    exists1 = [0] * (person_count + 1)
    global sum_msg1
    sum_msg1 = [0] * (person_count + 1)
    
    for i in range(1, person_count + 1):
        filename = 'call{0}-1.txt'.format(i)
        if path.exists(filename):
            file = open(filename, 'r')
        else:
            continue
    
        # mark this person as existing

        while(1):
            try:
                line = pickle.load(file)
            except EOFError:
                break
            # add to voice call duration OR to message count
            if line['description'] == "Short Message":
                exists1[i] = 1
                log_msg[i][line['phonenumber_oid']] = log_msg[i].get(line['phonenumber_oid'], 0) + 1
        # display times as a percentage of total time
        sum_msg1[i] = sum(log_msg[i].itervalues())
        for k, v in log_msg[i].iteritems():
            log_msg[i][k] = float(log_msg[i][k]) / sum_msg1[i]

    print "messages1"
    print sum_msg1

def compute_hamming(a, b):
    sum = 0
    for i in range(1, number_count + 1):
        sum += abs(a.get(i, 0) - b.get(i, 0))
    return sum
    

def read_anon():
    global anon_msg
    global hamming_msg
    global min_index
    global sum_msg2
    global exists2
    anon_msg = [dict() for i in range(person_count + 1)]
    hamming_msg = [dict() for i in range(person_count + 1)]
    min_index = [-1] * (person_count + 1)
    sum_msg2 = [0] * (person_count + 1)
    exists2 = [0] * (person_count + 1)
    
        
    for i in range(1, person_count + 1):
        # if person i didn't exist, continue
        if exists1[i] == 0:
            continue
        
        # open file if exists
        filename = 'call{0}-2.txt'.format(i)
        if path.exists(filename):
            file = open(filename, 'r')
        else:
            continue
    
        # store information
        while(1):
            # read line from file & store
            try:
                line = pickle.load(file)
            except EOFError:
                break
            if line['description'] == "Short Message":
                anon_msg[i][line['phonenumber_oid']] = anon_msg[i].get(line['phonenumber_oid'], 0) + 1
                exists2[i] = 1
        # sum over all values->get percentages
        sum_msg2[i] = sum(anon_msg[i].itervalues())
        for k, v in anon_msg[i].iteritems():
            anon_msg[i][k] = float(anon_msg[i][k]) / sum_msg2[i]


        # find min difference
        min_diff = float("inf")
        for j in range(1, person_count + 1):
            # compute hamming score if person exists
            if exists1[j]:
                hamming_msg[i][j] = compute_hamming(anon_msg[i], log_msg[j])
            else:
                hamming_msg[i][j] = float("inf")
            # update min if necessary
            if hamming_msg[i][j] < min_diff:
                min_diff = hamming_msg[i][j]
                min_index[i] = j

    print "messages2"
    print sum_msg2

def output_results():
    valid = list()
    # count the number of total items
    count = 0
    avg_msg1 = 0
    avg_msg2 = 0
    for i in range(1, person_count + 1):
        if exists2[i] == 1 and exists1[i] == 1:
            count += 1
            avg_msg1 += sum_msg1[i]
            avg_msg2 += sum_msg2[i]
            valid.append(i)
    print "TOTAL ANON: {0}".format(count)
    # average call time across all users
    avg_msg1 = float(avg_msg1) / count
    avg_msg2 = float(avg_msg2) / count

    # count the number of correct items
    avg_msg_correct1 = 0
    avg_msg_correct2 = 0
    avg_msg_wrong1 = 0
    avg_msg_wrong2 = 0

    correct_count = 0
    for i in valid:
        if i == min_index[i]:
            correct_count += 1
            avg_msg_correct1 += sum_msg1[i]
            avg_msg_correct2 += sum_msg2[i]
        else:
            avg_msg_wrong1 += sum_msg1[i]
            avg_msg_wrong2 += sum_msg2[i]
    avg_msg_correct1 = float(avg_msg_correct1) / correct_count
    avg_msg_correct2 = float(avg_msg_correct2) / correct_count
    avg_msg_wrong1 = float(avg_msg_wrong1) / (count - correct_count)
    avg_msg_wrong2 = float(avg_msg_wrong2) / (count - correct_count)

    print "TOTAL CORRECT: {0}".format(correct_count)
    print ""

    # correct items: average call time 2nd sem; average call time 1st sem
    # wrong items: average call time 2nd sem; average call time 1st sem
    print "All items: average msg 2nd sem {0}\n           average msg 1st sem {1}".format(avg_msg2, avg_msg1)
    print "Correct items: average msg 2nd sem {0}\n               average msg 1st sem {1}".format(avg_msg_correct2, avg_msg_correct1)
    print "Wrong items: average msg 2nd sem {0}\n             average msg 1st sem {1}".format(avg_msg_wrong2, avg_msg_wrong1)
    print ""
    # then go into detail about each
    # using for loop:
    for i in valid:
        
        print "Anon ({0}) is most similar to Person {1}".format(i, min_index[i])
        sorted_hamming_msg = sorted(hamming_msg[i].iteritems(), key=itemgetter(1))
        
        # if i != j:
        if i != min_index[i]:
            print "WRONG"
            # print index that i occurs at
            for j in range(len(sorted_hamming_msg)):
                if sorted_hamming_msg[j][0] == i:
                    print "Actual Anon ({0}) occurs at position {1}".format(i, j)
                    break
            # print 2nd sem call time; 1st sem correct id call time, 1st sem wrong id call time
            print "2nd sem msg: {0}".format(sum_msg2[i])
            print "1st sem returned value msg: {0}".format(sum_msg1[min_index[i]])
            print "1st sem actual value msg: {0}".format(sum_msg1[i])
        else:
            print "CORRECT"
            # print 2nd sem call time; 1st sem call time
            print "2nd sem msg: {0}".format(sum_msg2[i])
            print "1st sem msg: {0}".format(sum_msg1[i])

        # print sorted list of hamming values
        for tup in sorted_hamming_msg:
            print "{0}: {1}".format(tup[0], tup[1])

# start calling functions
read_callspan()
read_anon()
output_results()

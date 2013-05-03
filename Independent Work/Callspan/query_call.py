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


global convert # THIS is is an ID from 1 to 106, for phone data
convert = [0] * (person_count + 1)
#convert[7] = 2
convert[6] = 3
convert[29] = 4
convert[83] = 5
convert[85] = 6
convert[59] = 7
convert[86] = 8
convert[95] = 9
convert[94] = 10
convert[78] = 12
convert[90] = 13
convert[15] = 15
convert[14] = 16
convert[88] = 17
convert[8] = 18
convert[81] = 19
convert[71] = 20
convert[7] = 21
convert[97] = 22
convert[57] = 23
convert[5] = 24
convert[96] = 25
convert[89] = 26
convert[80] = 27
convert[69] = 28
convert[2] = 29
convert[18] = 30
convert[3] = 32
convert[58] = 33
convert[27] = 34
convert[91] = 35
convert[63] = 36
convert[10] = 37
convert[68] = 38
convert[70] = 40
convert[33] = 41
convert[66] = 42
convert[53] = 43
convert[92] = 46
convert[22] = 49
convert[49] = 50
convert[42] = 51
convert[38] = 52 # and 57
convert[65] = 53
convert[36] = 54
convert[4] = 55
convert[19] = 56
convert[39] = 60 # but also 11
convert[51] = 58
convert[23] = 61 #62 has no corresponding.. all contradict
convert[26] = 63
convert[93] = 65
convert[64] = 66
convert[60] = 67
convert[30] = 68
convert[73] = 70 #72 has no match
convert[20] = 74
convert[74] = 75
convert[79] = 76
convert[84] = 77
convert[24] = 78
convert[61] = 79
convert[72] = 81
convert[76] = 82
convert[82] = 83 # not sure only 1 entry
convert[45] = 84
convert[50] = 86
convert[13] = 87
convert[11] = 88
convert[77] = 89
convert[47] = 90
convert[54] = 91
convert[87] = 92
convert[46] = 93
convert[37] = 94 # 37 could be 16
convert[56] = 95
convert[34] = 96
convert[12] = 97
convert[40] = 98 #nothing matches 99
convert[75] = 100
convert[43] = 101
convert[16] = 102 # 16 could be 37
convert[21] = 103 # not sure only 1 entry; could be 21 instead of 82
convert[62] = 104

global network # THIS represents converstion from phone data to network data
network = [0] * 108
network[3] = 1
network[4] = 2
network[5] = 3
network[6] = 4
network[7] = 5
network[8] = 6
network[9] = 7
network[10] = 8
network[11] = 9
network[12] = 10
network[13] = 11
network[14] = 12
network[15] = 13
network[16] = 14
network[17] = 15
network[19] = 16
network[20] = 17
network[21] = 18
network[22] = 19
network[23] = 20
network[25] = 21
network[26] = 22
network[27] = 23
network[28] = 24
network[29] = 25
network[30] = 26
network[31] = 27
network[32] = 28
network[33] = 29
network[35] = 30
network[36] = 31
network[37] = 32
network[38] = 33
network[40] = 34
network[41] = 35
network[42] = 36
network[43] = 37
network[44] = 38
network[46] = 39
network[48] = 40
network[49] = 41
network[50] = 42
network[52] = 43
network[53] = 44
network[54] = 45
network[55] = 46
network[56] = 47
network[57] = 48
network[58] = 49
network[60] = 50
network[61] = 51
network[62] = 52
network[63] = 53
network[65] = 54
network[66] = 55
network[67] = 56
network[68] = 57
network[69] = 58
network[70] = 59
network[71] = 60
network[72] = 61
network[73] = 62
network[74] = 63
network[75] = 64
network[76] = 65
network[77] = 66
network[78] = 67
network[79] = 68
network[80] = 69
network[81] = 70
network[82] = 71
network[83] = 72
network[84] = 73
network[86] = 74
network[87] = 75
network[88] = 76
network[89] = 77
network[90] = 78
network[01] = 79
network[92] = 80
network[93] = 81
network[94] = 82
network[95] = 83
network[96] = 84
network[97] = 85
network[98] = 86
network[99] = 87
network[100] = 88
network[101] = 89
network[102] = 90
network[103] = 91
network[104] = 92
network[106] = 93
network[107] = 94

# 0 = blank, 1 = ugrad, 2 = grad, 3 = sloan, 4 = staff
blank = 19
ugrad = 10
grad = 35
sloan = 27
staff = 6
global freq
#freq = [blank, ugrad, grad, sloan, staff]
freq = [1, 1, 1, 1, 1]
global pos
pos = ['None' for i in range(108)]
pos[1] = 0
pos[2] = 2
pos[3] = 1
pos[4] = 3
pos[5] = 2
pos[6] = 0 # stu
pos[7] = 0
pos[8] = 2
pos[9] = 1
pos[10] = 2
pos[11] = 2
pos[12] = 3
pos[13] = 4
pos[14] = 2
pos[15] = 2
pos[16] = 1
pos[17] = 2
pos[18] = 0 # stu
pos[19] = 3
pos[20] = 3
pos[21] = 2
pos[22] = 3
pos[23] = 3
pos[24] = 1
pos[25] = 3
pos[26] = 2
pos[27] = 1
pos[28] = 2
pos[29] = 0
pos[30] = 2
pos[31] = 3
pos[32] = 0
pos[33] = 4
pos[34] = 2
pos[35] = 3
pos[36] = 3
pos[37] = 2
pos[38] = 3
pos[39] = 0
pos[40] = 3
pos[41] = 4
pos[42] = 3
pos[43] = 2
pos[44] = 2
pos[45] = 3
pos[46] = 3
pos[47] = 2
pos[48] = 0
pos[49] = 2
pos[50] = 3
pos[51] = 2
pos[52] = 0
pos[53] = 2
pos[54] = 2
pos[55] = 1
pos[56] = 3
pos[57] = 0
pos[58] = 1
pos[59] = 0
pos[60] = 2
pos[61] = 1
pos[62] = 0
pos[63] = 2
pos[64] = 3
pos[65] = 2
pos[66] = 3
pos[67] = 3
pos[68] = 1
pos[69] = 2
pos[70] = 1
pos[71] = 2
pos[72] = 3
pos[73] = 3
pos[74] = 2
pos[75] = 2
pos[76] = 4
pos[77] = 3
pos[78] = 0
pos[79] = 3
pos[80] = 0
pos[81] = 2
pos[82] = 3
pos[83] = 0
pos[84] = 3
pos[85] = 2
pos[86] = 0
pos[87] = 0
pos[88] = 4
pos[89] = 2
pos[90] = 0
pos[91] = 2
pos[92] = 3
pos[93] = 2
pos[94] = 2
pos[95] = 4
pos[96] = 0
pos[97] = 2


def read_survey():
    global position
    position = ["None" for i in range(person_count + 1)]
    
    file = open('survey.txt', 'r')
    while(1):
        try:
            line = pickle.load(file)
        except EOFError:
            break
        position[line['oid']] = line['survey_Position']
    for i in range(person_count + 1):
        print str(i) + position[i]

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
    global log
    log = [dict() for i in range(person_count + 1)]
    global exists1
    exists1 = [0] * (person_count + 1)
    global sum_time1
    sum_time1 = [0] * (person_count + 1)
    global call_num1
    call_num1 = [0] * (person_count + 1)
    
    for i in range(1, person_count + 1):
        filename = 'call{0}-1.txt'.format(i)
        if path.exists(filename):
            file = open(filename, 'r')
            exists1[i] = 1
        else:
            continue

        # read line per line
        while(1):
            try:
                line = pickle.load(file)
            except EOFError:
                break
            # record duration if voice call
            if line['description'] == "Voice Call":
                log[i][line['phonenumber_oid']] = log[i].get(line['phonenumber_oid'], 0) + line['duration']
                call_num1[i] += 1
        # display times as a percentage of total time
        sum_time1[i] = sum(log[i].itervalues())
        for k, v in log[i].iteritems():
            log[i][k] = float(log[i][k]) / sum_time1[i]

def compute_hamming(a, b):
    sum = 0
    for i in range(1, number_count + 1):
        sum += abs(a.get(i, 0) - b.get(i, 0))
    return sum
    

def read_anon():
    global anon
    global hamming
    global min_index
    global sum_time2
    global exists2
    global call_num2
    anon = [dict() for i in range(person_count + 1)]
    hamming = [dict() for i in range(person_count + 1)]
    min_index = [-1] * (person_count + 1)
    sum_time2 = [0] * (person_count + 1)
    exists2 = [0] * (person_count + 1)
    call_num2 = [0] * (person_count + 1)
    
        
    for i in range(1, person_count + 1):
        # if person i didn't exist, continue
        if exists1[i] == 0:
            continue
        
        # open file if exists
        filename = 'call{0}-2.txt'.format(i)
        if path.exists(filename):
            file = open(filename, 'r')
            exists2[i] = 1
        else:
            continue
    
        # store information
        while(1):
            # read line from file & store
            try:
                line = pickle.load(file)
            except EOFError:
                break
            # record if voice call
            if line['description'] == "Voice Call":
                anon[i][line['phonenumber_oid']] = anon[i].get(line['phonenumber_oid'], 0) + line['duration']
                call_num2[i] += 1
        # sum over all values->get percentages
        sum_time2[i] = sum(anon[i].itervalues())
        for k, v in anon[i].iteritems():
            anon[i][k] = float(anon[i][k]) / sum_time2[i]

        # find min difference
        min_diff = float("inf")
        for j in range(1, person_count + 1):
            # compute hamming score if person exists
            if exists1[j]:
                hamming[i][j] = compute_hamming(anon[i], log[j])
            else:
                hamming[i][j] = float("inf")
            # update min if necessary
            if hamming[i][j] < min_diff:
                min_diff = hamming[i][j]
                min_index[i] = j

def output_results():
    valid = list()
    # count the number of total items
    count = 0
    avg_time1 = 0
    avg_time2 = 0
    avg_num1 = 0
    avg_num2 = 0
    for i in range(1, person_count + 1):
        if exists2[i] == 1 and exists1[i] == 1:
            count += 1
            avg_time1 += sum_time1[i]
            avg_time2 += sum_time2[i]
            avg_num1 += call_num1[i]
            avg_num2 += call_num2[i]
            valid.append(i)
    print "TOTAL ANON: {0}".format(count)
    # average call time across all users
    avg_time1 = float(avg_time1) / count
    avg_time2 = float(avg_time2) / count
    avg_num1 = float(avg_num1) / count
    avg_num2 = float(avg_num2) / count

    # count the number of correct items
    avg_time_correct1 = 0
    avg_time_correct2 = 0
    avg_time_wrong1 = 0
    avg_time_wrong2 = 0
    avg_num_correct1 = 0
    avg_num_correct2 = 0
    avg_num_wrong1 = 0
    avg_num_wrong2 = 0

    correct_count = 0
    for i in valid:
        if i == min_index[i]:
            correct_count += 1
            avg_time_correct1 += sum_time1[i]
            avg_time_correct2 += sum_time2[i]
            avg_num_correct1 += call_num1[i]
            avg_num_correct2 += call_num2[i]
        else:
            avg_time_wrong1 += sum_time1[i]
            avg_time_wrong2 += sum_time2[i]
            avg_num_wrong1 += call_num1[i]
            avg_num_wrong2 += call_num2[i]
    avg_time_correct1 = float(avg_time_correct1) / correct_count
    avg_time_correct2 = float(avg_time_correct2) / correct_count
    avg_time_wrong1 = float(avg_time_wrong1) / (count - correct_count)
    avg_time_wrong2 = float(avg_time_wrong2) / (count - correct_count)

    avg_num_correct1 = float(avg_num_correct1) / correct_count
    avg_num_correct2 = float(avg_num_correct2) / correct_count
    avg_num_wrong1 = float(avg_num_wrong1) / (count - correct_count)
    avg_num_wrong2 = float(avg_num_wrong2) / (count - correct_count)
    print "TOTAL CORRECT: {0}".format(correct_count)
    print ""

    # correct items: average call time 2nd sem; average call time 1st sem
    # wrong items: average call time 2nd sem; average call time 1st sem
    print "All items: average call time 2nd sem {0}\n           average call time 1st sem {1}".format(avg_time2, avg_time1)
    print "Correct items: average call time 2nd sem {0}\n               average call time 1st sem {1}".format(avg_time_correct2, avg_time_correct1)
    print "Wrong items: average call time 2nd sem {0}\n             average call time 1st sem {1}".format(avg_time_wrong2, avg_time_wrong1)
    print ""
    print "All items: average call num 2nd sem {0}\n           average call num 1st sem {1}".format(avg_num2, avg_num1)
    print "Correct items: average call num 2nd sem {0}\n               average call num 1st sem {1}".format(avg_num_correct2, avg_num_correct1)
    print "Wrong items: average call num 2nd sem {0}\n             average call num 1st sem {1}".format(avg_num_wrong2, avg_num_wrong1)

    avg_diff_correct = 0
    avg_diff_wrong = 0
    smallest_diff_correct = 2
    smallest_ind = 0
    largest_diff_wrong = 0
    largest_ind = 0

    # then go into detail about each
    # using for loop:
    for i in valid:
        
        print "Anon ({0}) is most similar to Person {1}".format(i, min_index[i])
        sorted_hamming = sorted(hamming[i].iteritems(), key=itemgetter(1))
        # if i != j:
        if i != min_index[i]:
            print "WRONG"
            # print index that i occurs at
            for j in range(len(sorted_hamming)):
                if sorted_hamming[j][0] == i:
                    print "Actual Anon ({0}) occurs at position {1}".format(i, j)
                    break
            # print 2nd sem call time; 1st sem correct id call time, 1st sem wrong id call time
            print "2nd sem call time: {0}".format(sum_time2[i])
            print "1st sem returned value call time: {0}".format(sum_time1[min_index[i]])
            print "1st sem actual value call time: {0}".format(sum_time1[i])
            print "2nd sem call num: {0}".format(call_num2[i])
            print "1st sem returned value call num: {0}".format(call_num1[min_index[i]])
            print "1st sem actual value call num: {0}".format(call_num1[i])
            diff = sorted_hamming[1][1] - sorted_hamming[0][1]
            avg_diff_wrong += diff
            if largest_diff_wrong < diff:
                largest_diff_wrong = diff
                largest_ind = i
        else:
            print "CORRECT"
            # print 2nd sem call time; 1st sem call time
            print "2nd sem call time: {0}".format(sum_time2[i])
            print "1st sem call time: {0}".format(sum_time1[i])
            print "2nd sem call num: {0}".format(call_num2[i])
            print "1st sem call num: {0}".format(call_num1[i])
            diff = sorted_hamming[1][1] - sorted_hamming[0][1]
            avg_diff_correct += diff
            if smallest_diff_correct > diff:
                smallest_diff_correct = diff
                smallest_ind = i

        print "Difference btw 1st guess and 2nd guess: {0}".format(sorted_hamming[1][1] - sorted_hamming[0][1])
        # print sorted list of hamming values
        for tup in sorted_hamming:
            print "{0}: {1}".format(tup[0], tup[1])

    avg_diff_correct = float(avg_diff_correct) / correct_count
    if correct_count == count:
        avg_diff_wrong = 0
    else:
        avg_diff_wrong = float(avg_diff_wrong) / (count - correct_count)
    print "Average diff btw 1st and 2nd guess when correct: {0}; when wrong: {1}".format(avg_diff_correct, avg_diff_wrong)
    print "Smallest diff when correct: {0}, at {1}".format(smallest_diff_correct, smallest_ind)
    print "Largest diff when wrong: {0}, at {1}".format(largest_diff_wrong, largest_ind)

def read_all():
    global log_call
    log_call = [dict() for i in range(person_count + 1)]
    global exists
    exists = [0] * (person_count + 1)
    global sum_time
    sum_time = [0] * (person_count + 1)
    global entry_count
    entry_count = [0] * (person_count + 1)
    
    for i in range(1, person_count + 1):
        # OPEN FILE 1
        filename = 'call{0}-1.txt'.format(i)
        if path.exists(filename):
            file = open(filename, 'r')
            print "Opening " + filename
            
            exists[i] = 1
            # iterate through each line of file
            while(1):
                try:
                    line = pickle.load(file)
                except EOFError:
                    break
            
                if line['description'] == "Voice Call":
                    duration = line['duration']
                    if duration < 0:
                        duration = 0
                    log_call[i][line['phonenumber_oid']] = log_call[i].get(line['phonenumber_oid'], 0) + float(duration)
                    entry_count[i] += 1
    
        # OPEN FILE 2
        filename = 'cellspan{0}-2.txt'.format(i)
        if path.exists(filename):
            file = open(filename, 'r')
            print "Opening " + filename
        
            exists[i] = 1
            # iterate through each line of file
            while(1):
                try:
                    line = pickle.load(file)
                except EOFError:
                    break
            
                if line['description'] == "Voice Call":
                    duration = line['duration']
                    if duration < 0:
                        duration = 0
                    log_call[i][line['phonenumber_oid']] = log_call[i].get(line['phonenumber_oid'], 0) + float(duration)
                    entry_count[i] += 1

        if exists[i] == 1:
            # obtain sum of all time
            sum_time[i] = sum(log_call[i].itervalues())
            for k, v in log_call[i].iteritems():
                if log_call[i][k] < 0:
                    print "OVERFLOW: {0}".format(log_call[i][k])
                log_call[i][k] = float(log_call[i][k]) / sum_time[i]

def compute_similarity():
    global rank
    rank = [dict() for i in range(person_count + 1)]
    
    for i in range(1, person_count + 1):
        if exists[i] == 0:
            continue
        for j in range(1, person_count + 1):
            if 1 == j:
                continue
            if exists[j] == 1:
                rank[i][j] = compute_hamming(log_call[i], log_call[j])
            else:
                rank[i][j] = float("inf")

def output_rank():
    for i in range(1, person_count + 1):
        ind = convert[i]
        if ind == 0:
            p = position[i]
        else:
            p = pos[ind]
        print "RANKED SIMILARITIES: {0} (converts to {1}, then to {2}) ".format(i, convert[i], network[convert[i]]) + p
        sorted_hamming = sorted(rank[i].iteritems(), key=itemgetter(1))
        for tup in sorted_hamming:
            if tup[0] != i:
                ind = convert[tup[0]]
                if ind == 0:
                    p = position[tup[0]]
                else:
                    p = pos[ind]
                print "{0} {1} {2} ({3}, {4}) ".format(i, tup[0], tup[1], convert[tup[0]], network[convert[tup[0]]]) + p

def create_profiles():
    global profile # list of dictionaries (distributions)
    profile = [dict() for i in range(5)]
    for i in range(1, 5): # i is profile index
        count = 0
        for j in range(1, person_count + 1): # j is user index
            if pos[j] != i: # if j is not the correct kind of user, skip
                continue
            dis_sum = sum(log_call[j].itervalues())
            if dis_sum == 0:
                continue
            count += 1
            print "sum for person {0} is {1}".format(j, dis_sum)
            for k, v in log_call[j].iteritems(): # k is tower number
                profile[i][k] = profile[i].get(k, 0) + v # v is % time spent there

        for k, v in profile[i].iteritems():
            profile[i][k] = float(v) / count
    
    print "printing profiles"
    for d in profile:
        print sum(d.itervalues())

    for i in range(1, 5):
        for j in range(i + 1, 5):
            score = compute_hamming(profile[i], profile[j])
            print "diff between {0} and {1} is {2}".format(i, j, score)

def compare_profiles():
    global rank
    rank = [dict() for i in range(person_count + 1)]
    
    for i in range(1, person_count + 1):
        if exists[i] == 0:
            continue
        for j in range(1, 5): # for each person iterate thru the profiles
            rank[i][j] = compute_hamming(log_call[i], profile[j]) / freq[j] # adjust for distrib


    

def print_results():
    correct_count = 0
    wrong_count = 0
    correct_diff = 0
    wrong_diff = 0
    for i in range(1, person_count + 1):
        print "RANKED SIMILARITIES: {0} (converts to {1}, then to {2}) position: {3}".format(i, convert[i], network[convert[i]], pos[i])
        if pos[i] == 0:
            continue
        sorted_hamming = sorted(rank[i].iteritems(), key=itemgetter(1))
        if len(sorted_hamming) == 0:
            continue
        if sorted_hamming[0][0] == pos[i]:
            print "CORRECT"
            correct_count += 1
            correct_diff += (sorted_hamming[1][1] - sorted_hamming[0][1])
        else:
            print "WRONG"
            wrong_count += 1
            wrong_diff += (sorted_hamming[1][1] - sorted_hamming[0][1])
        for tup in sorted_hamming:
            print "{0} {1} {2} ({3}, {4})".format(i, tup[0], tup[1], convert[tup[0]], network[convert[tup[0]]],)
    
    print "{0} CORRECT, {1} WRONG".format(correct_count, wrong_count)
    print "Correct diff: {0} Wrong diff: {1}".format(correct_diff / correct_count, wrong_diff / wrong_count)

# start calling functions
read_survey()

#read_callspan()
#read_anon()
#output_results()

read_all()
create_profiles()
compare_profiles()
print_results()

#compute_similarity()
#output_rank()


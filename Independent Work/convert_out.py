import string
from os import path
import datetime
import pickle
from operator import itemgetter
import random

global tower_count
global person_count
tower_count = 32656
person_count = 97 # TESTING

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





#hours
def timedelta_to_days(td):
    return (float(td.microseconds)/(1000*3600) + float(td.seconds)/(3600) + float(td.days)*24)

def read_out():
    global map # convert from each node to a cluster number
    map = [-1] * (tower_count + 1)
    global clusters # list of clusters
    clusters = list()

    i = 6 # this specifies which output file
    filename = "out_{0}.txt".format(i)
    f = open(filename, 'r')

    clusterno = 0
    line = f.readline()
    # iterate through each line
    while (line):
        new_cluster = list()
        nodes = string.split(line)
        # iterate through each node in line
        for num in nodes:
            num = int(num)
            new_cluster.append(num)
            if map[num] == -1:
                map[num] = clusterno
            else:
                print "ERROR"
        # update before next iteration
        clusters.append(new_cluster)
        clusterno += 1
        line = f.readline()

    for i in range(1, tower_count + 1):
        if map[i] == -1:
            map[i] = clusterno
            clusterno += 1
            new_cluster = list()
            new_cluster.append(i)
            clusters.append(new_cluster)

    print str(clusterno)

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

# this function is for testing
def test_read():
    for i in range(tower_count + 1):
        clusterno = map[i]
        if i in clusters[clusterno]:
            print "Node {0} in cluster {1}".format(i, clusterno)
        else:
            print "ERROR: cluster {0} NOT in cluster {1}".format(i, clusterno)
    print "Testing done"

def read_cellspan1():
    global log_loc1
    log_loc1 = [dict() for i in range(person_count + 1)]
    global exists1
    exists1 = [0] * (person_count + 1)
    #global exists2
    #exists2 = [0] * (person_count + 1)
    global sum_time1
    sum_time1 = [0] * (person_count + 1)
    #global sum_time2
    #sum_time2 = [0] * (person_count + 1)
    global entry_count1
    entry_count1 = [0] * (person_count + 1)

    # changed from person_count to 10
    for i in range(1, person_count + 1):
        #if i == 20:
        #    continue
        filename = 'cellspan{0}-1.txt'.format(i)
        if path.exists(filename):
            file = open(filename, 'r')
        else:
            continue
    
        print "Opening " + filename

        exists1[i] = 1
        # iterate through each line of file
        while(1):
            try:
                line = pickle.load(file)
            except EOFError:
                break

            #clusterno = line['celltower_oid']
            clusterno = map[line['celltower_oid']]
            duration = timedelta_to_days(line['endtime'] - line['starttime'])
            if duration < 0:
                duration = 0
            log_loc1[i][clusterno] = log_loc1[i].get(clusterno, 0) + float(duration)
            entry_count1[i] += 1

        # obtain sum of all time
        sum_time1[i] = sum(log_loc1[i].itervalues())
        for k, v in log_loc1[i].iteritems():
            if log_loc1[i][k] < 0:
                print "OVERFLOW: {0}".format(log_loc1[i][k])
            log_loc1[i][k] = float(log_loc1[i][k]) / sum_time1[i]

def compute_hamming(a, b):
    sum = 0
    for i in range(1, tower_count + 1):
        sum += abs(a.get(i, 0) - b.get(i, 0))
    return sum

def read_cellspan2():
    global log_loc2
    log_loc2 = [dict() for i in range(person_count + 1)]
    global exists2
    exists2 = [0] * (person_count + 1)
    #global exists2
    #exists2 = [0] * (person_count + 1)
    global sum_time2
    sum_time2 = [0] * (person_count + 1)
    #global sum_time2
    #sum_time2 = [0] * (person_count + 1)
    global hamming_loc
    hamming_loc = [dict() for i in range(person_count + 1)]
    global min_index
    min_index = [-1] * (person_count + 1)
    global entry_count2
    entry_count2 = [0] * (person_count + 1)
    
    for i in range(1, person_count + 1):
        filename = 'cellspan{0}-2.txt'.format(i)
        if path.exists(filename):
            file = open(filename, 'r')
        else:
            continue
        
        print "Opening " + filename
        exists2[i] = 1
        # iterate through each line of file
        while(1):
            try:
                line = pickle.load(file)
            except EOFError:
                break
            
            #clusterno = line['celltower_oid']
            clusterno = map[line['celltower_oid']]
            duration = timedelta_to_days(line['endtime'] - line['starttime'])
            if duration < 0:
                duration = 0
            log_loc2[i][clusterno] = log_loc2[i].get(clusterno, 0) + float(duration)
            entry_count2[i] += 1
        
        # obtain sum of all time
        sum_time2[i] = sum(log_loc2[i].itervalues())
        for k, v in log_loc2[i].iteritems():
            if log_loc2[i][k] < 0:
                print "OVERFLOW {0}".format(log_loc2[i][k])
            log_loc2[i][k] = float(log_loc2[i][k]) / sum_time2[i]

        # compute hamming
        min_diff = float("inf")
        for j in range(1, person_count + 1):
            # compute hamming score if person exists
            if exists1[j]:
                hamming_loc[i][j] = compute_hamming(log_loc2[i], log_loc1[j])
            else:
                hamming_loc[i][j] = float("inf")
            # update min if necessary
            if hamming_loc[i][j] < min_diff:
                min_diff = hamming_loc[i][j]
                min_index[i] = j

def output_results():
    valid = list()

    count = 0
    avg_num1 = 0
    avg_num2 = 0

    for i in range(1, person_count + 1):
        if exists2[i] == 1 and exists1[i] == 1:
            count += 1
            avg_num1 += entry_count1[i]
            avg_num2 += entry_count2[i]
            valid.append(i)
    print "TOTAL ANON: {0}".format(count)
    # divide avg time across all users
    avg_num1 = float(avg_num1) / count
    avg_num2 = float(avg_num2) / count

    # count the number of correct items
    avg_num_correct1 = 0
    avg_num_correct2 = 0
    avg_num_wrong1 = 0
    avg_num_wrong2 = 0

    correct_count = 0
    for i in valid:
        if i == min_index[i]:
            correct_count += 1
            avg_num_correct1 += entry_count1[i]
            avg_num_correct2 += entry_count2[i]
        else:
            avg_num_wrong1 += entry_count1[i]
            avg_num_wrong2 += entry_count2[i]
    
    avg_num_correct1 = float(avg_num_correct1) / correct_count
    avg_num_correct2 = float(avg_num_correct2) / correct_count
    if correct_count == count:
        avg_num_wrong1 = 0
        avg_num_wrong2 = 0
    else:
        avg_num_wrong1 = float(avg_num_wrong1) / (count - correct_count)
        avg_num_wrong2 = float(avg_num_wrong2) / (count - correct_count)
    print "TOTAL CORRECT: {0}".format(correct_count)
    print ""

    # correct items: average call time 2nd sem; average call time 1st sem
    # wrong items: average call time 2nd sem; average call time 1st sem
    print "All items: average num 2nd sem {0}\n           average num 1st sem {1}".format(avg_num2, avg_num1)
    print "Correct items: average num 2nd sem {0}\n               average num 1st sem {1}".format(avg_num_correct2, avg_num_correct1)
    print "Wrong items: average num 2nd sem {0}\n             average num 1st sem {1}".format(avg_num_wrong2, avg_num_wrong1)

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
        sorted_hamming = sorted(hamming_loc[i].iteritems(), key=itemgetter(1))
        # if i != j:
        if i != min_index[i]:
            print "WRONG"
            # print index that i occurs at
            for j in range(len(sorted_hamming)):
                if sorted_hamming[j][0] == i:
                    print "Actual Anon ({0}) occurs at position {1}".format(i, j)
                    break
            # print 2nd sem call time; 1st sem correct id call time, 1st sem wrong id call time
            print "2nd sem log num: {0}".format(entry_count2[i])
            print "1st sem returned value log num: {0}".format(entry_count1[min_index[i]])
            print "1st sem actual value log num: {0}".format(entry_count1[i])
            diff = sorted_hamming[1][1] - sorted_hamming[0][1]
            avg_diff_wrong += diff
            if largest_diff_wrong < diff:
                largest_diff_wrong = diff
                largest_ind = i
        else:
            print "CORRECT"
            # print 2nd sem call time; 1st sem call time
            print "2nd sem log num: {0}".format(entry_count2[i])
            print "1st sem log num: {0}".format(entry_count1[i])
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

def read_cellspan():
    global log_loc
    log_loc = [dict() for i in range(person_count + 1)]
    global exists
    exists = [0] * (person_count + 1)
    global sum_time
    sum_time = [0] * (person_count + 1)
    global entry_count
    entry_count = [0] * (person_count + 1)
    
    for i in range(1, person_count + 1):
        # OPEN FILE 1
        filename = 'cellspan{0}-1.txt'.format(i)
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
            
                clusterno = line['celltower_oid']
            #clusterno = map[line['celltower_oid']]
                duration = timedelta_to_days(line['endtime'] - line['starttime'])
                if duration < 0:
                    duration = 0
                log_loc[i][clusterno] = log_loc[i].get(clusterno, 0) + float(duration)
                entry_count[i] += 1
        
        # OPEN FILE 2
        filename = 'cellspan{0}-2.txt'.format(i)
        if path.exists(filename):
            file = open(filename, 'r')
            print "Opening " + filename
            exists[i] = 1
            while(1):
                try:
                    line = pickle.load(file)
                except EOFError:
                    break
                    
                clusterno = line['celltower_oid']
            #clusterno = map[line['celltower_oid']]
                duration = timedelta_to_days(line['endtime'] - line['starttime'])
                if duration < 0:
                    duration = 0
                log_loc[i][clusterno] = log_loc[i].get(clusterno, 0) + float(duration)
                entry_count[i] += 1
    
        if exists[i] == 1:
            # obtain sum of all time
            sum_time[i] = sum(log_loc[i].itervalues())
            for k, v in log_loc[i].iteritems():
                if log_loc[i][k] < 0:
                    print "OVERFLOW: {0}".format(log_loc[i][k])
                log_loc[i][k] = float(log_loc[i][k]) / sum_time[i]

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
                rank[i][j] = compute_hamming(log_loc[i], log_loc[j])
            else:
                rank[i][j] = float("inf")

def output_rank():
    for i in range(1, person_count + 1):
        print "RANKED SIMILARITIES: {0} (converts to {1}, then to {2}) ".format(i, convert[i], network[convert[i]]) + pos[i]
        sorted_hamming = sorted(rank[i].iteritems(), key=itemgetter(1))
        for tup in sorted_hamming:
            if tup[0] != i:
                print "{0} {1} {2} ({3}, {4}) ".format(i, tup[0], tup[1], convert[tup[0]], network[convert[tup[0]]]) + pos[tup[0]]

def create_profiles():
    global profile # list of dictionaries (distributions)
    profile = [dict() for i in range(5)]
    for i in range(1, 5): # i is profile index 
        count = 0
        for j in range(1, person_count + 1): # j is user index
            if pos[j] != i: # if j is not the correct kind of user, skip
                continue
            dis_sum = sum(log_loc[j].itervalues())
            if dis_sum == 0:
                continue
            count += 1
            print "sum for person {0} is {1}".format(j, dis_sum)
            for k, v in log_loc[j].iteritems(): # k is tower number
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
            rank[i][j] = compute_hamming(log_loc[i], profile[j]) / freq[j] # adjust for distrib

def print_results():
    correct_count = 0
    wrong_count = 0
    correct_hamm = 0
    wrong_hamm = 0
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
            correct_hamm += sorted_hamming[0][1]
        else:
            print "WRONG"
            wrong_count += 1
            wrong_hamm += sorted_hamming[0][1]
        for tup in sorted_hamming:
            print "{0} {1} {2} ({3}, {4})".format(i, tup[0], tup[1], convert[tup[0]], network[convert[tup[0]]],)

    print "{0} CORRECT, {1} WRONG".format(correct_count, wrong_count)
    print "correct hamm {0}, wrong hamm {1}".format(correct_hamm/correct_count, wrong_hamm/wrong_count)

def print_conversions():
    global usable
    usable = list()
    for i in range(1, person_count + 1):
        print "{0} -> {1} -> {2}".format(i, convert[i], network[convert[i]])
        if network[convert[i]] != 0:
            usable.append(network[convert[i]])
    print usable

def select_pairs():
    pairs = [(1, 2), (2, 3), (3, 4), (4, 5)] #put all friends pairs here
    friends = len(pairs)

    max = len(usable)
    while len(pairs) < 2 * friends:
        x = usable[random.randint(1, max)]
        y = usable[random.randint(1, max)]
        if (x , y) in pairs or (y, x) in pairs or x == y:
            continue
        pairs.append((x, y))

    print pairs

def is_valid(x, y):
    if x in usable and y in usable:
        print "YES"
    else:
        print "NO"


print_conversions()
#select_pairs()
is_valid(90, 91)


#read_out()
#read_survey()
#read_cellspan1()
#read_cellspan2()
#output_results()

read_cellspan()
create_profiles()

compare_profiles()
print_results()

#compute_similarity()
#output_rank()
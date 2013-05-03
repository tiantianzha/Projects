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



def read_file(person, sem, log):
    filename = 'cellspan{0}-{1}.txt'.format(person, sem)
    if path.exists(filename):
        f = open(filename, 'r')
    else:
        return 0
    
    while(1):
        try:
            line = pickle.load(f)
        except EOFError:
            break

        # discard strange entries
        if line['starttime'] > line['endtime']:
            continue
        tup = (line['celltower_oid'], line['starttime'], line['endtime'])
        log.append(tup)

    return 1


# converts timedelta to hours
def timedelta_to_hours(td):
    return (float(td.microseconds)/(1000*3600) + float(td.seconds)/(3600) + float(td.days)*24)


# compute overlap between 2 logs
def compute_overlap(a, b):
    a_len = len(a)
    b_len = len(b)
    i = j = 0
    overlap = dict()
    
    # constants
    id = 0
    start = 1
    end = 2
    
    while (i < a_len and j < b_len):
        # update current values
        ca = a[i]
        cb = b[j]
        #print "a at {0}".format(i)
        #print ca
        #print "b at {0}".format(j)
        #print cb
        # if a is behind b
        if ca[start] <= cb[start] and ca[end] <= cb[start]:
            i += 1
            #print "advance a"
            continue
        # if b is behind a
        if cb[start] <= ca[start] and cb[end] <= ca[start]:
            j += 1
            #print "advance b"
            continue
        # if a starts to overlap b
        if ca[start] <= cb[start] and ca[end] >= cb[start]:
            # ca before cb
            if ca[end] <= cb[end]:
                #print "overlap! ca before cb"
                if ca[id] == cb[id]:
                    #print "same ID"
                    overlap[ca[id]] = overlap.get(ca[id], 0) + timedelta_to_hours(ca[end] - cb[start])
                i += 1
                continue
            # ca engulfs cb
            if ca[end] >= cb[end]:
                #print "overlap! ca engulfs cb"
                if ca[id] == cb[id]:
                    #print "same ID"
                    overlap[ca[id]] = overlap.get(ca[id], 0) + timedelta_to_hours(cb[end] - cb[start])
                j += 1
                continue
        # if b starts to overlap a
        if cb[start] <= ca[start] and cb[end] >= ca[start]:
            # cb before ca
            if cb[end] <= ca[end]:
                #print "overlap! cb before ca"
                if ca[id] == cb[id]:
                    #print "same ID"
                    overlap[ca[id]] = overlap.get(ca[id], 0) + timedelta_to_hours(cb[end] - ca[start])
                j += 1
                continue
            # cb engulfs ca
            if cb[end] >= ca[end]:
                #print "overlap! cb engulfs ca"
                if ca[id] == cb[id]:
                    #print "same ID"
                    overlap[ca[id]] = overlap.get(ca[id], 0) + timedelta_to_hours(cb[end] - cb[start])
                i += 1
                continue
    return overlap



# iterate between given person and all other persons
def iterate_pairs(person):
    # populate entries for this person
    log = list()
    ret1 = read_file(person, 1, log)
    ret2 = read_file(person, 2, log)
    results_list = dict()
    
    if (ret1 == 0 and ret2 == 0):
        return None

            # changed from person count to 10
    for i in range(1, person_count + 1):
        if i == person:
            continue
        print "person {0} and {1}".format(person, i)
        other_log = list()
        ret1 = read_file(i, 1, other_log)
        ret2 = read_file(i, 2, other_log)
        if (ret1 == None and ret2 == None):
            continue
        results = compute_overlap(log, other_log)
        results_list[(person, i)] = results

    sum_time = dict()
    for tup, results in results_list.iteritems():
        sum_time[tup[1]] = sum(results.itervalues())
    sorted_sum_time = sorted(sum_time.iteritems(), key=itemgetter(1), reverse=True)
    print sorted_sum_time
    return sorted_sum_time


# given a dict of dicts; print
def print_results(person, results, f):
    f.write("RESULTS FOR PERSON {0}\n".format(person))
    f.write("converts to survey {0} and network {1}\n".format(convert[person], network[convert[person]]))
    if convert[person] == 0:
        p = position[person]
    else:
        p = pos[convert[person]]
    f.write("position is " + p + "\n")
    overlap = dict()
    for pair, log in results.iteritems():
        overlap[pair] = sum(log.itervalues())
    sorted_overlap = sorted(overlap.iteritems(), key=itemgetter(1), reverse=True)
    for tup in sorted_overlap:
        pair = tup[0]
        print pair
        f.write("RESULTS FOR {0} and {1}: {2} HOURS\n".format(pair[0], pair[1], tup[1]))
        if convert[pair[1]] == 0:
            p = position[pair[1]]
        else:
            p = pos[convert[pair[1]]]
        f.write("position is " + p + "\n")
        log = results[tup[0]]
        sorted_log = sorted(log.iteritems(), key=itemgetter(1), reverse=True)
        for item in sorted_log:
            f.write("{0}: {1}\n".format(item[0], item[1]))
        f.write("\n")
        


# iterate through all possible pairs
def old_main():
    for i in range(1, person_count + 1): # change to person_count + 1
        results = iterate_pairs(i)
        if results == None:
            continue
        filename = 'overlap{0}.txt'.format(i)
        file = open(filename, 'w+')
        print_results(i, results, file)

def conversion():
    global usable
    usable = list()
    global id_to_network
    id_to_network = [0] * (person_count + 1)
    global network_to_id
    network_to_id = [0] * (95)
    
    for i in range(1, person_count + 1):
        #print "{0} -> {1} -> {2}".format(i, convert[i], network[convert[i]])
        if network[convert[i]] != 0:
            usable.append(network[convert[i]])

    for i in range(1, person_count + 1):
        nw = network[convert[i]]
        id_to_network[i] = nw
        network_to_id[nw] = i
        

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

def main():
    conversion()
    
    correct_pairs = [(2, 5), (2, 6), (2, 10), (2, 11), (2, 20), (4, 8), (4, 13), (4, 19), (8, 4), (8, 13), (8, 23), (10, 2), (10, 92), (13, 4), (13, 8), (13, 23), (19, 31), (20, 2), (20, 3), (20, 6), (20, 50), (21, 53), (21, 84), (23, 13), (28, 88), (31, 19), (32, 57), (34, 33), (36, 59), (36, 85), (36, 86), (53, 21), (53, 84), (55, 46), (56, 25), (56, 26), (57, 15), (57, 32), (59, 43), (59, 85), (59, 86), (63, 55), (63, 70), (63, 81), (66, 81), (70, 43), (70, 63), (70, 65), (73, 83), (77, 2), (77, 5), (77, 6), (81, 63), (81, 66), (84, 3), (84, 21), (84, 53), (85, 21), (85, 36), (85, 59), (85, 86), (89, 78), (90, 91), (92, 2)]

    all_pairs = list()
    max = len(correct_pairs)
    for tup in correct_pairs:
        x = network_to_id[tup[0]]
        y = network_to_id[tup[1]]
        all_pairs.append((x, y))

    while len(all_pairs) < 2 * max:
        x = usable[random.randint(1, max)]
        y = usable[random.randint(1, max)]
        if (x , y) in all_pairs or (y, x) in all_pairs or x == y:
            continue
        all_pairs.append((x, y))

    ranking = dict()
    time_spent = dict()
    skip = 0
    for pair in all_pairs:
        skip += 1
        if skip < 34:
            continue
        list_of_rank = iterate_pairs(pair[0])
        if list_of_rank == None:
            print "INVALID"
            print pair
            continue
        for i in range(len(list_of_rank)):
            if list_of_rank[i][0] == pair[1]:
                ranking[pair] = i + 1
                time_spent[pair] = list_of_rank[i][1]
                print pair
                print "OR {0}, {1}".format(id_to_network[pair[0]], id_to_network[pair[1]])
                print "  rank {0}".format(ranking[pair])
                print "  time spent {0}".format(time_spent[pair])
                break
    print ranking

    sorted_ranking = sorted(ranking.iteritems(), key=itemgetter(1), reverse=True)
    print sorted_ranking
    correct_count = 0
    for tup in sorted_ranking:
        x = id_to_network[tup[0][0]]
        y = id_to_network[tup[0][1]]
        if (x, y) in correct_pairs:
            correct_count += 1
            print "{0}, {1} OR {2}, {3}".format(x, y, tup[0], tup[1])



#read_survey()
main()
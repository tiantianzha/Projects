from os import environ
from MySQLdb import connect
from MySQLdb import cursors
import datetime
from operator import itemgetter

#----------------------------------------------------------------------------------#

# Edge object saves the 2 endpoints (oid, neighbour), and maintains an array
# of weights, each entry corresponding to a person

class Edge:
    def __init__(self, oid, neighbour, person_oid, person_num):
        self.oid = oid
        self.neighbour = neighbour
        self.person_num = person_num
        self.total_weight = 1
        self.weights = [0] * (person_num + 1)
        self.weights[person_oid] += 1

    def add_edge(self, old, new, person):
        assert self.oid == old
        assert self.neighbour == new
        self.weights[person] += 1
        self.total_weight += 1

    def print_edge(self):
        print "    from {0} to {1}: {2}".format(self.oid, self.neighbour, self.total_weight)
        #for i in range(1, self.person_num + 1):
        #    if self.weights[i] == 0: 
        #        continue
        #    print "        person_oid : {0}, weight = {1}".format(i, self.weights[i])
            
#----------------------------------------------------------------------------------#

# Tower object maintains a list of outgoing edges between this tower and other towers

class Tower:
    def __init__(self, oid, person_num):
        self.oid = oid
        self.visits = 0
        self.person_num = person_num
        self.neighbours = list()
        # print "done creating 1 tower"

    def add_edge(self, old, new, person):
        assert self.oid == old
        added = 0
        for n in self.neighbours: # n is of type edge
            if n.neighbour == new:
                n.add_edge(old, new, person);
                added = 1
        if (added == 0):
            self.neighbours.append(Edge(old, new, person, self.person_num))

    def add_visit(self):
        self.visits += 1

    def print_tower(self):
        print "  tower_oid: {0}, visited {1} times".format(self.oid, self.visits)
        for edge in self.neighbours:
            edge.print_edge()

#----------------------------------------------------------------------------------#

# Graph object: contains a list of all towers

class Graph:

    # Initialize empty graph with no phone calls
    def __init__(self, tower_num, person_num):
        self.tower_num = tower_num
        self.person_num = person_num
        self.towers = [Tower(i, person_num) for i in range(tower_num + 1)]

    # Add a phone call
    def add_edge(self, old, new, person):
        self.towers[new].add_visit()
        self.towers[old].add_edge(old, new, person)

    # Add a visit
    def add_visit(self, tower_oid):
        self.towers[tower_oid].add_visit()

    # Print the graph
    def print_graph(self):
        print "number of towers : {0}".format(self.tower_num)
        for i in range(1, len(self.towers)):
            self.towers[i].print_tower()
              
    def get_visits(self, i):
        return self.towers[i].visits

    # had to do this because I couldn't access towers[i] from outside code
    # this seems only to apply with arrays
    # Graph instance has no attribute __getitem__
    def get_oid(self, i):
        return self.towers[i].oid

#----------------------------------------------------------------------------------#

def data_connect():

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

    # find tower_count
    cursor.execute('select max(celltower_oid) as celltower_oid from cellspan')
    row = cursor.fetchone()
    global tower_count
    tower_count = row['celltower_oid']

    # find person_count
    cursor.execute('select max(person_oid) as person_oid from cellspan')
    row = cursor.fetchone()
    global person_count
    person_count = row['person_oid']

def build_graph():

    # find tower_count
    cursor.execute('select max(celltower_oid) as celltower_oid from cellspan')
    row = cursor.fetchone()
    global tower_count
    tower_count = row['celltower_oid']
    print "tower count : {0}".format(tower_count)

    # find person_count
    cursor.execute('select max(person_oid) as person_oid from cellspan')
    row = cursor.fetchone()
    global person_count
    person_count = row['person_oid']
    print "person count : {0}".format(person_count)

    # create graph of callers and callees
    towers = Graph(tower_count, person_count)
    print "done creating graph"

    # populate the graph by querying database
    for i in range(1, person_count + 1):
        cursor.execute('select * from cellspan where person_oid = ' + str(i))
        row = cursor.fetchone()
        if (row == None):
            print "person {0} has no location data".format(i)
            continue
        old_tower = row['celltower_oid'];
        towers.add_visit(old_tower)
        row = cursor.fetchone()
        while row:
            new_tower = row['celltower_oid']
            towers.add_edge(old_tower, new_tower, i)
            old_tower = new_tower
            row = cursor.fetchone()
        print "done with person {0}".format(i)

    print "done adding to graph"
    # towers.print_graph()
    
    for i in range(16000, len(towers.towers) + 1):
        recorded = towers.get_visits(i)
        cursor.execute('select count(*) from cellspan where celltower_oid = '
                       + str(towers.get_oid(i)))
        actual = cursor.fetchone()['count(*)']        
        #if (recorded != actual):
        print "for tower {0}: recorded = {1}, actual = {2}".format(towers.get_oid(i), recorded, actual)

def find_paths():

    global sem_start
    global sem_end
    sem_start1 = datetime.datetime(2004, 8, 30, 0, 0, 0, 0)
    sem_end1 = datetime.datetime(2004, 12, 17, 11, 59, 59, 0)
    sem_start2 = datetime.datetime(2005, 2, 1, 0, 0, 0, 0)
    sem_end2 = datetime.datetime(2005, 5, 20, 11, 59, 59, 0)
    sem_start3 = datetime.datetime(2005, 8, 29, 0, 0, 0, 0)
    sem_end3 = datetime.datetime(2004, 12, 22, 11, 59, 59, 0)
    duration = datetime.timedelta(0, 600)
    transition = datetime.timedelta(0, 600)
    # print duration
    # print transition

    global all_paths
    all_paths = [list() for i in range(person_count + 1)]

    for i in range(1, person_count + 1):
        query = ('select * from cellspan where person_oid = ' + str(i) 
                 + ' and starttime > "' + str(sem_start1) 
                 + '" and starttime < "' + str(sem_end1) 
                 + '" or starttime > "' + str(sem_start2) 
                 + '" and starttime < "' + str(sem_end2)
                 + '" or starttime > "' + str(sem_start3)
                 + '" and starttime < "' + str(sem_end3) + '"')
        cursor.execute(query)

        row = cursor.fetchone()
        if row == None:
            continue

        old_start = row['starttime']
        old_end = row['endtime']
        
        # start the first path
        one_path = list()
        one_path.append(row['celltower_oid'])
        in_path = 1

        row = cursor.fetchone()
        
        # loops through to find all paths of current user
        while (row):
            new_start = row['starttime']
            new_end = row['endtime']
            
            # start a new path
            if (in_path == 0):
                one_path.append(row['celltower_oid'])
                in_path = 1

            # if this is a hidden end destination
            elif (new_start - old_end > transition):
                all_paths[i].append(one_path)
                one_path = list()
                one_path.append(row['celltower_oid'])
  
            # if this is an end destination
            elif (new_end - new_start > duration):
                one_path.append(row['celltower_oid'])
                all_paths[i].append(one_path)
                one_path = list()
                in_path = 0
                
            # usual situation--continue path
            else:
                one_path.append(row['celltower_oid'])

            old_start = new_start
            old_end = new_end
            row = cursor.fetchone()

        # outside of while loop--end case
        if (in_path == 1):
            all_paths[i].append(one_path)    

def find_osc_pairs(path):
    # print(path)
    pairs = list()
    check_pairs = list()
    thresh = 3

    freq = dict()
    valid = list()

    # count frequency of nodes
    for node in path:
        freq[node] = freq.get(node, 0) + 1

    # create list consisting of those appearing more than once
    for k, v in freq.iteritems():
        if v >= 2:
            valid.append(k);
            
    for node in valid:
        first = node
        # print "first is {0}".format(first)
        for node in path:
            second = node
            # print "  second is {0}".format(second)
            if first == second:
                #print "    first == second"
                continue
            if (first, second) in check_pairs or (second, first) in check_pairs:
                #print "    already found {0}, {1}".format(first, second)
                continue
            # print "    checking if osc pair"
            to_seek = None
            transitions = 0
            for node in path:
                if to_seek == None:
                    if node == first:
                        to_seek = second
                        # print "to_seek was none, now second"
                    elif node == second:
                        to_seek = first
                        # print "to_seek was none, now first"
                    else:
                        continue
                elif to_seek == first:
                    if node == first:
                        to_seek = second
                        transitions += 1
                        #print "to seek was first, now second, transitions = {0}".format(transitions)
                    else:
                        continue
                
                else: 
                    if node == second:
                        to_seek = first
                        transitions += 1
                        #print "to seek was second, now first, transitions = {0}".format(transitions)
            if transitions >= thresh:
                if first < second:
                    check_pairs.append((first, second))
                    pairs.append(((first, second), transitions))
                else:
                    check_pairs.append((second, first))
                    pairs.append(((second, first), transitions))
                #print "    found pair: {0}, {1}; {2}".format(first, second, transitions)
    #for item in pairs:
        #print "{0}, {1}: {2}".format(item[0][0], item[0][1], item[1])
    return pairs


def find_all_osc():
    global osc_pairs
    global valid_pairs
    valid_pairs = list()
    osc_pairs = dict()
    osc_pairs_weighted = dict()
    # iterate through all users
    for user_paths in all_paths:
        # iterate through all paths
        for path in user_paths:
            if len(path) <= 3:
                continue
            pairs = find_osc_pairs(path)
            for pair in pairs:
                osc_pairs[pair[0]] = osc_pairs.get(pair[0], 0) + 1
                # print "updated : {0}, {1}".format(pair[0], osc_pairs.get(pair[0])) 
                osc_pairs_weighted[pair[0]] = osc_pairs_weighted.get(pair[0], 0) + pair[1]
    print "\nunweighted"
    global sorted_osc_pairs
    sorted_osc_pairs = sorted(osc_pairs.iteritems(), key=itemgetter(1), reverse=True)
    #sorted_osc_pairs_w = sorted(osc_pairs_weighted.iteritems(), 
                                #key=itemgetter(1), reverse=True)
    sum_osc = sum(osc_pairs.itervalues())
    thresh = 0.001 * sum_osc

    for item in sorted_osc_pairs:
        print "{0} {1} {2}".format(item[0][0], item[0][1], item[1])

def get_names():
    cursor.execute('select * from cellname')
    result = cursor.fetchall()
     
    global all_names       
    all_names = [[] for i in range(tower_count + 1)]

    for row in result:
        celltower = row['celltower_oid']
        all_names[celltower].append(row['name'].lower())

    global tower_name
    tower_name = ['\0' for i in all_names]
    for i in range(len(all_names)):
        if len(all_names[i]) == 0:
            continue
        tower_name[i] = max(set(all_names[i]), key = all_names[i].count)
   
    #tower_name = [max(set(all_names[i]), key = all_names[i].count) 
    #              for i in range(tower_count + 1)]
    


def assign_cluster():

    global cluster_list
    global cluster_name
    global tower_to_cluster
    closest_tower = [None] * (tower_count + 1)
    pair_list = list()
    tower_to_cluster = [-1 for i in range(tower_count + 1)]
    cluster_list = dict()
    cluster_name = dict()
    cluster_index = 0

    # find closest tower for each tower
    for pair in valid_pairs:
        if closest_tower[pair[0][0]] == None:
            closest_tower[pair[0][0]] = (pair[0][1], pair[1])
        if closest_tower[pair[0][1]] == None:
            closest_tower[pair[0][1]] = (pair[0][0], pair[1])

    # create pairs list
    for i in range(tower_count + 1):
        if closest_tower[i] != None:
            if (closest_tower[i][0], i) not in pair_list:
                pair_list.append((i, closest_tower[i][0]))
                #print "{0}, {1}".format(i, closest_tower[i][0])

    for pair in pair_list:
        print pair
    # use closest tower to find clusters
    for pair in pair_list:
        added = 0
        for k, v in cluster_list.items(): # think about the order
            if pair[0] in v:
                v.append(pair[1])
                tower_to_cluster[pair[1]] = k
                added = 1
                break
            if pair[1] in v:
                v.append(pair[0])
                tower_to_cluster[pair[0]] = k
                added = 1
                break
        if added == 1:
            continue
        cluster_list[cluster_index] = [pair[0], pair[1]]
        # give non-null name if possible
        cluster_name[cluster_index] = tower_name[pair[0]]
        if tower_name[pair[0]] == '\0':
            if tower_name[pair[1]] == '\0':
                cluster_name[cluster_index] = str(pair[0])
            else:
                cluster_name[cluster_index] = tower_name[pair[1]]
        # link cluster index
        tower_to_cluster[pair[0]] = cluster_index
        tower_to_cluster[pair[1]] = cluster_index
        cluster_index += 1

    # printing
    for i in range(len(cluster_list)):
        print "cluster {0}: {1}".format(i, cluster_name[i])
        print "  {0}".format(cluster_list[i])
        #for j in range(len(cluster_list[i])):
        #    print "  {0} -- proper indexing: {1}".format(cluster_list[i][j], tower_to_cluster[cluster_list[i][j]])


def build_histogram():
    global aggregate
    
    cursor.execute('select max(person_oid) as person_oid from cellspan')
    row = cursor.fetchone()
    global person_count
    person_count = row['person_oid']
    aggregate = [dict() for i in range(person_count + 1)]

    for i in range(person_count + 1):
        print "person {0}".format(i)
        query = ('select * from cellspan where person_oid = ' + str(i) 
                 + ' and starttime > "' + str(sem_start) 
                 + '" and starttime < "' + str(sem_end) + '"')
        cursor.execute(query)

        row = cursor.fetchone()
        if row == None:
            continue

        while row:
            duration = max(datetime.timedelta(0), row['endtime'] - row['starttime'])
            cluster = tower_to_cluster[row['celltower_oid']]
            if cluster == -1:
                cluster = row['celltower_oid']
            # print "  tower {0} in cluster {1}".format(row['celltower_oid'], cluster)
            aggregate[i][cluster] = aggregate[i].get(cluster, datetime.timedelta(0)) + duration
            row = cursor.fetchone()

    for i in range(person_count + 1):
        print "person {0}".format(i)
        for k, v in aggregate[i].items():
            print "cluster {0}, time {1}".format(k, v)

def difference(person):
    score = [datetime.timedelta(0) for i in range(person_count + 1)]
    ref_time = sum(aggregate[person])

    for i in range(person_count + 1):
        if i == person:
            continue

        total_time = sum(aggregate[i]) 
        for k, v in aggregate[i].items():
            diff = v - aggregate[person].get(k, datetime.timedelta(0))
            score[i] += abs(diff)

    for i in range(person_count + 1):
        print "person {0}, score {1}".format(i, score[i])
            
def main():
    data_connect()
    find_paths()
    find_all_osc()

main()











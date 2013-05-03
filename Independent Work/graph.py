from graphics import *
from os import environ
from MySQLdb import connect
from MySQLdb import cursors

#----------------------------------------------------------------------------------#

# Call object: contains the fields of a phone call

class Call:
    def __init__(self, caller, callee):
    #def __init__(self, caller, callee, direction, voice, start, end):
        self.caller = caller
        self.callee = callee
        #self.direction = direction
        #self.voice = voice
        #self.start = start
        #self.end = end

    def print_call(self):
        print "\t\tcaller is " + str(self.caller) + ", callee is " + str(self.callee)

#----------------------------------------------------------------------------------#

# Person object: contains person and a phone log. Each phone log entry is a list of
# calls with that callee. If log entry[i] == None, no contact with that person.

class Person:
    def __init__(self, person_oid, entries):
        self.person_oid = person_oid
        self.phonebook = [None]*entries

    def add_call(self, new_call):
        assert self.person_oid == new_call.caller
        if self.phonebook[new_call.callee] == None:
            self.phonebook[new_call.callee] = list()
        self.phonebook[new_call.callee].append(new_call)

    def print_person(self):
        print "person_oid is " + str(self.person_oid)
        print "phonebook:"
        for i in range (0, len(self.phonebook)):
            print "\tto callee " + str(i)
            if self.phonebook[i] == None:
                continue
            for j in range (0, len(self.phonebook[i])):
                self.phonebook[i][j].print_call()

#----------------------------------------------------------------------------------#

# Graph object: contains a list of all the callers (callees are identified only
# by number.

class Graph:

    # Initialize empty graph with no phone calls
    def __init__(self, caller_num, callee_num):
        self.caller_num = caller_num
        self.callee_num = callee_num
        self.caller = list()
        for i in range (0, caller_num):
            self.caller.append(Person(i, callee_num))

    # Add a phone call
    def add_call(self, new_call):
        # print new_call.caller
        self.caller[new_call.caller].add_call(new_call);

    # Print the graph
    def print_graph(self):
        print "number of callers : " + str(self.caller_num)
        print "number of callees : " + str(self.callee_num)
        for i in range (0, len(self.caller)):
            self.caller[i].print_person()

    # Draw a person as a circle
    def draw_person(self, win, colour, x, y):
        person = Point(x, y)
        person.setFill(colour)
        person.setOutline(colour)
        person.draw(win)

    # Draw a line between two persons
    def draw_edge(self, win, caller, callee):
        left_pad = 20
        length = 2660
        caller_y = 50
        callee_y = 750
        caller_x = left_pad + caller * length / self.caller_num
        callee_x = left_pad + callee * length / self.callee_num
        line = Line(Point(caller_x, caller_y), Point(callee_x, callee_y))
        line.draw(win)
        # print "drawing edge between " + str(caller) + " and " + str(callee)

    # Draw the graph
    def draw_graph(self):

        win = GraphWin("Calls bipartite graph", 2700, 800)
        win.setBackground('white')

        left_pad = 20
        length = 2660
        caller_y = 50
        callee_y = 750

        for i in range(0, self.caller_num):
            x = left_pad + i * length / self.caller_num
            self.draw_person(win, 'red', x, caller_y)
            
        for i in range(0, self.callee_num):
            x = left_pad + i * length / self.callee_num
            self.draw_person(win, 'blue', x, callee_y)
            # print i
            # print callee_num

        for i in range(0, self.caller_num):
            for j in range (0, self.callee_num):
                if self.caller[i].phonebook[j] != None:
                    self.draw_edge(win, i, j)
                
                


#----------------------------------------------------------------------------------#

def main():

    # establish connection to database
ef main():

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
    cursor = connection.cursor(cursors.DictCursor)

    # find max value for person_oid
    cursor.execute('select max(person_oid) as person_oid from callspan')
    row = cursor.fetchone()
    caller_count = row['person_oid']
    print "caller count : " + str(caller_count)

    # find max value for phonenumber_oid
    cursor.execute('select max(phonenumber_oid) as phonenumber_oid from callspan')
    row = cursor.fetchone()
    callee_count = row['phonenumber_oid']
    print "callee count : " + str(callee_count)

    # create graph of callers and callees
    mit = Graph(caller_count + 1, callee_count + 1)
    #mit.draw_graph()

    # populate the graph by querying database
    cursor.execute(
        'select * from callspan')

   

    row = cursor.fetchone()
    while row:
        caller = row['person_oid']
        callee = row['phonenumber_oid']
        # print "caller id : " + str(caller) + ", callee id : " +  str(callee)
        new_call = Call(caller, callee)
        mit.add_call(new_call)
        row = cursor.fetchone()

    mit.draw_graph()

    print "done drawing graph"
    
    while 1:
        x = 1
    


if __name__ == '__main__':
    main()

else:

    # Test client
    # numbers = (0, 1, 2)
    caller_num = 100
    callee_num = 200

    mit = Graph(caller_num, callee_num)

#alice = Person(0, numbers)
    call1 = Call(0, 1)
#call1.print_call()
    call2 = Call(0, 1)
    call3 = Call(0, 2)

    call4 = Call(1, 0)
    call5 = Call(20, 100)

#print alice.person_oid
#print alice.phonebook

    mit.add_call(call1)
    mit.add_call(call2)
    mit.add_call(call3)
    mit.add_call(call4)
    mit.add_call(call5)

#mit.print_graph()
    mit.draw_graph()


    while (1):
        x = 1






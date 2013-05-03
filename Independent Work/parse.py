import string
from pygraph.classes.graph import graph
from graphics import *

global tower_count
global person_count
tower_count = 32656
person_count = 97

# read from stdin
def read_file():
    global pairs
    pairs = dict()
    f1 = open('sem1.txt', 'r+')
    f2 = open('sem2.txt', 'r+')
    
    line = f1.readline()
    while (line):
        num = string.split(line)
        pairs[(int(num[0]), int(num[1]))] = int(num[2])
        line = f1.readline()
    
    line = f2.readline()
    while (line):
        num = string.split(line)
        pair = (int(num[0]), int(num[1]))
        pairs[pair] = pairs.get(pair, 0) + int(num[2])
        line = f2.readline()

    f3 = open('total.txt', 'r+')
    for pair in pairs.iteritems():
        f3.write("{0} {1} {2}\n".format(pair[0][0], pair[0][1], pair[1]))
        f3.write("{1} {0} {2}\n".format(pair[0][0], pair[0][1], pair[1]))

def create_graph():
    global gr
    gr = graph()
    gr.add_nodes([i for i in range(tower_count + 1)])
    for k, v in pairs.iteritems():
        print k
        print v
        gr.set_edge_weight(k, v)
    edges = gr.edges()
    for e in edges:
        print "({0}, {1}): {2}\n".format(e[0], e[1], gr.edge_weight(e))

def id_to_point(id):
    pad = 20
    wid = 208
    hei = 157
    unit = 4
    
    id = id - 1
    x = pad + (id % wid) * unit
    y = pad + int(id / wid) * unit
    p = Point(x, y)
    return p

def draw_graph():
    win = GraphWin("Oscillating pairs", 872, 668)
    win.setBackground('white')

    for i in range(1, tower_count + 1):
        p = id_to_point(i)
        p.setFill('blue')
        p.setOutline('blue')
        p.draw(win)

    edges = gr.edges()
    for e in edges:
        p1 = id_to_point(e[0])
        p2 = id_to_point(e[1])
        wt = gr.edge_weight(e)
        line = Line(p1, p2)
        line.draw(win)


read_file()
#create_graph()
#draw_graph()
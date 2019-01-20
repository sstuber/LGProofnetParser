import networkx as nx
import LoLaLinkNode
import matplotlib.pyplot as plt

from NodeFactory import *
from Graph import *

MATCH_REGEX = r'(\w+|\(.+\))(\/|\\)(\(.+\)|\w+)|(\w+)'
function_dict = {
    '/': 'right',
    '\\': 'left',
    None: 'singleton'
}

upgraded_regex = r'(diamond)?(square)?(\w+|\(.+\))(\/|\\)(diamond)?(square)?(\(.+\)|\w+)|(diamond)?(square)?(\w+)'
#(diamond)?(square)?(\w+|\(.+\))(\/|\\)(diamond)?(square)?(\(.+\)|\w+)|(diamond)?(square)?(\w+)
if __name__ == '__main__':

    print("begin main")

    print("begin test connection")
    g1 = LoLaGraph()
    g1.addNode(NODE_FACTORY.createLinkNode(g1)) #0
    g1.addNode(NODE_FACTORY.createLinkNode(g1)) #1

    g1.addNode(NODE_FACTORY.createVertex(g1, "s"))      #2
    g1.addNode(NODE_FACTORY.createVertex(g1, "sos"))    #3
    g1.addNode(NODE_FACTORY.createVertex(g1, "s"))      #4
    g1.addNode(NODE_FACTORY.createVertex(g1, "sosonp")) #5
    g1.addNode(NODE_FACTORY.createVertex(g1, "np"))     #6

    g1.graph.add_edge(0, 2, parent=2)
    g1.graph.add_edge(0, 3, parent=0)
    g1.graph.add_edge(0, 4, parent=0)

    g1.graph.add_edge(1, 3, parent=3)
    g1.graph.add_edge(1, 5, parent=5)
    g1.graph.add_edge(1, 6, parent=1)

    g2 = LoLaGraph()
    g2.addNode(NODE_FACTORY.createLinkNode(g2)) #7
    g2.addNode(NODE_FACTORY.createLinkNode(g2)) #8

    g2.addNode(NODE_FACTORY.createVertex(g2, "s"))    #9
    g2.addNode(NODE_FACTORY.createVertex(g2, "snps")) #10
    g2.addNode(NODE_FACTORY.createVertex(g2, "nps"))  #11
    g2.addNode(NODE_FACTORY.createVertex(g2, "np"))   #12
    g2.addNode(NODE_FACTORY.createVertex(g2, "s"))    #13

    g2.graph.add_edge(7, 9, parent=9)
    g2.graph.add_edge(7, 10, parent=7)
    g2.graph.add_edge(7, 11, parent=7)

    g2.graph.add_edge(8, 11, parent=11)
    g2.graph.add_edge(8, 12, parent=12)
    g2.graph.add_edge(8, 13, parent=8)
    g1.getPossibleConnections(g2)

    print("end test connection")

    print("begin test connection")

    g3 = LoLaGraph()
    g3.addNode(NODE_FACTORY.createLinkNode(g3)) #14
    g3.addNode(NODE_FACTORY.createLinkNode(g3)) #15
    g3.getNode(15).type = LinkType.Par

    g3.addNode(NODE_FACTORY.createVertex(g3, "w")) #16
    g3.addNode(NODE_FACTORY.createVertex(g3, "x")) #17
    g3.addNode(NODE_FACTORY.createVertex(g3, "y")) #18
    g3.addNode(NODE_FACTORY.createVertex(g3, "z")) #19

    g3.addEdge(14, 16)
    g3.addEdge(14, 17)
    g3.addEdge(18, 14)
    g3.addEdge(15, 18)
    g3.addEdge(17, 15)
    g3.addEdge(19, 15)

    contractions = g3.getPossibleContractions()

    g3.draw()
    for g in contractions:
        g.draw()

    print("end test contract")

    print("end main")

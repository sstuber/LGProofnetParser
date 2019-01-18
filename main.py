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

    g1 = LoLaGraph()
    g1.addNode(NODE_FACTORY.createVertex(g1))
    g1.addNode(NODE_FACTORY.createVertex(g1))
    g1.addNode(NODE_FACTORY.createVertex(g1))
    g1.addNode(NODE_FACTORY.createLinkNode(g1))

    g1.graph.add_edge(0, 3, parent=0)
    g1.graph.add_edge(1, 3, parent=3)
    g1.graph.add_edge(2, 3, parent=3)

    leaves = g1.getLeaves()

    for leaf in leaves:
        print(leaf.nodeId)

    nx.draw(g1.graph)
    # plt.show()



    print("end main")

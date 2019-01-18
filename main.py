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

    print('k')
    #userString = input('')

    #userString.split(' ')

    g1 = LoLaGraph()
    g1.addNode(NODE_FACTORY.createLinkNode())
    g1.addNode(NODE_FACTORY.createLinkNode())
    g1.graph.add_edge(0, 1)

    g2 = LoLaGraph()
    g2.addNode(NODE_FACTORY.createLinkNode())
    g2.addNode(NODE_FACTORY.createLinkNode())
    g2.graph.add_edge(2, 3)

    g2.updateNode(2, 0)


    g3 = nx.compose(g1.graph, g2.graph)



    G = nx.petersen_graph()

    labels = {0:"asdioh",1:"diashodioasd",3:"asidohasiod"}
    node_color = ['r','g','b']
    plt.subplot(121)
    nx.draw(g3, with_labels=True, labels=labels, node_color=node_color, node_size=1000)
    plt.show()
    #
    # g3 = nx.compose(g1.graph, g2.graph)
    #
    # # nx.draw(g3)
    #
    # print(g3.edges())

    print('doeg')
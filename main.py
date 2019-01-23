import networkx as nx
import LoLaLinkNode
import matplotlib.pyplot as plt
from Prover import *
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

    # graph = LoLaGraph()
    #
    # graph.addNode(NODE_FACTORY.createVertex(graph, '(np\s)/np'))
    #
    # new_graph = graph.unfold_graph()
    #
    #
    # new_graph.getNode(0)
    #
    # new_graph.draw()


    # print("begin main")
    #
    # print("begin test connection")
    # g1 = LoLaGraph()
    #
    # g1.addNode(NODE_FACTORY.createLinkNode(g1)) #0
    # g1.addNode(NODE_FACTORY.createLinkNode(g1)) #1
    #
    # g1.addNode(NODE_FACTORY.createVertex(g1, "s"))      #2
    # g1.addNode(NODE_FACTORY.createVertex(g1, "sos"))    #3
    # g1.addNode(NODE_FACTORY.createVertex(g1, "s"))      #4
    # g1.addNode(NODE_FACTORY.createVertex(g1, "sosonp")) #5
    # g1.addNode(NODE_FACTORY.createVertex(g1, "np"))     #6
    #
    # g1.graph.add_edge(0, 2, parent=2)
    # g1.graph.add_edge(0, 3, parent=0)
    # g1.graph.add_edge(0, 4, parent=0)
    #
    # g1.graph.add_edge(1, 3, parent=3)
    # g1.graph.add_edge(1, 5, parent=5)
    # g1.graph.add_edge(1, 6, parent=1)
    #
    # g2 = LoLaGraph()
    #
    # g2.addNode(NODE_FACTORY.createLinkNode(g2)) #7
    # g2.addNode(NODE_FACTORY.createLinkNode(g2)) #8
    #
    # g2.addNode(NODE_FACTORY.createVertex(g2, "s"))    #9
    # g2.addNode(NODE_FACTORY.createVertex(g2, "snps")) #10
    # g2.addNode(NODE_FACTORY.createVertex(g2, "nps"))  #11
    # g2.addNode(NODE_FACTORY.createVertex(g2, "np"))   #12
    # g2.addNode(NODE_FACTORY.createVertex(g2, "s"))    #13
    #
    # g2.graph.add_edge(7, 9, parent=9)
    # g2.graph.add_edge(7, 10, parent=7)
    # g2.graph.add_edge(7, 11, parent=7)
    #
    # g2.graph.add_edge(8, 11, parent=11)
    # g2.graph.add_edge(8, 12, parent=12)
    # g2.graph.add_edge(8, 13, parent=8)
    # g1.getPossibleConnections(g2)
    #
    # print("end test connection")
    #
    # print("begin test contraction")
    #
    # g3 = LoLaGraph()
    #
    # g3.addNode(NODE_FACTORY.createLinkNode(g3)) #14
    # g3.addNode(NODE_FACTORY.createLinkNode(g3)) #15
    # g3.getNode(15).type = LinkType.Par
    #
    # g3.addNode(NODE_FACTORY.createVertex(g3, "w")) #16
    # g3.addNode(NODE_FACTORY.createVertex(g3, "x")) #17
    # g3.addNode(NODE_FACTORY.createVertex(g3, "y")) #18
    # g3.addNode(NODE_FACTORY.createVertex(g3, "z")) #19
    #
    # g3.addEdge(child_id=14, parent_id=16)
    # g3.addEdge(child_id=14, parent_id=17)
    # g3.addEdge(child_id=18, parent_id=14)
    # g3.addEdge(child_id=15, parent_id=18)
    # g3.addEdge(child_id=17, parent_id=15)
    # g3.addEdge(child_id=19, parent_id=15)
    #
    # contractions = g3.getPossibleContractions()
    #
    # print("end test contraction")
    #
    # print("begin test rewrite")
    #
    # g4 = LoLaGraph()
    #
    # g4.addNode(NODE_FACTORY.createLinkNode(g4)) #21
    # g4.addNode(NODE_FACTORY.createLinkNode(g4)) #22
    #
    # g4.addNode(NODE_FACTORY.createVertex(g4, "y")) #24
    # g4.addNode(NODE_FACTORY.createVertex(g4, "x")) #23
    # g4.addNode(NODE_FACTORY.createVertex(g4, "u")) #25
    # g4.addNode(NODE_FACTORY.createVertex(g4, "v")) #26
    # g4.addNode(NODE_FACTORY.createVertex(g4, "w")) #27
    #
    # g4.addEdge(child_id=20, parent_id=22)
    # g4.addEdge(child_id=20, parent_id=23)
    # g4.addEdge(child_id=24, parent_id=20)
    # g4.addEdge(child_id=21, parent_id=24)
    # g4.addEdge(child_id=25, parent_id=21)
    # g4.addEdge(child_id=26, parent_id=21)
    #
    # rewritings = g4.getPossibleRewritings()
    #
    # print("end test rewrite")
    sentence = "games that kids love but parents hate"
    targetType = "n"
    print("begin test: " + sentence + " |- " + targetType)
    prover = Prover()
    lexicon = get_types_file_dict()
    prover.prove(sentence, lexicon, targetType)
    print("end test " + sentence)

    print("end main")

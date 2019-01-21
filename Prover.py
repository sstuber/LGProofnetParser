from LoLaLinkNode import *
from Graph import *

class Prover:
    def __init__(self):
        print("gegroet!")

    def prove(self, sequent, targetType):
        # derivations = []
        # build the proof nets
        # connect the trees
        # for each connection:
        #   # keep applying contractions and structural rules until stuck
        #   # if it is a tensor tree, add to derivations
        #   # else go to next connection
        # for each derivation:
        #   # return the proof net and the proof term
        return True

    def buildGraph(self):
        return True

    def create_unfolded_graph_from_word(self, sequent):
        graph = LoLaGraph()
        graph.addNode(NODE_FACTORY.createVertex(graph, sequent))

        graph = graph.unfold_graph()

        return graph


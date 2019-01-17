
import networkx as nx

class LoLaGraph:

    def __init__(self, parent_graph=None):
        self.parentGraph = parent_graph

        #nx.Graph().add_node();

        print('we graph now')


    # return list of new graphs that are possible steps
    def connect(self, graph):
        print('we folded')

    # return list of new graphs that are possible contractions
    def contract(self):
        print('we contracted')

    # returns bool
    def isTensorTree(self):
        return False




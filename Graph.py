
import networkx as nx

class LoLaGraph:

    def __init__(self, parent_graph=None):
        self.parentGraph = parent_graph

        self.graph = nx.Graph()

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

    # niet naar beneden scrollen






















    # echt niet doen






















    # KIJK WEG LUL



















    # :(

    def addNode(self, node):
        self.graph.add_node(node.nodeId, node=node)

    def getNode(self, nodeId):
        return self.graph.nodes()[nodeId]['node']

    def updateNode(self, nodeId, newId):
        adj = list(self.graph.adj[nodeId])
        self.graph.add_node(newId, node=self.getNode(nodeId))
        for neighborId in adj:
            self.graph.add_edge(newId, neighborId)
        self.graph.remove_node(nodeId)

    def draw(self):
        print("ik moet hier drawen")
from LoLaLinkNode import *
import networkx as nx
import itertools
import matplotlib.pyplot as plt

class LoLaGraph:

    def __init__(self, parent_graph=None):
        self.parentGraph = parent_graph

        self.graph = nx.Graph()

        print('we graph now')


    # return list of new graphs that are possible steps
    def getPossibleConnections(self, otherGraph):
        leaves = [leaf.nodeId for leaf in self.getLeaves()]
        otherLeaves = [leaf.nodeId for leaf in otherGraph.getLeaves()]

        combinations = [zip(leaf, otherLeaves)
                       for leaf in itertools.permutations(leaves, len(otherLeaves))]


        combinations = [list(ding) for ding in combinations]

        combinations = [all_combinations(ding) for ding in combinations]

        newGraphs = []
        for chain in combinations:
            for combination in chain:
                newGraph = self.connect(otherGraph, combination)
                if newGraph:
                    newGraphs.append(newGraph)

        for newGraph in newGraphs:
            print(newGraph)



    # connect two graphs
    # return new graph if connectionMap is exactly possible
    # else return None
    def connect(self, otherGraph, connectionMap):

        for connection in connectionMap:
            v1 = self.getNode(connection[0])
            v2 = otherGraph.getNode(connection[1])
            if not v1.canConnect(v2):
                return None

        #TODO: connect graphs according to map and return
        return connectionMap

    # return list of new graphs that are possible contractions
    def contract(self):
        print('we contracted')

    # returns bool
    def isTensorTree(self):
        return False

    # return all vertices that are leaves
    def getLeaves(self):

        leaves = []
        for v in dict(self.graph.nodes()).values():
            node = v['node']
            if(type(node) is LoLaVertex) and node.getVertexType() is not VertexType.NotALeaf:
                leaves.append(node)
        return leaves

    # add a node to the graph (index = nodeId)
    def addNode(self, node):
        self.graph.add_node(node.nodeId, node=node)

    # return the node from the graph with nodeId
    def getNode(self, nodeId):
        return self.graph.nodes()[nodeId]['node']

    # Update the nodeId to newId
    def updateNode(self, nodeId, newId):
        adj = list(self.graph.adj[nodeId])
        self.graph.add_node(newId, node=self.getNode(nodeId))
        for neighborId in adj:
            self.graph.add_edge(newId, neighborId)
        self.graph.remove_node(nodeId)

    def getParents(self, nodeId):
        adj = self.graph.adj[nodeId]
        parents = []
        for k, v in dict(adj).items():
            if v['parent'] is not nodeId:
                parents.append(k)
        return parents

    def getChildren(self, nodeId):
        adj = self.graph.adj[nodeId]
        children = []
        for k, v in dict(adj).items():
            if v['parent'] is nodeId:
                children.append(k)
        return children

    def draw(self):
        # build color list and label dictionary
        colors = []
        labels = {}

        for k, v in dict(self.graph.nodes()).items():
            node = v['node']
            colors.append(node.getColor())
            if type(node) is LoLaVertex:
                labels[node.nodeId] = node.sequent

        # draw the graph
        nx.draw(self.graph, show_labels=True, labels=labels, node_color=colors, node_size=1000)
        plt.show()

def all_combinations(any_list):
    return itertools.chain.from_iterable(
        itertools.combinations(any_list, i + 1)
        for i in range(len(any_list)))

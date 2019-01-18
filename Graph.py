from LoLaLinkNode import *
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
        print("ik moet hier drawen")
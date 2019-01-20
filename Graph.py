from LoLaLinkNode import *
import networkx as nx
import itertools
import matplotlib.pyplot as plt
from NodeFactory import *

class LoLaGraph:

    def __init__(self, parent_graph=None):
        self.parentGraph = parent_graph
        self.graph = nx.Graph()

    # return list of new graphs that can be created from connecting with otherGraph
    def getPossibleConnections(self, otherGraph):
        leaves = [leaf.nodeId for leaf in self.getLeaves()]
        otherLeaves = [leaf.nodeId for leaf in otherGraph.getLeaves()]

        combinations = [zip(leaf, otherLeaves)
                       for leaf in itertools.permutations(leaves, len(otherLeaves))]


        combinations = [list(ding) for ding in combinations]



        combinations = [all_combinations(ding) for ding in combinations]

        visited = set()
        newGraphs = []
        for chain in combinations:
            for combination in chain:
                if(combination not in visited):
                    visited.add(combination)
                    newGraph = self.connect(otherGraph, combination)
                    if newGraph:
                        newGraphs.append(newGraph)

        # for newGraph in newGraphs:
        #     newGraph.draw()

    # connect two graphs
    # return new graph if connectionMap is exactly possible
    # else return None
    def connect(self, otherGraph, connectionMap):

        for connection in connectionMap:
            v1 = self.getNode(connection[0])
            v2 = otherGraph.getNode(connection[1])
            if not v1.canConnect(v2):
                return None

        newGraph = LoLaGraph(self)
        newGraph.graph = self.graph.copy()

        for connection in connectionMap:
            newGraph.updateNode(connection[0], connection[1])

        newGraph.graph = nx.compose(newGraph.graph, otherGraph.graph)

        return newGraph

    # return list of new graphs that can be created from contracting
    def getPossibleContractions(self):
        contractions = []
        for vertex in self.getVertices():
            contraction = self.contract(vertex)
            if contraction:
                contractions.append(contraction)

        return contractions

    # Contract a graph at vertex and return resulting graph. return none if impossible.
    def contract(self, vertex):
        # first assert the H vertex is not a conclusion
        if vertex.getVertexType() == VertexType.Conclusion:
            return None
        # this is the upper of two links
        upperLink = self.getNode(self.getChildren(vertex.nodeId)[0])
        downLink = self.getNode(self.getChildren(self.getChildren(upperLink.nodeId)[0])[0])

        # the links must be a different type
        if upperLink.type == downLink.type:
            return None
        # the links must share two vertices
        sharedVertices = upperLink.getSharedVertices(downLink, self)
        if len(sharedVertices) is not 2:
            return None
        # the shared vertices may not include the hypothesis
        if vertex.nodeId in sharedVertices:
            return None

        # the conclusion is the child of the remaining link that is not in shared vertices
        conclusion = [v for v in self.getChildren(downLink.nodeId) if v not in sharedVertices][0]

        # remove the two links and the shared vertices
        newGraph = LoLaGraph(self)
        newGraph.graph = self.graph.copy()

        newGraph.graph.remove_node(upperLink)
        newGraph.graph.remove_node(downLink)
        newGraph.graph.remove_nodes_from(sharedVertices)

        newGraph.joinVertices(vertex, conclusion)

        return newGraph

    # return list of new graphs that can be created from rewriting
    def getPossibleRewritings(self):
        rewritings = []
        for link in self.getLinks():
            rewriting = self.rewrite(link)
            if rewriting:
                for r in rewriting:
                    rewritings.append(r)

        return rewritings

    # Rewrite a graph at vertex and return resulting graph. return none if impossible.
    def rewrite(self, link):
        # NOTE: contractions only happen to tensor links connected as > · <
        if link.type is LinkType.Par:
            return False
        if link.getLinkShape(self) is LinkShape.Upward:
            return False
        if self.getNode(self.getChildren(link.nodeId)[0]).getVertexType() is VertexType.Conclusion:
            return False

        otherLink = self.getNode(self.getChildren(self.getChildren(link.nodeId)[0])[0])

        if otherLink.type is LinkType.Par:
            return False
        if otherLink.getLinkShape(self) is LinkShape.Downward:
            return False

        # We are now certain that we are dealing with > · < tensor links
        # There are 4 possible structural rewrites
        # in each rewrite, the tensor changes shape

        x, y = self.getParents(link.nodeId)
        u = link.getSharedVertices(otherLink, self)[0]
        v, w = self.getChildren(otherLink.nodeId)

        return [self.applyStructuralRule(link, otherLink, x, y, u, v, w, 0),
                self.applyStructuralRule(link, otherLink, x, y, u, v, w, 1),
                self.applyStructuralRule(link, otherLink, x, y, u, v, w, 2),
                self.applyStructuralRule(link, otherLink, x, y, u, v, w, 3)]

    # apply structural rule to rewrite graph
    def applyStructuralRule(self, link, otherLink, x, y, u, v, w, rule):
        newGraph = LoLaGraph(self)
        newGraph.graph = self.graph.copy()
        newGraph.graph.remove_node(link)
        newGraph.graph.remove_node(otherLink)
        newLink = newGraph.addNode(NODE_FACTORY.createLinkNode(self))
        newOtherLink = newGraph.addNode(NODE_FACTORY.createLinkNode(self))

        if rule is 0:
            newGraph.addEdge(newLink, x)
            newGraph.addEdge(v, newLink)
            newGraph.addEdge(u, newLink)
            newGraph.addEdge(newOtherLink, u)
            newGraph.addEdge(newOtherLink, y)
            newGraph.addEdge(w, newOtherLink)
        elif rule is 1:
            newGraph.addEdge(newLink, x)
            newGraph.addEdge(v, newLink)
            newGraph.addEdge(newLink, u)
            newGraph.addEdge(u, newOtherLink)
            newGraph.addEdge(newOtherLink, y)
            newGraph.addEdge(w, newOtherLink)
        elif rule is 2:
            newGraph.addEdge(newLink, x)
            newGraph.addEdge(u, newLink)
            newGraph.addEdge(w, newLink)
            newGraph.addEdge(newOtherLink, u)
            newGraph.addEdge(newOtherLink, y)
            newGraph.addEdge(v, newOtherLink)
        elif rule is 3:
            newGraph.addEdge(newLink, y)
            newGraph.addEdge(v, newLink)
            newGraph.addEdge(u, newLink)
            newGraph.addEdge(newOtherLink, x)
            newGraph.addEdge(newOtherLink, u)
            newGraph.addEdge(w, newOtherLink)
        return newGraph

    # acyclic, connected, without cotensor links
    def isTensorTree(self):
        if not nx.is_connected(self.graph):
            return False
        for link in self.getLinks():
            if link.type is LinkType.Par:
                return False
        if nx.find_cycle(self.graph, 'ignore'):
            return False
        return True

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
        return node

    def addEdge(self,child, parent):
        self.graph.add_edge(child.nodeId, parent.nodeId, parent=parent.nodeId)

    def addEdge(self,child: int, parent: int):
        self.graph.add_edge(child, parent, parent=parent)

    # return the node from the graph with nodeId
    def getNode(self, nodeId):
        return self.graph.nodes()[nodeId]['node']

    # Update the nodeId to newId
    def updateNode(self, nodeId, newId):
        # get the node from the graph we wish to update
        adj = self.graph.adj[nodeId]
        node = self.getNode(nodeId)
        self.graph.add_node(newId, node=self.getNode(nodeId))
        # remove the node from the graph
        self.graph.remove_node(nodeId)
        # restore the edges
        for neighborId, v in adj.items():
            parentId = v['parent']
            if parentId is nodeId:
                parentId = newId
            self.graph.add_edge(newId, neighborId, parent=parentId)

    # combine two vertices into one (after contraction)
    def joinVertices(self, node, otherNode):
        # get the adj of the node
        nodeAdj = self.graph.adj[node]
        # get the adj of the otherNode
        otherNodeAdj = self.graph.adj[otherNode]
        # create the union of both nodes
        joinedNode = self.addNode(NODE_FACTORY.createVertex(self, "x"))
        # remove the nodes from the graph
        self.graph.remove_node(node)
        self.graph.remove_node(otherNode)
        # restore the edges
        for neighborId, v in nodeAdj.items():
            parentId = v['parent']
            if parentId is node:
                parentId = joinedNode.nodeId
            self.graph.add_edge(joinedNode.nodeId, neighborId, parent=parentId)
        for neighborId, v in otherNodeAdj.items():
            parentId = v['parent']
            if parentId is otherNode:
                parentId = joinedNode.nodeId
            self.graph.add_edge(joinedNode.nodeId, neighborId, parent=parentId)


    #TODO: ensure left first
    def getParents(self, nodeId):
        adj = self.graph.adj[nodeId]
        parents = []
        for k, v in dict(adj).items():
            if v['parent'] is not nodeId:
                parents.append(k)
        return parents

    #TODO: ensure left first
    def getChildren(self, nodeId: int):
        adj = self.graph.adj[nodeId]
        children = []
        for k, v in dict(adj).items():
            if v['parent'] is nodeId:
                children.append(k)
        return children

    def getNeighbors(self, nodeId):
        return self.getParents(nodeId) + self.getChildren(nodeId)

    def getVertices(self):
        return [self.getNode(v) for v in self.graph.nodes() if type(self.getNode(v)) is LoLaVertex]

    def getLinks(self):
        return [self.getNode(v) for v in self.graph.nodes() if type(self.getNode(v)) is LoLaLinkNode]

    def draw(self):
        # build color list and label dictionary
        colors = []
        labels = {}

        for k, v in dict(self.graph.nodes()).items():
            node = v['node']
            colors.append(node.getColor())
            if type(node) is LoLaVertex:
                labels[node.nodeId] = str(node.nodeId) + " " + node.sequent

        # draw the graph
        nx.draw(self.graph, show_labels=True, labels=labels, node_color=colors, node_size=1000)
        plt.show()

def all_combinations(any_list):
    return itertools.chain.from_iterable(
        itertools.combinations(any_list, i + 1)
        for i in range(len(any_list)))

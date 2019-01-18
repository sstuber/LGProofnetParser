
from enum import Enum

class VertexType(Enum):
    Premise = 'premise'
    Conclusion = 'conclusion'
    NotALeaf = 'notaleaf'


class LinkType(Enum):
    Tensor = 'tensor'
    Par = 'Par'


# type of function
class LinkMode(Enum):
    Unary = 'unary'
    Binary = 'binary'


class LoLaLinkNode:

    def __init__(self, nodeId, graph):

        self.nodeId = nodeId

        # list of premise vertices
        self.premises = []

        # list of conclusion vertices
        self.conclusions = []

        self.type = LinkType.Tensor

        # type of function
        self.mode = LinkMode.Binary

        # vertex that combines the other nodes (main vertex)
        self.main = None

        self.graph = graph

        print("")

    def __hash__(self):
        return hash(self.nodeId)

    def __eq__(self, other):
        if type(other) == int:
            return self.nodeId == other
        return self.nodeId == other.nodeId

class LoLaVertex:



    def __init__(self, nodeId, graph):

        self.nodeId = nodeId
        self.vertexType = None
        self.sequent = ''

        # lola graph
        self.graph = graph

    def __hash__(self):
        return hash(self.nodeId)

    def __eq__(self, other):
        if type(other) == int:
            return self.nodeId == other
        return self.nodeId == other.nodeId


    # graph. getadjects of self
    def getLoLaLinkNodes(self):
        return None

    # return the vertex type. Calculate with the graph
    def getVertexType(self):
        parents = self.graph.getParents(self.nodeId)
        children = self.graph.getChildren(self.nodeId)

        if not parents:
            return VertexType.Conclusion
        if not children:
            return VertexType.Premise
        return VertexType.NotALeaf

    # returns a graph that unfolded from
    def unfoldVertex(self):
        print('fold')





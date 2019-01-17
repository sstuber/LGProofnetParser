
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

    def __init__(self, nodeId):

        self.id = nodeId

        # list of premise vertices
        self.premises = []

        # list of conclusion vertices
        self.conclusions = []

        self.type = LinkType.Tensor

        # type of function
        self.mode = LinkMode.Binary

        # vertex that combines the other nodes (main vertex)
        self.main = None

        print("")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

class LoLaVertex:



    def __init__(self, nodeId):

        self.id = nodeId
        self.vertexType = None
        self.sequent = ''

        # lola graph
        self.graph = None


    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


    # graph. getadjects of self
    def getLoLaLinkNodes(self):
        return None

    # return the vertex type. Calculate with the graph
    def getVertexType(self):
        return None

    # returns a graph that unfolded from
    def unfoldVertex(self):
        print('fold')





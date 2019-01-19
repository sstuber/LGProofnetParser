
from enum import Enum
from SequentParser import ParseSequent

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


 # todo Use and fill values
class LoLaLinkNode:

    def __init__(self, nodeId, graph):

        self.nodeId: int = nodeId

        # list of premise vertices
        self.premises = []

        # list of conclusion vertices
        self.conclusions = []

        self.type: LinkType = LinkType.Tensor

        # type of function
        self.mode: LinkMode = LinkMode.Binary

        # vertex that combines the other nodes (main vertex)
        self.main: LoLaVertex = None

        self.graph = graph

        print("")

    def __hash__(self):
        return hash(self.nodeId)

    def __eq__(self, other):
        if type(other) == int:
            return self.nodeId == other
        return self.nodeId == other.nodeId

    def getColor(self):
        if self.type == LinkType.Tensor:
            return 'xkcd:light green'
        return 'xkcd:dark pink'


class LoLaVertex:

    def __init__(self, nodeId, graph, sequent):

        self.nodeId: int = nodeId
        self.sequent: str = sequent

        # lola graph
        self.graph = graph

    def __hash__(self):
        return hash(self.nodeId)

    def __eq__(self, other):
        if type(other) == int:
            return self.nodeId == other
        return self.nodeId == other.nodeId

    def __str__(self):
        return "%i: %s %s" % (self.nodeId, self.sequent, self.getVertexType())

    # TODO implement
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

    # return whether two vertices can connect
    def canConnect(self, other) -> bool:
        return self.sequent is other.sequent and \
               ((self.getVertexType() is VertexType.Premise and other.getVertexType() is VertexType.Conclusion)\
               or (self.getVertexType() is VertexType.Conclusion and other.getVertexType() is VertexType.Premise))

    # returns a graph that unfolded from
    def unfoldVertex(self):

        parsedSequent = ParseSequent(self.sequent)
        vertexType = self.getVertexType()


        print('fold')

    def getColor(self):
        return 'xkcd:sky blue'



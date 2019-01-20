
from enum import Enum
from SequentParser import ParseSequent
# from unfold_vertex_functions import unfold_functions
# TODO: Fix circular dependency between lolalinknode and unfold_vertex_functions

class VertexType(Enum):
    Premise = 'premise'
    Conclusion = 'conclusion'
    NotALeaf = 'notaleaf'


class LinkType(Enum):
    Tensor = 'tensor'
    Par = 'Par'

class LinkShape(Enum):
    Downward = 'downward'
    Upward = 'upward'

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

    def getLinkShape(self, graph):
        if len(graph.getParents(self.nodeId)) == 2:
            return LinkShape.Downward
        return LinkShape.Upward

    def getSharedVertices(self, otherLink, graph):
        return list(set(graph.getNeighbors(self.nodeId)).intersection(
            set(graph.getNeighbors(otherLink.nodeId))
        ))

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

        self.is_unfolded: bool = False

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

    # return the vertex type. Calculate with the graph
    def getVertexType(self):
        parents = self.graph.getParents(self.nodeId)
        children = self.graph.getChildren(self.nodeId)

        if not parents:
            return VertexType.Premise
        if not children:
            return VertexType.Conclusion
        return VertexType.NotALeaf

    # return whether two vertices can connect
    def canConnect(self, other) -> bool:
        self_vertex_type = self.getVertexType()
        other_vertex_type = other.getVertexType()

        return self.sequent is other.sequent and \
               ((self_vertex_type is VertexType.Premise and other_vertex_type is VertexType.Conclusion)\
               or (self_vertex_type is VertexType.Conclusion and other_vertex_type is VertexType.Premise))

    # # returns a graph that unfolded from
    # def unfoldVertex(self):
    #
    #     sequent_type, string_array = ParseSequent(self.sequent)
    #     vertex_type = self.getVertexType()
    #
    #     current_unfold_function = unfold_functions[vertex_type][sequent_type]
    #
    #     unfolded_graph = current_unfold_function(self, string_array)
    #
    #     return unfolded_graph

    def getColor(self):
        return 'xkcd:sky blue'

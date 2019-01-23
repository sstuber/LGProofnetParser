from LoLaDatatypes import VertexType, LinkType, LinkShape, LinkMode
from SequentParser import ParseSequent
# TODO: Fix circular dependency between lolalinknode and unfold_vertex_functions


# type of function


# todo Use and fill values
class LoLaLinkNode:

    def __init__(self, nodeId, graph):

        self.nodeId: int = nodeId

        self.type: LinkType = LinkType.Tensor

        # type of function
        self.mode: LinkMode = LinkMode.Binary

        self.left: bool = True

        self.sequent_type = None

        # vertex that combines the other nodes (main vertex)
        self.main: LoLaVertex = None

        self.graph = graph

    def get_pre_arrow_tuple(self):
        return self.left, self.sequent_type

    # return a copy of a link node
    def copy(self, newGraph):
        newLolaLinkNode = LoLaLinkNode(self.nodeId, newGraph)
        newLolaLinkNode.type = self.type
        newLolaLinkNode.mode = self.mode
        newLolaLinkNode.left = self.left
        newLolaLinkNode.sequent_type = self.sequent_type
        return newLolaLinkNode

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

    def getColor(self, graph):
        if self.type == LinkType.Tensor:
            return 'xkcd:light green'
        return 'xkcd:dark pink'


class LoLaVertex:

    def __init__(self, nodeId, graph, sequent):

        self.nodeId: int = nodeId
        self.sequent: str = sequent

        self.is_unfolded: bool = False

        self.is_sequent_root = False
        self.from_target_type = False
        self.axiom_link = None

        self.word = ""

        # lola graph
        self.graph = graph

    # return a copy of this node
    def copy(self, newGraph):
        newLinkVertex = LoLaVertex(self.nodeId, newGraph, self.sequent)
        newLinkVertex.is_unfolded = self.is_unfolded
        newLinkVertex.is_sequent_root = self.is_sequent_root
        newLinkVertex.from_target_type = self.from_target_type
        newLinkVertex.word = self.word
        return newLinkVertex

    def __hash__(self):
        return hash(self.nodeId)

    def __eq__(self, other):
        if type(other) == int:
            return self.nodeId == other
        return self.nodeId == other.nodeId

    def __str__(self):
        return "%i: %s %s" % (self.nodeId, self.sequent)

    # return the vertex type. Calculate with the graph
    def getVertexType(self, graph):
        parents = graph.getParents(self.nodeId)
        children = graph.getChildren(self.nodeId)

        if graph.node_count() == 1:
            if self.from_target_type:
                return VertexType.Premise
            return VertexType.Conclusion

        if not parents:
            return VertexType.Premise
        if not children:
            return VertexType.Conclusion
        return VertexType.NotALeaf

    # return whether two vertices can connect
    def canConnect(self, otherVertex, graph, otherGraph) -> bool:
        self_vertex_type = self.getVertexType(graph)
        other_vertex_type = otherVertex.getVertexType(otherGraph)

        return self.sequent == otherVertex.sequent and \
               ((self_vertex_type == VertexType.Premise and other_vertex_type == VertexType.Conclusion) \
                or (self_vertex_type == VertexType.Conclusion and other_vertex_type == VertexType.Premise))

     # returns a graph that unfolded from
    def unfoldVertex(self, graph, unfold_function, new_graph):

        sequent_type, string_array = ParseSequent(self.sequent)
        vertex_type = self.getVertexType(graph)

        if self.from_target_type:
            vertex_type = VertexType.Premise

        changed_graph = unfold_function(vertex_type, sequent_type, self, string_array, new_graph)

        return changed_graph

    def getColor(self, graph):
        if self.getVertexType(graph) is VertexType.Premise:
            return 'xkcd:orange'
        if self.getVertexType(graph) is VertexType.Conclusion:
            return 'xkcd:pale sky blue'
        return 'xkcd:light mauve'

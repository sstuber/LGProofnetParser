from LoLaDatatypes import VertexType, LinkType, LinkShape, LinkMode
from SequentParser import ParseSequent

# tensor/par link in the graph
class LoLaLinkNode:

    def __init__(self, nodeId, graph):
        self.nodeId: int = nodeId
        self.type: LinkType = LinkType.Tensor
        self.mode: LinkMode = LinkMode.Binary
        self.left: bool = True
        self.sequent_type = None
        self.main: LoLaVertex = None
        self.graph = graph

    # helper function for unfolding graph
    def get_pre_arrow_tuple(self):
        return self.left, self.sequent_type

    # return a fresh deep copy of a link node
    def copy(self, newGraph):
        newLolaLinkNode = LoLaLinkNode(self.nodeId, newGraph)
        newLolaLinkNode.type = self.type
        newLolaLinkNode.mode = self.mode
        newLolaLinkNode.left = self.left
        newLolaLinkNode.sequent_type = self.sequent_type
        return newLolaLinkNode

    # return whether the link faces up or down i.e. /\ or \/
    def getLinkShape(self, graph):
        if len(graph.getParents(self.nodeId)) == 2:
            return LinkShape.Downward
        return LinkShape.Upward

    # return the set of vertices shared between two links
    def getSharedVertices(self, otherLink, graph):
        return list(set(graph.getNeighbors(self.nodeId)).intersection(
            set(graph.getNeighbors(otherLink.nodeId))
        ))

    # hash the link with its node id
    def __hash__(self):
        return hash(self.nodeId)

    # compare two links using their node id
    def __eq__(self, other):
        if type(other) == int:
            return self.nodeId == other
        return self.nodeId == other.nodeId

    # give a color for drawing in networkX (tensor = green, par = pink)
    def getColor(self, graph):
        if self.type == LinkType.Tensor:
            return 'xkcd:light green'
        return 'xkcd:dark pink'

# vertex in the graph
class LoLaVertex:

    def __init__(self, nodeId, graph, sequent):
        self.nodeId: int = nodeId
        self.sequent: str = sequent
        self.is_unfolded: bool = False
        self.is_sequent_root = False
        self.from_target_type = False
        self.axiom_link = None
        self.word = ""
        self.graph = graph

    # return a fresh deep copy of this node
    def copy(self, newGraph):
        newLinkVertex = LoLaVertex(self.nodeId, newGraph, self.sequent)
        newLinkVertex.is_unfolded = self.is_unfolded
        newLinkVertex.is_sequent_root = self.is_sequent_root
        newLinkVertex.from_target_type = self.from_target_type
        newLinkVertex.word = self.word
        newLinkVertex.axiom_link = self.axiom_link
        return newLinkVertex

    # hash the vertex with its node id
    def __hash__(self):
        return hash(self.nodeId)

    # compare two vertices using their node id
    def __eq__(self, other):
        if type(other) == int:
            return self.nodeId == other
        return self.nodeId == other.nodeId

    # pretty print a node
    def __str__(self):
        return "%i: %s" % (self.nodeId, self.sequent)

    # return the set of links shared between two vertices (max 1)
    def getSharedLinks(self, otherVertex, graph):
        return list(set(graph.getNeighbors(self.nodeId)).intersection(
            set(graph.getNeighbors(otherVertex.nodeId))
        ))

    # return the vertex type (premise, conclusion, notALeaf)
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

     # unfold the vertex and return the resulting graph
    def unfoldVertex(self, graph, unfold_function, new_graph):

        sequent_type, string_array = ParseSequent(self.sequent)
        vertex_type = self.getVertexType(graph)

        if self.from_target_type:
            vertex_type = VertexType.Premise

        changed_graph = unfold_function(vertex_type, sequent_type, self, string_array, new_graph)

        return changed_graph

    # give a color for drawing in networkX (premise = orange, conclusion = blue, notALeaf = mauve)
    def getColor(self, graph):
        if self.getVertexType(graph) is VertexType.Premise:
            return 'xkcd:orange'
        if self.getVertexType(graph) is VertexType.Conclusion:
            return 'xkcd:pale sky blue'
        return 'xkcd:light mauve'

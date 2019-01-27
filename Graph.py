import networkx as nx
import itertools
import matplotlib.pyplot as plt
from unfold_vertex_functions import unfoldVertex
from NodeFactory import *
from LoLaDatatypes import *


# A wrapper around networkX that stores a proof net or proof structure and has helper functions
class LoLaGraph:

    def __init__(self, parent_graph=None):
        self.parentGraph = parent_graph
        self.graph = nx.Graph()

    # determine whether two graphs are isomorphic (utilizes the adjacency and node id's)
    def __eq__(self, other):
        return nx.is_isomorphic(self.graph, other.graph)

    # hash a graph by using the edge degree
    def __hash__(self):
        return hash(tuple(sorted(self.graph.degree())))

    # go to the farthest ancestor of this graph
    def get_deep_parent(self):
        tmp_graph = self.parentGraph

        if tmp_graph is None:
            return self
        return tmp_graph.get_deep_parent()

    # returns a fresh deep graph copy
    def copy(self):
        newLoLaGraph = LoLaGraph(self.parentGraph)
        newGraph = self.graph.copy()
        ding = dict(newGraph.nodes())
        for k, v in ding.items():
            v['node'] = v['node'].copy(newLoLaGraph)
        newLoLaGraph.graph = newGraph
        return newLoLaGraph

    # Get the words in a graph from left to right DFS
    def getOrderedPremises(self):
        # starting at conclusion, traversing left-first
        stack = [self.getConclusions()[0]]
        discovered = set()
        premises = []
        while stack:
            node = stack.pop()
            if node not in discovered:
                discovered.add(node)
                adj = self.graph.adj[node.nodeId]
                right = [x for x in adj if adj[x]['alignment'] is EdgeAlignment.Right]
                straight = [x for x in adj if adj[x]['alignment'] is EdgeAlignment.Straight]
                left = [x for x in adj if adj[x]['alignment'] is EdgeAlignment.Left]

                if right:
                    for ding in right:
                        stack.append(self.getNode(ding))
                if straight:
                    for ding in straight:
                        stack.append(self.getNode(ding))
                if left:
                    for ding in left:
                        stack.append(self.getNode(ding))

                # if we are at a premise, add to the word order
                if type(node) is LoLaVertex and node.getVertexType(self) is VertexType.Premise:
                    premises.append(node)

        return premises

    # check if the word order in the graph corresponds to the input sentence
    def hasCorrectWordOrder(self, sentence):
        premiseOrder = list(map(lambda x: x.word, self.getOrderedPremises()))
        return sentence.lower() == " ".join(premiseOrder)

    # check if the graph has only 1 conclusion vertex and if that vertex has the expected sequent
    def hasCorrectConclusion(self, conclusion):
        return len(self.getConclusions()) == 1 and self.getConclusions()[0].sequent == conclusion

    # connect a graph according to the connection map and check if sentence and target type are correct
    def connect(self, connectionMap, sentence, targetType):
        newGraph = self.copy()

        # try to apply each step in the connection map
        for connectionType in connectionMap:
            for connection in connectionType:
                n0 = self.getNode(connection[0])
                n1 = self.getNode(connection[1])
                # simple word modules may not connect to each other
                if n0.word and n1.word:
                    return False
                # vertices with the same link may not connect
                if n0.getSharedLinks(n1, self):
                    return False
                connection = list(connection)
                newGraph.connectNodes(connection[0], connection[1])

        # return the new graph if it has the words in the right order and the conclusion is correct
        try:
            if newGraph.hasCorrectWordOrder(sentence) and newGraph.hasCorrectConclusion(targetType):
                return newGraph
        except:
            return False
        return False

    # get a list of all possible unary contractions in the graph
    def getPossibleUnaryContractions(self):
        contractions = []
        for vertex in self.getVertices():
            if vertex.getVertexType(self) == VertexType.Conclusion:
                continue
            upperLink = self.getNode(self.getChildren(vertex.nodeId)[0])
            if upperLink.mode is LinkMode.Unary:
                contraction = self.contractUnary(vertex, upperLink)
                if contraction:
                    contractions.append(contraction)

        return contractions

    # verify if a linknode points to a vertex as the main vertex
    def check_if_link_has_vertex_as_main(self, linknode, vertex_id):
        adj = self.graph.adj[linknode.nodeId]
        # for each edge check if the neighbour is the inbetween vertex
        for neighbourid, edge_dict in adj.items():
            if neighbourid == vertex_id:
                main_edge_id = edge_dict['main_edge']

                # and check of the edge the main edge is
                if main_edge_id is not None and main_edge_id == vertex_id:
                    return True
        return False

    # Apply a unary contraction at vertex and return resulting graph. return none if impossible.
    def contractUnary(self, vertex, upperLink):

        in_between_vertex_id = self.getChildren(upperLink.nodeId)[0]

        try:
            downLink = self.getNode(self.getChildren(in_between_vertex_id)[0])
        except:
            return None

        if downLink.mode is LinkMode.Binary:
            return None

        # the links must be a different type
        if upperLink.type == downLink.type:
            return None

        # if a linknode is par check of the main vertex is not the in between the link nodes
        if upperLink.type == LinkType.Par:
            # in between vertex is main -> don't contract
            if self.check_if_link_has_vertex_as_main(upperLink, in_between_vertex_id):
                return None

        if downLink.type == LinkType.Par:
            # in between vertex is main -> don't contract
            if self.check_if_link_has_vertex_as_main(downLink, in_between_vertex_id):
                return None

        sharedVertices = upperLink.getSharedVertices(downLink, self)
        if len(sharedVertices) != 1:
            return None
        # the shared vertices may not include the hypothesis
        if vertex.nodeId in sharedVertices:
            return None

        # the conclusion is the child of the remaining link that is not in shared vertices
        conclusion_id = [v for v in self.getChildren(downLink.nodeId) if v not in sharedVertices][0]
        conclusion = self.graph.nodes[conclusion_id]['node']

        if upperLink.type == LinkType.Par:
            # if upper link is par and hypotheses is not main don't contract
            if not self.check_if_link_has_vertex_as_main(upperLink, vertex.nodeId):
                return None

        if downLink.type == LinkType.Par:
            if not self.check_if_link_has_vertex_as_main(downLink, conclusion_id):
                return None

        # remove the two links and the shared vertices
        newGraph = self.copy()
        newGraph.parentGraph = self

        newGraph.graph.remove_node(upperLink)
        newGraph.graph.remove_node(downLink)
        newGraph.graph.remove_nodes_from(sharedVertices)

        newGraph.joinVertices(vertex, conclusion)

        return newGraph

    # Apply a binary contraction at vertex at vertex and return resulting graph. return none if impossible.
    def contractBinary(self, vertex, upperLink):
        try:
            downLink = self.getNode(self.getChildren(self.getChildren(upperLink.nodeId)[0])[0])
        except:
            return None
        # the links must be a different type
        if upperLink.type == downLink.type:
            return None
        # the links must be a different shape
        if upperLink.getLinkShape(self) == downLink.getLinkShape(self):
            return None
        # the links must share two vertices
        sharedVertices = upperLink.getSharedVertices(downLink, self)
        if len(sharedVertices) is not 2:
            return None
        # the shared vertices may not include the hypothesis
        if vertex.nodeId in sharedVertices:
            return None

        # the conclusion is the child of the remaining link that is not in shared vertices
        conclusion_id = [v for v in self.getChildren(downLink.nodeId) if v not in sharedVertices][0]
        conclusion = self.graph.nodes[conclusion_id]['node']

        # remove the two links and the shared vertices
        newGraph = self.copy()
        newGraph.parentGraph = self

        newGraph.graph.remove_node(upperLink)
        newGraph.graph.remove_node(downLink)
        newGraph.graph.remove_nodes_from(sharedVertices)

        newGraph.joinVertices(vertex, conclusion)

        return newGraph

    # Apply a structural rewrite at link and return resulting graph. return none if impossible.
    def rewrite(self, upperLink):
        # the upper link is unary and a tensor
        if upperLink.mode is not LinkMode.Unary or upperLink.type is not LinkType.Tensor:
            return False
        # try to get the descendants of upper link. could fail if too close to a conclusion vertex
        try:
            # the middle link is binary, pointing down, a tensor and the grandchild of upper link
            middleLink = self.getNode(self.getChildren(self.getChildren(upperLink.nodeId)[0])[0])
            if middleLink.mode is not LinkMode.Binary or middleLink.getLinkShape(self) is not LinkShape.Downward:
                return False
            # the lower link is binary, pointing down, a tensor and the grandchild of middle link
            lowerLink = self.getNode(self.getChildren(self.getChildren(middleLink.nodeId)[0])[0])
            if lowerLink.mode is not LinkMode.Binary or lowerLink.getLinkShape(self) is not LinkShape.Downward:
                return False
        except Exception as e:
            return False

        newGraph = self.copy()
        newGraph.parentGraph = self

        sharedUpperMiddle = upperLink.getSharedVertices(middleLink, newGraph)
        sharedMiddleLower = middleLink.getSharedVertices(lowerLink, newGraph)
        # h1 is the parent of the lower link that is not shared with the middle link
        h1 = newGraph.getNode([v for v in newGraph.getParents(lowerLink.nodeId) if v not in sharedMiddleLower][0])
        # h2 is the parent of the middle link that is not shared with upper link
        h2 = newGraph.getNode([v for v in newGraph.getParents(middleLink.nodeId) if v not in sharedUpperMiddle][0])
        # h3 is the parent of the upper link
        h3 = newGraph.getNode(newGraph.getParents(upperLink.nodeId)[0])
        # h4 is the child of the upper link
        h4 = newGraph.getNode(newGraph.getChildren(upperLink.nodeId)[0])
        # h5 is the shared vertex between the lower link and the middle link
        h5 = newGraph.getNode(sharedMiddleLower[0])

        # rewrite the graph
        newGraph.graph.remove_edge(lowerLink.nodeId, h1.nodeId)
        newGraph.graph.remove_edge(lowerLink.nodeId, h5.nodeId)
        newGraph.graph.remove_edge(middleLink.nodeId, h2.nodeId)
        newGraph.graph.remove_edge(middleLink.nodeId, h4.nodeId)
        newGraph.graph.remove_edge(middleLink.nodeId, h5.nodeId)
        newGraph.graph.remove_edge(upperLink.nodeId, h3.nodeId)
        newGraph.graph.remove_edge(upperLink.nodeId, h4.nodeId)

        newGraph.addEdge(lowerLink, h4, alignment=EdgeAlignment.Right)
        newGraph.addEdge(lowerLink, h5, alignment=EdgeAlignment.Left)
        newGraph.addEdge(middleLink, h1, alignment=EdgeAlignment.Left)
        newGraph.addEdge(middleLink, h2, alignment=EdgeAlignment.Right)
        newGraph.addEdge(h5, middleLink, alignment=EdgeAlignment.Straight)
        newGraph.addEdge(upperLink, h3, alignment=EdgeAlignment.Straight)
        newGraph.addEdge(h4, upperLink, alignment=EdgeAlignment.Straight)

        return newGraph

    # get the size of a graph
    def node_count(self):
        return len(dict(self.graph.nodes()).values())


    # acyclic, connected, without cotensor links
    # note: earlier steps in our program already ensure the resulting graph is connected
    def isTensorTree(self):
        for link in self.getLinks():
            if link.type is LinkType.Par:
                return False
        try:
            nx.find_cycle(self.graph, 'ignore')
            return False
        except:
            return True

    # return all vertices that are leaves
    def getLeaves(self):
        leaves = []
        for v in dict(self.graph.nodes()).values():
            node = v['node']
            if(type(node) is LoLaVertex) and node.getVertexType(self) is not VertexType.NotALeaf:
                leaves.append(node)
        return leaves

    # add a node to the graph (index = nodeId)
    def addNode(self, node):
        self.graph.add_node(node.nodeId, node=node)
        return node

    # add an edge to the graph (either pass id's or objects)
    # parentage means higher up in the graph, or premisism
    def addEdge(self, child=None, parent=None, child_id=None, parent_id=None, alignment=None, main_edge=None):
        if child is not None and parent is not None:
            self.graph.add_edge(child.nodeId, parent.nodeId, parent=parent.nodeId, alignment=alignment, main_edge=main_edge)

        if child_id is not None and parent_id is not None:
            self.graph.add_edge(child_id, parent_id, parent=parent, alignment=alignment, main_edge=main_edge)

    # return the node from the graph with corresponding nodeId
    def getNode(self, nodeId):
        return self.graph.nodes()[nodeId]['node']

    # connect two nodes
    def connectNodes(self, node, otherNode):

        # restore node properties
        if node.word or node.from_target_type:
            otherNode.word = node.word
            otherNode.is_sequent_root = node.is_sequent_root
            otherNode.from_target_type = node.from_target_type

        # restore edge properties
        try:
            adj = self.graph.adj[node]
        except:
            return

        for neighborId, edge in adj.items():
            parentId = edge['parent']
            alignment = edge['alignment']
            main_edge_id = edge['main_edge']
            if main_edge_id is not None and main_edge_id == node.nodeId:
                main_edge_id = otherNode.nodeId

            if parentId == node.nodeId:
                parentId = otherNode.nodeId
            self.graph.add_edge(otherNode.nodeId, neighborId, parent=parentId, alignment=alignment, main_edge=main_edge_id)

        self.graph.remove_node(node.nodeId)

    # combine two vertices into one (after contraction)
    def joinVertices(self, node, otherNode):

        try:
            adj = self.graph.adj[node.nodeId]
        except:
            pass

        self.graph.remove_node(node.nodeId)
        for neighborId, edge in adj.items():
            parentId = edge['parent']
            alignment = edge['alignment']
            main_edge_id = edge['main_edge']
            if main_edge_id is not None and main_edge_id == node.id:
                main_edge_id = otherNode.nodeId
            if parentId is node.nodeId:
                parentId = otherNode.nodeId
            self.graph.add_edge(otherNode.nodeId, neighborId, parent=parentId, alignment=alignment, main_edge=main_edge_id)

    # unfold a graph until all complex types are reduced to simple sequents at the leaves
    def unfold_graph(self):
        all_nodes_unfolded = True

        for v in dict(self.graph.nodes()).values():
            node = v['node']

            if (type(node) is LoLaVertex) and not node.is_unfolded:
                all_nodes_unfolded = False

                new_lola_graph = node.unfoldVertex(self, unfoldVertex, LoLaGraph())

                if new_lola_graph is not None:
                    self.graph = nx.compose(self.graph, new_lola_graph.graph)

        if all_nodes_unfolded:
            return self

        return self.unfold_graph()

    # get the parents of a node
    def getParents(self, nodeId):
        adj = self.graph.adj[nodeId]
        parents = []
        for k, v in dict(adj).items():
            if v['parent'] is not nodeId:
                parents.append(k)
        return parents

    # get the children of a node
    def getChildren(self, nodeId: int):
        adj = self.graph.adj[nodeId]
        children = []
        for k, v in dict(adj).items():
            if v['parent'] is nodeId:
                children.append(k)
        return children

    # get the parents and the children of a node
    def getNeighbors(self, nodeId):
        return self.getParents(nodeId) + self.getChildren(nodeId)

    # get all vertices in the graph
    def getVertices(self):
        return [self.getNode(v) for v in self.graph.nodes() if type(self.getNode(v)) is LoLaVertex]

    # get all vertices in the graph that are a premise (have no parent link)
    def getPremises(self):
        return [v for v in self.getVertices() if v.getVertexType(self) is VertexType.Premise]

    # get all vertices in the graph that are a conclusion (have no children link)
    def getConclusions(self):
        return [v for v in self.getVertices() if v.getVertexType(self) is VertexType.Conclusion]

    # get all links in the graph
    def getLinks(self):
        return [self.getNode(v) for v in self.graph.nodes() if type(self.getNode(v)) is LoLaLinkNode]

    # draw the graph using the built-in networkX drawing function
    # TODO choose correct labels for final hand-in version
    def draw(self):
        # build color list and label dictionary
        colors = []
        labels = {}

        for k, v in dict(self.graph.nodes()).items():
            node = v['node']
            colors.append(node.getColor(self))
            if type(node) is LoLaVertex:
                if node.word:
                    labels[node.nodeId] = str(node.nodeId) + " " + node.word
                else:
                    labels[node.nodeId] = str(node.nodeId)
                if node.axiom_link is not None:
                    labels[node.nodeId] = labels[node.nodeId] + '  ' + node.axiom_link[0].value + " " + node.axiom_link[1].value
            else:
                labels[node.nodeId] = ""# str(node.nodeId)

        # draw the graph
        nx.draw(self.graph, show_labels=True, labels=labels, node_color=colors, node_size=150, font_size=8)
        plt.show()
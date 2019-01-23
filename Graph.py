from LoLaLinkNode import *
import networkx as nx
import itertools
import matplotlib.pyplot as plt
from unfold_vertex_functions import unfoldVertex
from NodeFactory import *
from LoLaDatatypes import *

class LoLaGraph:


    def __init__(self, parent_graph=None):
        self.parentGraph = parent_graph
        self.graph = nx.Graph()

    def __eq__(self, other):
        return nx.is_isomorphic(self.graph, other.graph)

    def __hash__(self):
        return hash(tuple(sorted(self.graph.degree())))

    def get_deep_parent(self):
        tmp_graph = self.parentGraph

        if tmp_graph is None:
            return self
        return tmp_graph.get_deep_parent()

    # returns a fresh graph
    def copy(self):
        newLoLaGraph = LoLaGraph(self.parentGraph)
        newGraph = self.graph.copy()
        ding = dict(newGraph.nodes())
        for k, v in ding.items():
            v['node'] = v['node'].copy(newLoLaGraph)
        newLoLaGraph.graph = newGraph
        return newLoLaGraph

    # Get the words in a graph from left to right
    def getOrderedPremises(self):
        # DFS starting at conclusion, traversing left-first
        stack = [self.getConclusions()[0]]
        discovered = set()
        premises = []
        while stack:
            node = stack.pop()
            if node not in discovered:
                discovered.add(node)
                adj = self.graph.adj[node.nodeId]
                # if adj has edge where edge.alignment is EdgeAlignment.Right
                # append node
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

                if type(node) is LoLaVertex and node.getVertexType(self) is VertexType.Premise:
                    premises.append(node)

        return premises

    # Check if the word order in the graph corresponds to the input sentence
    def hasCorrectWordOrder(self, sentence):
        premiseOrder = list(map(lambda x: x.word, self.getOrderedPremises()))
        return sentence.lower() == " ".join(premiseOrder)

    def hasCorrectConclusion(self, conclusion):
        return len(self.getConclusions()) == 1 and self.getConclusions()[0].sequent == conclusion

    # connect a graph according to the connection map and check if sentence and target type are correct
    def connectFeest(self, connectionMap, sentence, targetType):
        newGraph = self.copy()  # graph.copy()

        for connectionType in connectionMap:
            for connection in connectionType:
                connection = list(connection)
                newGraph.updateNodeFeest(connection[0], connection[1])

        try:
            if newGraph.hasCorrectWordOrder(sentence) and newGraph.hasCorrectConclusion(targetType):
                return newGraph
        except:
            return False
        return False


    # return list of new graphs that can be created from connecting with otherGraph
    def getPossibleConnections(self, otherGraph):

        # get the leaves from both graphs
        leaves = [leaf for leaf in self.getLeaves()]
        otherLeaves = [leaf for leaf in otherGraph.getLeaves()]

        # build a list for each leaf in this graph for which leaves in the other graph it can connect with
        candidatesConnections = []
        for leaf in leaves:

            opposingLeaves = [otherLeaf for otherLeaf in otherLeaves
             if otherLeaf.getVertexType(otherGraph) == VertexType.OppositeLeafType(leaf.getVertexType(self))
             and leaf.sequent == otherLeaf.sequent]

            candidatesConnections.append(opposingLeaves + [None])

        # a connectionMap tells each vertex which vertex in the other graph to connect with
        candidatesConnections = list(itertools.product(*candidatesConnections))[:-1]
        connectionMaps = []
        # if a connectionMap points to the same vertex twice, it is invalid
        for connectionMap in candidatesConnections:
            seen = set()
            duplicate = False
            for vertex in connectionMap:
                if vertex in seen:
                    duplicate = True
                    break
                if vertex is not None:
                    seen.add(vertex)
            if not duplicate:
                connectionMaps.append(connectionMap)

        connectionMaps = list(map(lambda x: list(zip(leaves, x)), connectionMaps))

        newGraphs = []
        for connectionMap in connectionMaps:
            newGraph = self.connect(otherGraph, connectionMap)
            if newGraph:
                newGraphs.append(newGraph)

        return newGraphs

    # connect two graphs
    # return new graph if connectionMap is exactly possible
    # else return None
    def connect(self, otherGraph, connectionMap):

        for connection in connectionMap:
            # if the leave will not connect, connection[1] is None
            if connection[1] is None:
                continue
            v1 = self.getNode(connection[0])
            v2 = otherGraph.getNode(connection[1])
            # if you are a sequent root, only connect if you stay a premise
            if v1.is_sequent_root:
                if v1.from_target_type: # must stay a conclusion
                    if v2.getVertexType(otherGraph) != VertexType.Conclusion:
                        return None
                else: # must stay a premise
                    if v2.getVertexType(otherGraph) != VertexType.Premise:
                        return None
            if v2.is_sequent_root:
                if v2.from_target_type: # must stay a conclusion
                    if v1.getVertexType(self) != VertexType.Conclusion:
                        return None
                else: # must stay a premise
                    if v1.getVertexType(self) != VertexType.Premise:
                        return None
            # if v1.is_sequent_root and v2.getVertexType(otherGraph) != VertexType.Premise:
            #     return None
            # if v2.is_sequent_root and v1.getVertexType(self) != VertexType.Premise:
            #     return None
            if not v1.canConnect(v2, self, otherGraph):
                return None

        newGraph = self.copy()#graph.copy()

        for connection in connectionMap:
            if connection[1] is not None:
                newGraph.updateNode(connection[0].nodeId, connection[1].nodeId)

        newGraph.graph = nx.compose(newGraph.graph, otherGraph.copy().graph)
        # problem: compose takes properties from otherGraph. can lose word/is_sequent_root/from_target_type
        # restore properties
        for connection in connectionMap:
            if connection[0].is_sequent_root:
                if connection[1] is not None:
                    node = newGraph.getNode(connection[1].nodeId)
                    node.word = connection[0].word
                    node.is_sequent_root = connection[0].is_sequent_root
                    node.from_target_type = connection[0].from_target_type

        return newGraph

    # return list of new graphs that can be created from contracting
    def getPossibleContractions(self):
        contractions = []
        for vertex in self.getVertices():
            contraction = self.contract(vertex)
            if contraction:
                contractions.append(contraction)

        return contractions

    def contract(self, vertex):
        # first assert the H vertex is not a conclusion
        if vertex.getVertexType(self) == VertexType.Conclusion:
            return None
        # this is the upper of two links
        upperLink = self.getNode(self.getChildren(vertex.nodeId)[0])
        if upperLink.mode is LinkMode.Binary:
            return self.contractBinary(vertex, upperLink)
        else:
            return self.contractUnary(vertex, upperLink)

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

            # adj = self.graph.adj[upperLink.nodeId]
            # # for each edge check if the neighbour is the inbetween vertex
            # for neighbourid, edge_dict in adj.items():
            #     if neighbourid == in_between_vertex_id:
            #         main_edge_id = edge_dict['main_edge']
            #
            #         # and check of the edge the main edge is
            #         if main_edge_id is not None and main_edge_id == in_between_vertex_id:
            #             return None

        if downLink.type == LinkType.Par:
            # in between vertex is main -> don't contract
            if self.check_if_link_has_vertex_as_main(downLink, in_between_vertex_id):
                return None

            # adj = self.graph.adj[downLink.nodeId]
            # # for each edge check if the neighbour is the inbetween vertex
            # for neighbourid, edge_dict in adj.items():
            #     if neighbourid == in_between_vertex_id:
            #         main_edge_id = edge_dict['main_edge']
            #
            #         # and check of the edge the main edge is
            #         if main_edge_id is not None and main_edge_id == in_between_vertex_id:
            #             return None

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

    # Contract a graph at vertex and return resulting graph. return none if impossible.
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

    # return list of new graphs that can be created from rewriting
    def getPossibleRewritings(self):
        rewritings = []
        for link in self.getLinks():
            rewriting = self.rewrite(link)
            if rewriting:
                rewritings.append(rewriting)

        return rewritings


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

    # # Rewrite a graph at vertex and return resulting graph. return none if impossible.
    # def rewrite(self, link):
    #     # NOTE: contractions only happen to tensor links connected as > · <
    #     if link.type is LinkType.Par:
    #         return False
    #     if link.getLinkShape(self) is LinkShape.Upward:
    #         return False
    #     if self.getNode(self.getChildren(link.nodeId)[0]).getVertexType(self) is VertexType.Conclusion:
    #         return False
    #
    #     otherLink = self.getNode(self.getChildren(self.getChildren(link.nodeId)[0])[0])
    #
    #     if otherLink.type is LinkType.Par:
    #         return False
    #     if otherLink.getLinkShape(self) is LinkShape.Downward:
    #         return False
    #
    #     # We are now certain that we are dealing with > · < tensor links
    #     # There are 4 possible structural rewrites
    #     # in each rewrite, the tensor changes shape
    #
    #     x, y = self.getParents(link.nodeId)
    #     u = link.getSharedVertices(otherLink, self)[0]
    #     v, w = self.getChildren(otherLink.nodeId)
    #
    #     return [self.applyStructuralRule(link, otherLink, x, y, u, v, w, 0),
    #             self.applyStructuralRule(link, otherLink, x, y, u, v, w, 1),
    #             self.applyStructuralRule(link, otherLink, x, y, u, v, w, 2),
    #             self.applyStructuralRule(link, otherLink, x, y, u, v, w, 3)]
    #
    # # apply structural rule to rewrite graph
    # def applyStructuralRule(self, link, otherLink, x, y, u, v, w, rule):
    #     newGraph = self.copy()
    #     newGraph.graph.remove_node(link)
    #     newGraph.graph.remove_node(otherLink)
    #     newLink = newGraph.addNode(NODE_FACTORY.createLinkNode(self))
    #     newOtherLink = newGraph.addNode(NODE_FACTORY.createLinkNode(self))
    #     x = self.getNode(x)
    #     y = self.getNode(y)
    #     u = self.getNode(u)
    #     v = self.getNode(v)
    #     w = self.getNode(w)
    #
    #     if rule is 0:
    #         newGraph.addEdge(newLink, x)
    #         newGraph.addEdge(v, newLink)
    #         newGraph.addEdge(u, newLink)
    #         newGraph.addEdge(newOtherLink, u)
    #         newGraph.addEdge(newOtherLink, y)
    #         newGraph.addEdge(w, newOtherLink)
    #     elif rule is 1:
    #         newGraph.addEdge(newLink, x)
    #         newGraph.addEdge(v, newLink)
    #         newGraph.addEdge(newLink, u)
    #         newGraph.addEdge(u, newOtherLink)
    #         newGraph.addEdge(newOtherLink, y)
    #         newGraph.addEdge(w, newOtherLink)
    #     elif rule is 2:
    #         newGraph.addEdge(newLink, x)
    #         newGraph.addEdge(u, newLink)
    #         newGraph.addEdge(w, newLink)
    #         newGraph.addEdge(newOtherLink, u)
    #         newGraph.addEdge(newOtherLink, y)
    #         newGraph.addEdge(v, newOtherLink)
    #     elif rule is 3:
    #         newGraph.addEdge(newLink, y)
    #         newGraph.addEdge(v, newLink)
    #         newGraph.addEdge(u, newLink)
    #         newGraph.addEdge(newOtherLink, x)
    #         newGraph.addEdge(newOtherLink, u)
    #         newGraph.addEdge(w, newOtherLink)
    #     return newGraph

    def node_count(self):
        return len(dict(self.graph.nodes()).values())


    # acyclic, connected, without cotensor links
    def isTensorTree(self):
        if not nx.is_connected(self.graph):
            return False
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

    def addEdge(self, child=None, parent=None, child_id=None, parent_id=None, alignment=None, main_edge=None):
        if child is not None and parent is not None:
            self.graph.add_edge(child.nodeId, parent.nodeId, parent=parent.nodeId, alignment=alignment, main_edge=main_edge)

        if child_id is not None and parent_id is not None:
            self.graph.add_edge(child_id, parent_id, parent=parent, alignment=alignment, main_edge=main_edge)

    # return the node from the graph with nodeId
    def getNode(self, nodeId):
        return self.graph.nodes()[nodeId]['node']


    def updateNodeFeest(self, node, otherNode):

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

    # Update the nodeId to newId
    def updateNode(self, nodeId, newId):
        # get the node from the graph we wish to update
        node = self.getNode(nodeId)
        newNode = self.graph.add_node(newId, node=self.getNode(nodeId))
        self.getNode(newId).nodeId = newId
        # remove the node from the graph
        self.graph.remove_node(nodeId)
        # restore the edges
        try:
            adj = self.graph.adj[nodeId]
        except:
            return
        for neighborId, edge in adj.items():
            parentId = edge['parent']
            alignment = edge['alignment']
            main_edge_id = edge['main_edge']
            if main_edge_id is not None and main_edge_id == nodeId:
                main_edge_id = newId

            if parentId == nodeId:
                parentId = newId
            self.graph.add_edge(newId, neighborId, parent=parentId, alignment=alignment, main_edge=main_edge_id)

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

        ####

        #
        # # get the adj of the node
        # nodeAdj = self.graph.adj[node]
        # # get the adj of the otherNode
        # otherNodeAdj = self.graph.adj[otherNode]
        # # create the union of both nodes
        # joinedNode = self.addNode(NODE_FACTORY.createVertex(self, otherNode.sequent))
        # joinedNode.from_target_type = otherNode.from_target_type
        # joinedNode.is_sequent_root = otherNode.is_sequent_root
        # # remove the nodes from the graph
        # self.graph.remove_node(node)
        # self.graph.remove_node(otherNode)
        # # restore the edges
        # for neighborId, v in nodeAdj.items():
        #     parentId = v['parent']
        #     alignment = v['alignment']
        #     main_edge_id = v['main_edge']
        #     if main_edge_id is not None and main_edge_id == node:
        #         main_edge_id = joinedNode.nodeId
        #     if parentId is node:
        #         parentId = joinedNode.nodeId
        #     self.graph.add_edge(joinedNode.nodeId, neighborId, parent=parentId, alignment=alignment, main_edge=main_edge_id)
        # for neighborId, v in otherNodeAdj.items():
        #     parentId = v['parent']
        #     alignment = v['alignment']
        #     main_edge_id = v['main_edge']
        #     if main_edge_id is not None and main_edge_id == node:
        #         main_edge_id = joinedNode.nodeId
        #     if parentId is otherNode:
        #         parentId = joinedNode.nodeId
        #     self.graph.add_edge(joinedNode.nodeId, neighborId, parent=parentId, alignment=alignment, main_edge=main_edge_id)

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

    def getPremises(self):
        return [v for v in self.getVertices() if v.getVertexType(self) is VertexType.Premise]

    def getConclusions(self):
        return [v for v in self.getVertices() if v.getVertexType(self) is VertexType.Conclusion]

    def getLinks(self):
        return [self.getNode(v) for v in self.graph.nodes() if type(self.getNode(v)) is LoLaLinkNode]

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
                    labels[node.nodeId] = str(node.nodeId)#""#str(node.nodeId) + " " + node.sequent
                if node.axiom_link is not None:
                    labels[node.nodeId] = labels[node.nodeId] + '  ' + node.axiom_link[0].value + " "+ node.axiom_link[1].value
            else:
                labels[node.nodeId] = ""# str(node.nodeId)

        # draw the graph
        nx.draw(self.graph, show_labels=True, labels=labels, node_color=colors, node_size=150, font_size=8)
        plt.show()

def all_combinations(any_list):
    return itertools.chain.from_iterable(
        itertools.combinations(any_list, i + 1)
        for i in range(len(any_list)))


from LoLaLinkNode import LoLaLinkNode, LoLaVertex
from LoLaDatatypes import *
from SequentParser import SequentType

def expand_subset(lola_graph, subset):
    subsets = get_subsets(lola_graph)
    return [s for s in subsets if subset[0] in s][0]

def get_subsets(lola_graph):
    discovered = set()
    subnets = []
    links_left = set([x for x in lola_graph.getLinks() if x.type is not LinkType.Par])
    links_visited = set()
    stack = [list(links_left)[0]]

    while links_left:
        current_subnet = []
        while stack:
            node = stack.pop()
            if node not in discovered:
                discovered.add(node)
                lola_node = node
                if type(lola_node) is LoLaLinkNode:
                    current_subnet.append(node)
                    links_visited.add(node)
                    links_left.remove(node)
                neighbors = list(lola_graph.graph.adj[node])
                for neighbor in neighbors:
                    if len(current_subnet) > 0 and (type(lola_node) is LoLaVertex and lola_node.axiom_link is not None):
                        continue
                    poep = lola_graph.getNode(neighbor)
                    if type(poep) is LoLaLinkNode and poep.type is LinkType.Par:
                        continue
                    stack.append(poep)
        subnets.append(current_subnet)
        if links_left:
            stack.append(list(links_left)[0])

    return subnets

def get_lowest_vertex(graph, subnet):
    lowest = subnet[0]

    # subset heeft alleen maar tensor dus altijd children
    children = graph.getChildren(lowest.nodeId)

    while len(children) > 0:

        vertex = children[0]

        vertex_children = graph.getChildren(vertex)

        # als vertex leaf is dan is conclusie van graph
        if len(vertex_children) == 0:
            return graph.getNode(vertex)

        child_link_node =  graph.getNode(vertex_children[0])

        # als child link node niet in subset dan return the tussen vertex
        if child_link_node not in subnet:
            return graph.getNode(vertex)

        children = graph.getChildren(child_link_node.nodeId)


def crawl_axiom_graph(lola_graph, subset, visited=None, lowest=None):
    if lowest is None:
        lowest = get_lowest_vertex(lola_graph, subset)
    if visited is None:
        visited = set()
    current = lowest
    while True:
        if type(current) is LoLaVertex:
            parents = lola_graph.getParents(current.nodeId)
            if parents:
                parent = parents[0]
                if parent in subset:
                    current = lola_graph.getParents(current.nodeId)[0]
                else:
                    break
            else:
                break
        else:
            adj = lola_graph.graph.adj[current]
            for k, v in adj.items():
                if v['main_edge']:
                    if k not in visited:
                        current = lola_graph.getNode(k)
                    else:
                        current = [p for p in lola_graph.getParents(current.nodeId) if p is not v][0]
                    break
            for p in lola_graph.getParents(current):
                visited.add(p)

    red_arrows = []
    blue_arrows = []

    vertices_in_subset = []
    for link in subset:
        neighbors = list(lola_graph.graph.adj[link.nodeId])
        for neighbor in neighbors:
            vertices_in_subset.append(lola_graph.getNode(neighbor))

    for v in vertices_in_subset:
        if v == lola_graph.getConclusions()[0]:
            continue
        if v.axiom_link:
            if v.axiom_link[0] is AxiomLinkType.Blue:
                blue_arrows.append(v)
            if v.axiom_link[0] is AxiomLinkType.Red:
                red_arrows.append(v)

    # remove a red arrow (can be multiple: diverge)
    # -> build corresponding term
    # also remove a blue arrow (can multiple: diverge

    for red in red_arrows:
        for blue in blue_arrows:
            # TODO build term here
            # remove a combination of red and blue arrows in the subset
            newGraph = lola_graph.copy()
            newGraph.getNode(red).axiom_link = None
            newGraph.getNode(blue).axiom_link = None
            expanded_subset = expand_subset(newGraph, subset)
            crawl_axiom_graph(newGraph, expanded_subset, visited, blue)

def check_if_link_has_vertex_with(lola_graph, linknode_id , axiom_link_type):
    adj = lola_graph.graph.adj[linknode_id]
    # for each edge check if the neighbour is the inbetween vertex
    for neighbourid, edge_dict in adj.items():

        neighbour = lola_graph.getNode(neighbourid)

        if neighbour.axiom_link is None:
            return False

        if neighbourid == linknode_id:
            main_edge_id = edge_dict['main_edge']

            # and check of the edge the main edge is
            if main_edge_id is not None and main_edge_id == linknode_id:
                return True
    return False


class VariableManager():
    def __init__(self):
        self.dict = {}

        self.count = 0

        self.wordList = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    def get_variable_from_node_id(self,node_id):
        if node_id in self.dict:
            return self.dict[node_id]

        if self.count< 26:
            self.dict[node_id] = self.wordList[self.count]
        else:
            self.dict[node_id] = self.count

        self.count = self.count + 1

        return self.dict[node_id]


    def set_variable(self, node_id, value):
        self.dict[node_id] = value


def left_forwardslash_term(variable_manager, term_till_now , link_node, lola_graph):

    vertex_a = lola_graph.getNode(lola_graph.getChildren(link_node.nodeId)[0])
    vertex_z = None
    vertex_b = None

    adj = lola_graph.graph.adj[link_node.nodeId]
    for k, v in adj.items():
        if v['main_edge']:
            vertex_z = lola_graph.getNode( v['main_edge'])

        if k != vertex_a.nodeId:
            vertex_b = lola_graph.getNode(k)

    term = f'( {variable_manager.get_variable_from_node_id(vertex_a.nodeId)} / {variable_manager.get_variable_from_node_id(vertex_b.nodeId)} )'

    variable_manager.set_variable(vertex_z, term)

    return term


def left_backwardlash_term(variable_manager, term_till_now , link_node, lola_graph):

    vertex_a = lola_graph.getNode(lola_graph.getChildren(link_node.nodeId)[0])
    vertex_z = None
    vertex_b = None

    adj = lola_graph.graph.adj[link_node.nodeId]
    for k, v in adj.items():
        if v['main_edge']:
            vertex_z = lola_graph.getNode( v['main_edge'])

        if k != vertex_a.nodeId:
            vertex_b = lola_graph.getNode(k)

    term = f'( {variable_manager.get_variable_from_node_id(vertex_b.nodeId)} \ {variable_manager.get_variable_from_node_id(vertex_a.nodeId)} )'

    variable_manager.set_variable(vertex_z, term)

    return term


link_to_term_functions = {
    (True, SequentType.ForwardSlash): '',
    (True, SequentType.Tensor): '',
    (True, SequentType.BackwardSlash): '',
    (False, SequentType.ForwardSlash): '',
    (False, SequentType.Tensor): '',
    (False, SequentType.BackwardSlash): '',
}





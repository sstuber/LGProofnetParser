from SequentParser import ParseSequent, SequentType
from LoLaDatatypes import AxiomLinkType, AxiomLinkDirection
from LoLaLinkNode import LoLaVertex

blue_parent_no_tentacle = [(True, SequentType.ForwardSlash), (True, SequentType.BackwardSlash)]
# main node is current vertex
blue_parent_tentacle = [(False, SequentType.ForwardSlash),(False, SequentType.BackwardSlash)]

blue_child_no_tentacle = [(True, SequentType.Tensor), (False, SequentType.Tensor)]
# main node not current vertex
blue_child_tentacle = [(True, SequentType.ForwardSlash), (True, SequentType.BackwardSlash)]


red_parent_no_tentacle = [(True, SequentType.Tensor), (False, SequentType.Tensor)]
# main node not current vertex
red_parent_tentacle = [(False, SequentType.ForwardSlash), (False, SequentType.BackwardSlash)]

red_child_no_tentacle = [(False, SequentType.ForwardSlash), (False, SequentType.BackwardSlash)]
# main node is current vertex
red_child_tentacle = [(True, SequentType.ForwardSlash), (True, SequentType.BackwardSlash)]


def transform_to_axiom_graph(lola_graph, bias_map):

    nx_graph_dict_values = dict(lola_graph.graph.nodes()).values()

    lola_nodes = list(map(lambda nx_dict: nx_dict['node'], nx_graph_dict_values))
    lola_vertices = list(filter(lambda lola_node: type(lola_node) is LoLaVertex , lola_nodes))

    for vertex in lola_vertices:
        axiom_link_type = get_axiom_link_of_vertex(lola_graph, vertex)
        vertex_bias = get_polarity_from_sequent(vertex.sequent, bias_map)

        axiom_direction = transform_bias_into_direction(vertex_bias,axiom_link_type)
        if axiom_link_type is not None:
            vertex.axiom_link = (axiom_link_type, axiom_direction)
        print(vertex.axiom_link)

    return lola_graph

def get_axiom_link_of_vertex(graph, vertex):

    parent_nodes = graph.getParents(vertex.nodeId)
    children_nodes = graph.getChildren(vertex.nodeId)

    if len(parent_nodes) == 0:
        child_link_node = graph.getNode(children_nodes[0])
        child_pre_info = child_link_node.get_pre_arrow_tuple()

        is_main_of_child = check_if_link_has_vertex_as_main(graph, child_link_node, vertex.nodeId)

        if child_pre_info in red_child_no_tentacle or (child_pre_info in red_child_tentacle and is_main_of_child):
            print(' red candidate')
            if vertex.is_sequent_root:
                return AxiomLinkType.Red

        print('isPremise')
        return None

    if len(children_nodes) == 0:
        parent_link_node = graph.getNode(parent_nodes[0])
        parent_pre_info = parent_link_node.get_pre_arrow_tuple()
        is_main_of_parent = check_if_link_has_vertex_as_main(graph, parent_link_node, vertex.nodeId)

        if parent_pre_info in blue_parent_no_tentacle or (
                parent_pre_info in blue_parent_no_tentacle and is_main_of_parent):
            return AxiomLinkType.Blue

        print('isConclusion')
        return None

    parent_link_node = graph.getNode(parent_nodes[0])
    parent_pre_info = parent_link_node.get_pre_arrow_tuple()
    child_link_node = graph.getNode(children_nodes[0])
    child_pre_info = child_link_node.get_pre_arrow_tuple()

    is_main_of_parent = check_if_link_has_vertex_as_main(graph,parent_link_node,vertex.nodeId)
    is_main_of_child = check_if_link_has_vertex_as_main(graph, child_link_node, vertex.nodeId)

    if parent_pre_info in blue_parent_no_tentacle or (parent_pre_info in blue_parent_no_tentacle and is_main_of_parent):
        if child_pre_info in blue_child_no_tentacle or (child_pre_info in blue_child_tentacle and not is_main_of_child):
            # check if child is is candidate
            print('blue candidate')
            return AxiomLinkType.Blue

    if parent_pre_info in red_parent_no_tentacle or (parent_pre_info in red_parent_tentacle and not is_main_of_parent):
        if child_pre_info in red_child_no_tentacle or (child_pre_info in red_child_tentacle and is_main_of_child):
            print(' red candidate')
            return AxiomLinkType.Red

    return None


def check_if_link_has_vertex_as_main(lola_graph, linknode, vertex_id):
    adj = lola_graph.graph.adj[linknode.nodeId]
    # for each edge check if the neighbour is the inbetween vertex
    for neighbourid, edge_dict in adj.items():
        if neighbourid == vertex_id:
            main_edge_id = edge_dict['main_edge']

            # and check of the edge the main edge is
            if main_edge_id is not None and main_edge_id == vertex_id:
                return True
    return False


bias = {
    's': False,
    'np': False,
    'n': False
}

def transform_bias_into_direction(bias, AxiomLink):
    if AxiomLink is None:
        return None

    if AxiomLink is AxiomLinkType.Blue:
        if bias:
            return AxiomLinkDirection.Up
        return AxiomLinkDirection.Down
    # is red
    if bias:
        return AxiomLinkDirection.Down
    return AxiomLinkDirection.Up


def get_polarity_from_sequent(sequent, bias_map=bias):

    sequent_type, string_array = ParseSequent(sequent)

    if sequent_type is SequentType.SingleWord:
        return bias_map[string_array[0]]

    if sequent_type is SequentType.ForwardSlash or sequent_type is SequentType.BackwardSlash:
        return False

    if sequent_type is SequentType.Tensor:
        return True

    return False


from SequentParser import ParseSequent, SequentType
from LoLaDatatypes import AxiomLinkType

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



def get_axiom_link_of_vertex(graph, vertex):

    parent_nodes = graph.getParents(vertex.nodeId)
    children_nodes = graph.getChildren(vertex.nodeId)

    if len(parent_nodes) == 0:

        print('isPremise')

    if len(children_nodes) == 0:
        print('isConclusion')

    parent_link_node = parent_nodes[0]
    parent_pre_info = parent_link_node.get_pre_arrow_tuple()
    child_link_node = children_nodes[0]
    child_pre_info = child_link_node.get_pre_arrow_tuple()

    is_main_of_parent = check_if_link_has_vertex_as_main(graph,parent_link_node,vertex.nodeId)
    is_main_of_child = check_if_link_has_vertex_as_main(graph, child_link_node, vertex.nodeId)

    if parent_pre_info in blue_parent_no_tentacle or (parent_pre_info in blue_parent_no_tentacle and is_main_of_parent):
        if child_pre_info in blue_child_no_tentacle or (child_pre_info in blue_child_tentacle and not is_main_of_child):
            # check if child is is candidate
            print('blue candidate')
            return AxiomLinkType.Blue

    if parent_pre_info in red_parent_no_tentacle or (parent_pre_info in red_parent_tentacle and not is_main_of_parent):
        if child_pre_info in red_child_no_tentacle or (parent_pre_info in red_child_tentacle and is_main_of_child):
            print(' red candidate')
            return AxiomLinkType.Red

    return None


def check_if_link_has_vertex_as_main(graph, linknode, vertex_id):
    adj = graph.adj[linknode.nodeId]
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


def get_polarity_from_sequent(sequent, bias_map=bias):


    sequent_type, string_array = ParseSequent(sequent)

    if sequent_type is SequentType.ForwardSlash or sequent_type is SequentType.BackwardSlash:
        return False

    if sequent_type is SequentType.Tensor:
        return True

    if sequent_type is SequentType.Diamond or SequentType.Square:
        return False

    return bias_map[string_array[0]]


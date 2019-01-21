
from LoLaDatatypes import LinkType, LinkMode, VertexType
from NodeFactory import NODE_FACTORY
from SequentParser import SequentType



combined_sequent_id = 0
a_sequent_id = 1
b_sequent_id = 2


def no_operation(main_vertex, string_array, graph):
    main_vertex.is_unfolded = True
    return None


def get_binary_nodes(graph, string_array):
    a_sequent = string_array[a_sequent_id]
    a_node = NODE_FACTORY.createVertex(graph, a_sequent)

    b_sequent = string_array[b_sequent_id]
    b_node = NODE_FACTORY.createVertex(graph, b_sequent)

    link_node = NODE_FACTORY.createLinkNode(graph)

    graph.addNode(a_node)
    graph.addNode(b_node)
    graph.addNode(link_node)

    return a_node, b_node, link_node


def get_unary_nodes(graph, string_array):
    a_sequent = string_array[a_sequent_id]
    a_node = NODE_FACTORY.createVertex(graph, a_sequent)

    link_node = NODE_FACTORY.createLinkNode(graph)
    link_node.mode = LinkMode.Unary

    graph.addNode(a_node)
    graph.addNode(link_node)

    return a_node, link_node


def unfold_single_word(vertex, string_array, graph):

    vertex.is_unfolded = True

    graph.addNode(vertex)
    vertex.is_unfolded = True
    return graph


def unfold_premise_tensor(main_vertex, string_array, graph):

    graph.addNode(main_vertex)

    a_node, b_node, link_node = get_binary_nodes(graph,string_array)

    link_node.main = main_vertex
    link_node.type = LinkType.Par

    graph.addEdge(a_node, link_node)
    graph.addEdge(link_node, main_vertex)
    graph.addEdge(link_node, b_node)

    main_vertex.is_unfolded = True
    return graph


def unfold_premise_forwardslash(main_vertex, string_array, graph):

    graph.addNode(main_vertex)

    a_node, b_node, link_node = get_binary_nodes(graph, string_array)

    link_node.main = main_vertex

    graph.addEdge(link_node, main_vertex)
    graph.addEdge(link_node,b_node)
    graph.addEdge(a_node,link_node)

    main_vertex.is_unfolded = True
    return graph


# since there is not yet a difference between right and left
def unfold_premise_backwardslash(main_vertex, string_array, graph):

    graph.addNode(main_vertex)

    a_node, b_node, link_node = get_binary_nodes(graph, string_array)

    link_node.main = main_vertex

    graph.addEdge(link_node, main_vertex)
    graph.addEdge(link_node, b_node)
    graph.addEdge(a_node, link_node)

    main_vertex.is_unfolded = True
    return graph


def unfold_premise_square(main_vertex, string_array, graph):

    graph.addNode(main_vertex)

    a_node, link_node = get_unary_nodes(graph,string_array)

    link_node.main = main_vertex

    graph.addEdge(link_node,main_vertex)
    graph.addEdge(a_node, link_node)

    main_vertex.is_unfolded = True
    return graph


def unfold_premise_diamond(main_vertex, string_array, graph):

    graph.addNode(main_vertex)

    a_node, link_node = get_unary_nodes(graph,string_array)

    link_node.main = main_vertex
    link_node.type = LinkType.Par

    graph.addEdge(link_node,main_vertex)
    graph.addEdge(a_node, link_node)

    main_vertex.is_unfolded = True
    return graph


def unfold_conclusion_forwardslash(main_vertex, string_array, graph):

    graph.addNode(main_vertex)

    a_node, b_node, link_node = get_binary_nodes(graph, string_array)

    link_node.main = main_vertex
    link_node.type = LinkType.Par

    graph.addEdge(link_node, a_node)
    graph.addEdge(b_node, link_node)
    graph.addEdge(main_vertex, link_node)

    main_vertex.is_unfolded = True
    return graph


def unfold_conclusion_tensor(main_vertex, string_array, graph):

    graph.addNode(main_vertex)

    a_node, b_node, link_node = get_binary_nodes(graph, string_array)

    link_node.main = main_vertex

    graph.addEdge(link_node, a_node)
    graph.addEdge(link_node, b_node)
    graph.addEdge(main_vertex, link_node)

    main_vertex.is_unfolded = True
    return graph


def unfold_conclusion_backwardslash(main_vertex, string_array, graph):

    graph.addNode(main_vertex)

    a_node, b_node, link_node = get_binary_nodes(graph, string_array)

    link_node.main = main_vertex
    link_node.type = LinkType.Par

    graph.addEdge(link_node, a_node)
    graph.addEdge(b_node, link_node)
    graph.addEdge(main_vertex, link_node)

    main_vertex.is_unfolded = True
    return graph


def unfold_conclusion_square(main_vertex, string_array, graph):

    graph.addNode(main_vertex)

    a_node, link_node = get_unary_nodes(graph,string_array)

    link_node.main = main_vertex
    link_node.type = LinkType.Par

    graph.addEdge(main_vertex, link_node)
    graph.addEdge(link_node, a_node)

    main_vertex.is_unfolded = True
    return graph


def unfold_conclusion_diamond(main_vertex, string_array, graph):

    graph.addNode(main_vertex)

    a_node, link_node = get_unary_nodes(graph,string_array)

    link_node.main = main_vertex

    graph.addEdge(main_vertex, link_node)
    graph.addEdge(link_node, a_node)

    main_vertex.is_unfolded = True
    return graph


# TODO note to self; conclusion moeten misschien de premisses zijn en andersom
# premise zijn nu de [L] rules en conclusion de [R] rules

def unfoldVertex(vertex_type, sequent_type, main_vertex, string_array, graph):

    current_unfold_function = unfold_functions[vertex_type][sequent_type]

    unfolded_graph = current_unfold_function(main_vertex, string_array, graph)
    return unfolded_graph


# a functions has to contain
# - main_vertex.is_unfolded = true
# - graph.add_node(main_vertex)

unfold_functions = {
    VertexType.Premise: {
        SequentType.SingleWord: no_operation,
        SequentType.Tensor: unfold_premise_tensor,
        SequentType.ForwardSlash: unfold_premise_forwardslash,
        SequentType.BackwardSlash: unfold_premise_backwardslash,
        SequentType.Diamond: unfold_premise_diamond,
        SequentType.Square: unfold_premise_square
    },
    VertexType.Conclusion: {
        SequentType.SingleWord: no_operation,
        SequentType.Tensor: unfold_conclusion_tensor,
        SequentType.ForwardSlash: unfold_conclusion_forwardslash,
        SequentType.BackwardSlash: unfold_conclusion_backwardslash,
        SequentType.Diamond: unfold_conclusion_diamond,
        SequentType.Square: unfold_conclusion_diamond
    },
    VertexType.NotALeaf: {
        SequentType.SingleWord: no_operation,
        SequentType.Tensor: no_operation,
        SequentType.ForwardSlash: no_operation,
        SequentType.BackwardSlash: no_operation,
        SequentType.Diamond: no_operation,
        SequentType.Square: no_operation
    }
}

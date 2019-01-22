from LoLaLinkNode import *
from functools import reduce
import re
from Graph import *
import itertools
import networkx as nx

TYPES_PATH = './lexicon.csv'


class Prover:
    def __init__(self):
        print("init prover")

    def prove(self, sentence, lexicon, targetType):
        words = sentence.lower().split()
        sequence_lists = map(lambda x: (lexicon[x], x), words)
        unfolded_graphs = list(map(create_unfolded_graph_list_from_word, sequence_lists))
        derivations = []
        lexicalCombinations = list(itertools.product(*unfolded_graphs))


        # g1 = LoLaGraph()
        # g2 = LoLaGraph()
        #
        # l1 = g1.addNode(NODE_FACTORY.createLinkNode(g1))
        # l2 = g1.addNode(NODE_FACTORY.createLinkNode(g1))
        # l2.type = LinkType.Par
        #
        # n1 = g1.addNode(NODE_FACTORY.createVertex(g1, "s"))
        # n2 = g1.addNode(NODE_FACTORY.createVertex(g1, "sos"))
        # n3 = g1.addNode(NODE_FACTORY.createVertex(g1, "s"))
        # n4 = g1.addNode(NODE_FACTORY.createVertex(g1, "sosonp"))
        # n5 = g1.addNode(NODE_FACTORY.createVertex(g1, "np"))
        #
        # g1.addEdge(l1, n1)
        # g1.addEdge(n2, l1)
        # g1.addEdge(n3, l1)
        # g1.addEdge(l2, n2)
        # g1.addEdge(l2, n4)
        # g1.addEdge(n5, l2)
        #
        # l3 = g2.addNode(NODE_FACTORY.createLinkNode(g2))
        # l4 = g2.addNode(NODE_FACTORY.createLinkNode(g2))
        # l3.type = LinkType.Par
        #
        # n6 = g2.addNode(NODE_FACTORY.createVertex(g2, "s"))
        # n7 = g2.addNode(NODE_FACTORY.createVertex(g2, "snps"))
        # n8 = g2.addNode(NODE_FACTORY.createVertex(g2, "nps"))
        # n9 = g2.addNode(NODE_FACTORY.createVertex(g2, "np"))
        # n10 = g2.addNode(NODE_FACTORY.createVertex(g2, "s"))
        #
        # g2.addEdge(l3, n6)
        # g2.addEdge(n7, l3)
        # g2.addEdge(n8, l3)
        # g2.addEdge(l4, n9)
        # g2.addEdge(l4, n8)
        # g2.addEdge(n10, l4)
        #
        # lexicalCombinations = [[g1, g2]]
        #
        # targetType = "snps"

        for lexicalCombination in lexicalCombinations:
            perms = list(itertools.permutations(lexicalCombination))

            graphs = []
            for perm in perms:
                accumulatedGraphs = [perm[0]]
                for i in range(1, len(perm)):
                    tmpGraphs = []
                    for aGraph in accumulatedGraphs:
                        otherGraph = perm[i]
                        tmpGraphs = tmpGraphs + aGraph.getPossibleConnections(otherGraph)
                    accumulatedGraphs = tmpGraphs
                graphs = graphs + accumulatedGraphs

            graphs = [g for g in graphs if len(g.getConclusions()) == 1 and g.getConclusions()[0].sequent == targetType]
            # TODO: remove duplicate graphs and this line below
            try:
                graphs = [graphs[0]]
            except:
                pass

            graphs[0].hasCorrectWordOrder(sentence)

            while graphs:
                graph = graphs.pop()
                if graph.isTensorTree():
                    derivations.append(graph)
                    continue

                graphs = graphs + graph.getPossibleContractions()
                graphs = graphs + graph.getPossibleRewritings()

        for derivation in derivations:
            # return the proof term
            print("ik ben een derivation")

    def buildGraph(self):
        return True


def get_types_file_dict():
    types_file = open(TYPES_PATH)

    types_str = types_file.read()

    types_file.close()

    # remove the first line
    types_str = re.split(r'\n', types_str, 1)[1]

    # split the the other lines
    types_split_str = re.split(r'\n', types_str)

    # separate each line by the comma
    split_sentences = map(lambda x: re.split(r',', x), types_split_str)
    # remove the empty lines
    filtered_sentenced = filter(lambda x: len(x[1]) != 0, split_sentences)
    # reduce list in dictionary
    final_dict = reduce(add_word_to_dict, filtered_sentenced, {})

    return final_dict


def add_word_to_dict(types_dict, word_sequence_list):
    word_name = word_sequence_list[0]
    word_sequence = word_sequence_list[1]

    if word_name in types_dict:
        types_dict[word_name].append(word_sequence)
    else:
        types_dict[word_name] = [word_sequence]
    return types_dict


def create_unfolded_graph_list_from_word(sequence_list_tuple):
    graph_list = []

    sequence_list, word = sequence_list_tuple
    for sequence in sequence_list:
        graph = LoLaGraph()

        lola_vertex = NODE_FACTORY.createVertex(graph, sequence)
        lola_vertex.is_sequent_root = True
        lola_vertex.word = word
        graph.addNode(lola_vertex)

        graph = graph.unfold_graph()

        graph_list.append(graph)

    return graph_list

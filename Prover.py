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
        sequence_lists = map(lambda x: lexicon[x], words)
        unfolded_graphs = list(map(create_unfolded_graph_list_from_word, sequence_lists))
        derivations = []
        lexiconCombinations = list(itertools.product(*unfolded_graphs))
        for lexiconCombination in lexiconCombinations:
            perms = list(itertools.permutations(lexiconCombination))

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
            # g1.draw()
            # g2.draw()

            # for g in graphs:
            #     g.draw()

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


def create_unfolded_graph_list_from_word(sequence_list):
    graph_list = []
    for sequence in sequence_list:
        graph = LoLaGraph()

        lola_vertex = NODE_FACTORY.createVertex(graph, sequence)
        lola_vertex.is_sequent_root = True

        graph.addNode(lola_vertex)

        graph = graph.unfold_graph()

        graph_list.append(graph)

    return graph_list

from LoLaLinkNode import *
from functools import reduce
import re
from Graph import *
import itertools

TYPES_PATH = './lexicon.csv'


class Prover:
    def __init__(self):
        print("init prover")

    def prove(self, sentence, lexicon, targetType):

        words = sentence.lower().split()
        sequence_lists = map(lambda x: lexicon[x], words)
        unfolded_graphs = list(map(create_unfolded_graph_list_from_word, sequence_lists))

        all_possible_graph_combinations = list(itertools.product(*unfolded_graphs))

        g1 = LoLaGraph()
        g2 = LoLaGraph()
        g3 = LoLaGraph()

        aap = g1.addNode(NODE_FACTORY.createVertex(g1, "np"))

        l1 = g2.addNode(NODE_FACTORY.createLinkNode(g2))
        l2 = g2.addNode(NODE_FACTORY.createLinkNode(g2))
        n1 = g2.addNode(NODE_FACTORY.createVertex(g2, "(np\s)/np"))
        n2 = g2.addNode(NODE_FACTORY.createVertex(g2, "np"))
        n3 = g2.addNode(NODE_FACTORY.createVertex(g2, "np\s"))
        n4 = g2.addNode(NODE_FACTORY.createVertex(g2, "np"))
        n5 = g2.addNode(NODE_FACTORY.createVertex(g2, "s"))
        g2.addEdge(l1, n1)
        g2.addEdge(l1, n2)
        g2.addEdge(n3, l1)
        g2.addEdge(l2, n3)
        g2.addEdge(l2, n4)
        g2.addEdge(n5, l2)

        g3.addNode(NODE_FACTORY.createVertex(g3, "s"))

        unfoldedGraphs = [g1,g2,g3]

        dingen = g1.getPossibleConnections(g2)

        for ding in dingen:
            ding.draw()



        # unfolded = wordh.makevertexunfold
        # Find all possible graphs obtained from connecting

        # unfoldedGraphs = [1,2,3]
        # perms = list(itertools.permutations(unfoldedGraphs))
        #
        # for perm in perms:
        #     accumulatedGraphs = [perm[0]]
        #     for i in range(1, len(perm)):
        #         for aGraph in accumulatedGraphs:
        #             otherGraph = perm[i]
        #             aGraph.getPossibleConnections(otherGraph)



        # derivations = []
        # while graphs:
        #     graph = graphs.pop()
        #     if graph.isTensorTree():
        #         derivations.append(graph)
        #         continue
        #
        #     graphs = graphs + graph.getPossibleContractions()
        #     graphs = graphs + graph.getPossibleRewritings()
        #
        # for derivation in derivations:
        #     # return the proof term
        #     print("ik ben een derivation")

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
        graph.addNode(NODE_FACTORY.createVertex(graph, sequence))

        graph = graph.unfold_graph()

        graph_list.append(graph)

    return graph_list


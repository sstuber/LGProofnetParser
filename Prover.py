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

        lexicalCombinations_with_targettype = list(map(lambda graph_list:add_target_type_graph(
            graph_list, targetType), lexicalCombinations))

        for lexicalCombination in lexicalCombinations_with_targettype:
            proofStructure = lexicalCombination[0].copy()
            for i in range(1, len(lexicalCombination)):
                proofStructure.graph = nx.compose(proofStructure.graph, lexicalCombination[i].copy().graph)

            premDic = {}
            concDic = {}

            # construct a dictionary of premises and conclusions
            # key = sequent, value = node
            for p in proofStructure.getPremises():
                if p.word:
                    # if the node is the root of a word module and it is non-simple
                    if proofStructure.getChildren(p.nodeId):
                        continue
                    if p.sequent not in concDic:
                        concDic[p.sequent] = []
                    concDic[p.sequent].append(p)
                    continue
                if p.sequent not in premDic:
                    premDic[p.sequent] = []
                premDic[p.sequent].append(p)

            for c in proofStructure.getConclusions():
                if c.word:
                    # if the node is the root of a word module and it is non-simple
                    if proofStructure.getParents(c.nodeId):
                        continue
                    if c.sequent not in premDic:
                        premDic[c.sequent] = []
                    premDic[c.sequent].append(p)
                    continue
                if c.sequent not in concDic:
                    concDic[c.sequent] = []
                concDic[c.sequent].append(c)


            connectionMaps = []
            for seq, _ in premDic.items():
                if seq in concDic:
                    connectionMaps.append(list(list(zip(x,concDic[seq])) for x in itertools.permutations(premDic[seq],len(concDic[seq]))))

            graphs = []

            for connectionMap in itertools.product(*connectionMaps):
                newGraph = proofStructure.connectFeest(list(connectionMap), sentence, targetType)
                if newGraph:
                    graphs.append(newGraph)

            visitedGraphs = set()

            while graphs:
                graph = graphs.pop()

                if graph in visitedGraphs:
                    continue
                visitedGraphs.add(graph)

                if graph.isTensorTree():
                    derivations.append(graph)
                    continue

                graphs = graphs + graph.getPossibleContractions()
                graphs = graphs + graph.getPossibleRewritings()

        for derivation in derivations:
            # return the proof term
            print("ik ben een derivation")

        return derivations

    def buildGraph(self, ):
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


def add_target_type_graph(graph_list, targettype):
    graph = LoLaGraph()

    lola_vertex = NODE_FACTORY.createVertex(graph, targettype)
    lola_vertex.is_sequent_root = True
    lola_vertex.from_target_type = True

    graph.addNode(lola_vertex)

    graph = graph.unfold_graph()

    new_graph_list = (*graph_list, graph)

    return new_graph_list


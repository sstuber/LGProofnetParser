from functools import reduce
import re
from Graph import *
import itertools
import networkx as nx
from Axiom_links import transform_to_axiom_graph
from build_proofterm import *

TYPES_PATH = './lexicon.csv'


# the prover looks whether derivations can be found given
# an input sequence, polarities and a target type
# this is done by means of a proof net
# the output is a proof term for each derivation

def LambekProver(sentence, lexicon, targetType, bias_map):
    # all words in the sentence
    words = sentence.lower().split()
    # matching sequents to the words according to the lexicon
    sequence_lists = map(lambda x: (lexicon[x], x), words)
    # create word modules from the sequents by unfolding them
    unfolded_graphs = list(map(create_unfolded_graph_list_from_word, sequence_lists))
    # storage for all derivations the prover may find
    derivations = []
    # An ordered list of sequents for each possible combination (one word might have multiple sequents)
    lexicalCombinations = list(itertools.product(*unfolded_graphs))
    # An ordered list of sequents for each possible combination, combined with the target type
    lexicalCombinations_with_targettype = list(map(lambda graph_list:add_target_type_graph(
        graph_list, targetType), lexicalCombinations))

    # for each lexical combination, look for a derivation
    for j in range(len(lexicalCombinations_with_targettype)):
        lexicalCombination = lexicalCombinations_with_targettype[j]
        print("Start connecting graphs")
        print("Trying lexical combination: " + str(j + 1) + "/" + str(len(lexicalCombinations_with_targettype)))

        # combine all the word modules into one connected proof net
        proofStructure = lexicalCombination[0].copy()
        for i in range(1, len(lexicalCombination)):
            proofStructure.graph = nx.compose(proofStructure.graph, lexicalCombination[i].copy().graph)

        # construct a dictionary of premises and conclusions
        # key = sequent, value = node
        premDic = {}
        concDic = {}

        for p in proofStructure.getPremises():
            if p.word:
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
                if proofStructure.getParents(c.nodeId):
                    continue
                if c.sequent not in premDic:
                    premDic[c.sequent] = []
                premDic[c.sequent].append(p)
                continue
            if c.sequent not in concDic:
                concDic[c.sequent] = []
            concDic[c.sequent].append(c)

        # generate all combinations of <premise - conclusion> connections that have the same sequent
        connectionMaps = []
        for seq, _ in premDic.items():
            if seq in concDic:
                connectionMaps.append(list(list(zip(x,concDic[seq])) for x in itertools.permutations(premDic[seq],len(concDic[seq]))))

        # generate all graphs according to the connection map and store those that are valid
        graphs = []
        for connectionMap in itertools.product(*connectionMaps):
            newGraph = proofStructure.connect(list(connectionMap), sentence, targetType)
            if newGraph:
                graphs.append(newGraph)

        print("found " + str(len(graphs)) + " proofnets")
        print("finished connecting graphs")
        print("start contracting and rewriting graphs")

        # attempt to rewrite each graph into a tensor tree (if tensor tree, then derivation is valid)
        for i in range(len(graphs)):
            print("Trying graph " + str(i + 1) + "/" + str(len(graphs)))
            graph = graphs[i]
            testGraphs = [graph]
            visitedGraphs = set()

            # while we still have graphs that might turn into a derivation
            # 1. apply binary contractions and structural rewrites until stuck
            # 2. apply unary contractions
            # 3. repeat 1-2 until no more graphs or derivation found
            # this order is chosen because unary contractions yield divergence
            while testGraphs:
                testGraph = testGraphs.pop()

                # if the isomorphism of the current graph is already evaluated, disregard it
                if testGraph in visitedGraphs:
                    continue

                visitedGraphs.add(testGraph)

                # first do binary contractions and structural rewritings until stuck
                updated = True
                while updated:
                    prevGraph = testGraph
                    # apply a binary contraction if possible
                    for vertex in testGraph.getVertices():
                        if vertex.getVertexType(testGraph) == VertexType.Conclusion:
                            continue
                        try:
                            upperLink = testGraph.getNode(testGraph.getChildren(vertex.nodeId)[0])
                            if upperLink.mode is LinkMode.Binary:
                                contraction = testGraph.contractBinary(vertex, upperLink)
                                if contraction:
                                    testGraph = contraction
                                    break
                        except:
                            break
                    # apply a structural rewrite if possible
                    for link in testGraph.getLinks():
                        rewriting = testGraph.rewrite(link)
                        if rewriting:
                            testGraph = rewriting

                    # if the graph did not change, we cannot apply more binary contractions / structural rewrites
                    updated = prevGraph != testGraph

                # Check if we are done at this point
                if testGraph.isTensorTree():
                    derivations.append(testGraph)
                    print("Derivation found")
                    break

                # generate the unary contractions and restart the loop
                testGraphs = testGraphs + testGraph.getPossibleUnaryContractions()

    print("finished contracting and rewriting graphs")

    derivation_terms = []

    # for each derivation, find a proof term
    for derivation in derivations:

        main_proof_structure = derivation.get_deep_parent()

        transformed_graph = transform_to_axiom_graph(main_proof_structure, bias_map)

        transformed_graph.draw()

        subsets = get_subsets(transformed_graph)

        all_terms = []

        for subset in subsets:
            term_list = crawl_axiom_graph(transformed_graph, subset)
            print(all_terms)
            all_terms = all_terms + term_list

        derivation_terms.append((main_proof_structure.copy(), all_terms))

    return derivation_terms


# read the lexicon and make the information usable
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


# helper function for lexicon loader
def add_word_to_dict(types_dict, word_sequence_list):
    word_name = word_sequence_list[0]
    word_sequence = word_sequence_list[1]

    if word_name in types_dict:
        types_dict[word_name].append(word_sequence)
    else:
        types_dict[word_name] = [word_sequence]
    return types_dict


# generate a word module from a word in a sentence using the lexicon
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


# add the unfolded target type module of the sentence to the proof structure
def add_target_type_graph(graph_list, targettype):
    graph = LoLaGraph()

    lola_vertex = NODE_FACTORY.createVertex(graph, targettype)
    lola_vertex.is_sequent_root = True
    lola_vertex.from_target_type = True

    graph.addNode(lola_vertex)

    graph = graph.unfold_graph()

    new_graph_list = (*graph_list, graph)

    return new_graph_list


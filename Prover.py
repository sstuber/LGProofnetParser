from LoLaLinkNode import *
from Graph import *
import itertools

class Prover:
    def __init__(self):
        print("init prover")

    def prove(self, sentence, lexicon, targetType):
        words = sentence.lower().split()
        forms = map(lambda x: lexicon[x], words)
        #unfoldedGraphs = list(map(lambda x: stanfunctie[x], forms))

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
            print("hoi")

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

    def create_unfolded_graph_from_word(self, sequent):
        graph = LoLaGraph()
        graph.addNode(NODE_FACTORY.createVertex(graph, sequent))

        graph = graph.unfold_graph()

        return graph


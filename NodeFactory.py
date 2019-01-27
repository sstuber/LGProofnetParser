from LoLaLinkNode import *


# generate nodes and supply fresh unused identifiers
class NodeFactory:
    def __init__(self):
        self.currentHighestId = -1

    # generate a new unused id
    def getNewId(self):
        self.currentHighestId = self.currentHighestId + 1
        return self.currentHighestId

    # add a new link node to a graph
    def createLinkNode(self, graph):
        newId = self.getNewId()
        return LoLaLinkNode(newId, graph)

    # add a new vertex to a graph
    def createVertex(self, graph, sequent):
        newId = self.getNewId()
        return LoLaVertex(newId, graph, sequent)


# make the factory globally available in the code
NODE_FACTORY = NodeFactory()

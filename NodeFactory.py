from LoLaLinkNode import *



class NodeFactory:
    def __init__(self):
        self.currentHighestId = -1

    def getNewId(self):
        self.currentHighestId = self.currentHighestId + 1
        return self.currentHighestId

    def createLinkNode(self, graph):
        newId = self.getNewId()
        return LoLaLinkNode(newId, graph)

    def createVertex(self, graph, sequent):
        newId = self.getNewId()
        return LoLaVertex(newId, graph, sequent)



NODE_FACTORY = NodeFactory()

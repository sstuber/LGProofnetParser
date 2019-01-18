from LoLaLinkNode import *



class NodeFactory:
    def __init__(self):
        self.currentHighestId = -1

    def getNewId(self):
        self.currentHighestId = self.currentHighestId +1
        return self.currentHighestId

    def createLinkNode(self):
        newId = self.getNewId()
        return LoLaLinkNode(newId)

    def createVertex(self):
        newId = self.getNewId()
        return LoLaVertex(newId)



NODE_FACTORY = NodeFactory()

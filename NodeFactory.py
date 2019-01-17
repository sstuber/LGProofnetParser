



class NodeFactory:
    def __init__(self):
        self.currentHighestId = -1

    def getNewId(self):
        self.currentHighestId = self.currentHighestId +1
        return self.currentHighestId

    def createLinkNode(self):
        newId = self.getNewId()

    def createVertex(self):
        newId = self.getNewId()



NODE_FACTORY = NodeFactory()

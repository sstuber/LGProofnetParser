from enum import Enum


# the color of the axiom link
class AxiomLinkType(Enum):
    Blue = 'Blue'
    Red = 'Red'


# what direction the axiom link points
class AxiomLinkDirection(Enum):
    Up = 'up'
    Down = 'down'


# the type of vertex (dependent on if it is has parents and or children)
class VertexType(Enum):
    Premise = 'premise'
    Conclusion = 'conclusion'
    NotALeaf = 'notaleaf'

    # get the opposite vertex type
    def OppositeLeafType(vertexType):
        if vertexType == VertexType.Premise:
            return VertexType.Conclusion
        elif vertexType == VertexType.Conclusion:
            return VertexType.Premise
        return "invalid parameter in OppositeLeafType"


# the type of link (tensor or par / white or black)
class LinkType(Enum):
    Tensor = 'tensor'
    Par = 'Par'


# what way the link points if you look at the vertices (/\ or \/)
class LinkShape(Enum):
    Downward = 'downward'
    Upward = 'upward'


# how many vertices a link connects
class LinkMode(Enum):
    Unary = 'unary'
    Binary = 'binary'


# the direction of an edge from a link
class EdgeAlignment(Enum):
    Left = 'left'
    Right = 'right'
    Straight = 'straight'

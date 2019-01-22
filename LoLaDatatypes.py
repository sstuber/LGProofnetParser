from enum import Enum


class VertexType(Enum):
    Premise = 'premise'
    Conclusion = 'conclusion'
    NotALeaf = 'notaleaf'

    def OppositeLeafType(vertexType):
        if vertexType == VertexType.Premise:
            return VertexType.Conclusion
        elif vertexType == VertexType.Conclusion:
            return VertexType.Premise
        return "invalid parameter in OppositeLeafType"


class LinkType(Enum):
    Tensor = 'tensor'
    Par = 'Par'


class LinkShape(Enum):
    Downward = 'downward'
    Upward = 'upward'


class LinkMode(Enum):
    Unary = 'unary'
    Binary = 'binary'
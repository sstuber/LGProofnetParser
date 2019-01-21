from enum import Enum


class VertexType(Enum):
    Premise = 'premise'
    Conclusion = 'conclusion'
    NotALeaf = 'notaleaf'


class LinkType(Enum):
    Tensor = 'tensor'
    Par = 'Par'


class LinkShape(Enum):
    Downward = 'downward'
    Upward = 'upward'


class LinkMode(Enum):
    Unary = 'unary'
    Binary = 'binary'
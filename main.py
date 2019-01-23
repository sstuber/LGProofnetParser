import networkx as nx
import LoLaLinkNode
import matplotlib.pyplot as plt
from Prover import *
from NodeFactory import *
from Graph import *

MATCH_REGEX = r'(\w+|\(.+\))(\/|\\)(\(.+\)|\w+)|(\w+)'
function_dict = {
    '/': 'right',
    '\\': 'left',
    None: 'singleton'
}

upgraded_regex = r'(diamond)?(square)?(\w+|\(.+\))(\/|\\)(diamond)?(square)?(\(.+\)|\w+)|(diamond)?(square)?(\w+)'
#(diamond)?(square)?(\w+|\(.+\))(\/|\\)(diamond)?(square)?(\(.+\)|\w+)|(diamond)?(square)?(\w+)
if __name__ == '__main__':
    sentence = "games that kids love but parents hate"
    targetType = "n"
    print("begin test: " + sentence + " |- " + targetType)
    prover = Prover()
    lexicon = get_types_file_dict()

    sentence = "Games that kids love but parents hate"
    targetType = "n"

    prover.prove(sentence, lexicon, targetType)

    # while True:
    #     print('give sentence')
    #     sentence = input('')
    #
    #     print('give target type')
    #     targetType = input('')
    #
    #     # print('give bias for s')
    #     # bias_s = input('')
    #     # print('give bias for n')
    #     # bias_n = input('')
    #     # print('give bias for np')
    #     # bias_np = input('')
    #
    #     print("Begin test: " + sentence + " |- " + n)
    #     prover.prove(sentence, lexicon, targetType)

    print("end test " + sentence)

    print("end main")

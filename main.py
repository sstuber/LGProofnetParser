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

    prover = Prover()
    lexicon = get_types_file_dict()

    while True:

        print('give sentence')
        sentence = input('')

        print('give target type')
        targetType = input('')

        # print('give bias for s')
        # bias_s = input('')
        # print('give bias for n')
        # bias_n = input('')
        # print('give bias for np')
        # bias_np = input('')

        print("Begin test: " + sentence + " |- " + targetType)
        try:
            prover.prove(sentence, lexicon, targetType)
        except Exception as ex:
            print(ex)
            print("Encountered an error, please give new input")

        print("end test " + sentence)

    print("end main")

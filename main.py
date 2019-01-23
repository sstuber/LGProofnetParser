import networkx as nx
import LoLaLinkNode
import matplotlib.pyplot as plt
from Prover import *
from NodeFactory import *
from Graph import *


def get_bias_input():
    pos_input = set(['p','+','true','t','y'])
    neg_input = set(['n','-','false','f'])
    user_input = input('').lower()
    if user_input in pos_input:
        return True
    if user_input in neg_input:
        return False
    print("The input you gave was invalid. Please respond with + or -")
    return get_bias_input()


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

        print('give bias for s')
        bias_s = get_bias_input()
        print('give bias for n')
        bias_n = get_bias_input()
        print('give bias for np')
        bias_np = get_bias_input()

        bias = {bias_s, bias_n, bias_np}

        print("Begin test: " + sentence + " |- " + targetType)
        try:
            prover.prove(sentence, lexicon, targetType)
        except Exception as ex:
            print(ex)
            print("Encountered an error, please give new input")

        print("end test " + sentence)

    print("end main")



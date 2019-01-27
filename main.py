from Prover import *


# handle the user input when requesting polarities
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


if __name__ == '__main__':

    prover = Prover()
    lexicon = get_types_file_dict()

    while True:
        print('give sentence')
        sentence = 'games that kids love but parents hate'

        print('give target type')
        targetType = 'n'

        # print('give bias for s')
        # bias_s = get_bias_input()
        # print('give bias for n')
        # bias_n = get_bias_input()
        # print('give bias for np')
        # bias_np = get_bias_input()
        #
        # bias = {bias_s, bias_n, bias_np}

        print("Begin test: " + sentence + " |- " + targetType)

        prover.prove(sentence, lexicon, targetType)
        print("Encountered an error, please give new input")

        input('')
        print("end test " + sentence)

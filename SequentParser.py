
from enum import Enum
import re


MATCH_REGEX = r'(square)?(diamond)?(square)?(\w+|\(.+\))(\/|\\|tensor)(square)?(diamond)?(square)?(\(.+\)|\w+)|(square)?(diamond)?(square)?(\w+|\(.+\))'

LEFT_HAND_ID = 3
FUNCTION_ID = 4
RIGHT_HAND_ID = 8
SINGLETON_ID = 12
START_SECOND_UNARY = 9



class SequentType(Enum):
    ForwardSlash = 0
    Tensor = 1
    BackwardSlash = 2
    Square = 3
    Diamond = 4
    SingleWord = 5


sequentTypeDict = {
    '/': SequentType.ForwardSlash,
    '\\': SequentType.BackwardSlash,
    'tensor': SequentType.Tensor,
    None: SequentType.SingleWord
}


def ParseSequent(sequentString):

    match_tuple = re.match(MATCH_REGEX, sequentString).groups()

    find_unary_result = find_unary(match_tuple, sequentString)

    if find_unary_result is not None:
        return find_unary_result

    # if match_tuple[0] is not None or match_tuple[1] is not None or match_tuple[2] is not  None:
        # print('unary string found')
        # return FindUnary(match_tuple, sequentString)

    sequent_operator_string = match_tuple[FUNCTION_ID]
    sequent_type = sequentTypeDict[sequent_operator_string]

    if sequent_type == SequentType.SingleWord:
        return parse_single_word(match_tuple, sequentString)

    left_hand = match_tuple[LEFT_HAND_ID]
    left_hand_normalized = normalize_sequent(left_hand)
    right_hand = match_tuple[RIGHT_HAND_ID]
    right_hand_normalized = normalize_sequent(right_hand)

    return sequent_type, [sequentString, left_hand_normalized, right_hand_normalized]

def normalize_sequent(sequent_string: str):

    if sequent_string[0] == '(':
        sequent_string = sequent_string[1:-1]

    return sequent_string


def parse_single_word(match_tuple, full_string):
    found_unary = find_unary(match_tuple, full_string, START_SECOND_UNARY)

    if found_unary is not None:
        return found_unary

    return SequentType.SingleWord, [full_string]


def find_unary(match_tuple, full_string, start_id=0):

    unary_string_dict = {
        'square': SequentType.Square,
        'diamond': SequentType.Diamond
    }

    for i in range(start_id, start_id + 3):

        if match_tuple[i] is None:
            continue

        unary_string = match_tuple[i]
        split_string = re.split(unary_string, full_string, 1)[1]

        return unary_string_dict[unary_string], [full_string, normalize_sequent(split_string)]

    return None




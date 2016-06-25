from __future__ import absolute_import, print_function, unicode_literals

import random

from .constants import (NUM_BLACK_WORDS, NUM_BLUE_WORDS, NUM_RED_WORDS,
                        NUM_WHITE_WORDS, NUM_WORDS)
from ..models import TeamWord


def gen_word_list(num_words=NUM_WORDS):
    """Generate a list of words to be used by the game.

    Currently a placeholder.

    :param int num_words: The total number of words to return
    :return: Words to use.
    :rtype: list[str]
    """
    return [str(x) for x in range(num_words)]


def gen_team_list(num_red_words=NUM_RED_WORDS, num_blue_words=NUM_BLUE_WORDS,
                  num_white_words = NUM_WHITE_WORDS, num_black_words=NUM_BLACK_WORDS,
                  random=random.Random()):
    """Generate a list which maps words to teams.

    :param int num_red_words: The number of words for the red team
    :param int num_blue_words: The number of words for the blue team
    :param int num_white_words: The number of words for the white team
    :param int num_black_words: The number of words for the black team
    :return: A list of teams
    :rtype: list[TeamWord]
    """
    output = []
    output.extend([TeamWord.RED for _ in range(num_red_words)])
    output.extend([TeamWord.BLUE for _ in range(num_blue_words)])
    output.extend([TeamWord.WHITE for _ in range(num_white_words)])
    output.extend([TeamWord.BLACK for _ in range(num_black_words)])

    random.shuffle(output)
    return output

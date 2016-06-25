import requests

from codewords import models as m
from codewords.app import app, db
from codewords.game_logic.constants import (NUM_RED_WORDS, NUM_BLUE_WORDS,
    NUM_BLACK_WORDS, NUM_WHITE_WORDS)


def test_flow(server, db):
    """
    Create a game and play it to completion, asserting various
    properties along the way
    """
    host, port = server
    base_url = 'http://{host}:{port}/'.format(host=host, port=port)

    # Create a game
    response = requests.post(base_url + 'game'.format(host=host, port=port))
    game_id = response.json()['game_id']
    assert game_id > 0

    # Get the giver page
    giver_route = base_url + 'game/{}/give'.format(game_id)
    response = requests.get(giver_route, params={'team': 'blue'})
    j = response.json()
    assert 'red_words' in j
    assert len(j['red_words']) == NUM_RED_WORDS
    assert 'blue_words' in j
    assert len(j['blue_words']) == NUM_BLUE_WORDS
    assert 'black_words' in j
    assert len(j['black_words']) == NUM_BLACK_WORDS
    assert 'white_words' in j
    assert len(j['white_words']) == NUM_WHITE_WORDS

    # Post to the giver page if you're not the correct team
    response = requests.post(giver_route + '?team=red', json={'word': 'foo'})
    assert not response.ok

    # Post to the giver page if you're get the wrong word
    good_words = requests.get(giver_route + '?team=blue').json()['blue_words']
    bad_word = 'foo'
    while bad_word in good_words:
        bad_word += 'o'
    response = requests.post(giver_route + '?team=blue',
                             json={'word': bad_word, 'number': 1})
    assert not response.ok

    # Post to the giver page if you're get the wrong number
    response = requests.post(giver_route + '?team=blue',
                             json={'word': good_words[0], 'number': -1})
    assert not response.ok

    # Post to the giver page when everything is correct
    good_words = requests.get(giver_route + '?team=blue').json()['blue_words']
    response = requests.post(giver_route + '?team=blue',
                             json={'word': good_words[0], 'number': 2})
    assert response.ok

    # Check to make sure that the Game object is now correct
    game = db.session.query(m.Game).get(game_id)
    assert game.status == m.GameStatus.BLUE_TEAM_GUESS

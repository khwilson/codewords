from codewords import models as m
from codewords.app import db


def test_enums():
    assert m.GameStatus.from_index(0) == m.GameStatus.BLUE_TEAM_GIVE
    assert m.GameStatus.from_index(1) == m.GameStatus.RED_TEAM_GIVE
    assert m.GameStatus.from_index(2) == m.GameStatus.BLUE_TEAM_GUESS
    assert m.GameStatus.from_index(3) == m.GameStatus.RED_TEAM_GUESS
    assert m.GameStatus.from_index(4) == m.GameStatus.DONE


    assert m.GameWinner.from_index(0) == m.GameWinner.BLUE_TEAM
    assert m.GameWinner.from_index(1) == m.GameWinner.RED_TEAM
    assert m.GameWinner.from_index(2) == m.GameWinner.NOT_DONE

    assert m.TeamWord.from_index(0) == m.TeamWord.BLUE
    assert m.TeamWord.from_index(1) == m.TeamWord.RED
    assert m.TeamWord.from_index(2) == m.TeamWord.WHITE
    assert m.TeamWord.from_index(3) == m.TeamWord.BLACK


def test_game():
    game = m.Game(['hello', 'goodbye'], [m.TeamWord.BLUE, m.TeamWord.BLACK])
    assert game.words == ['hello', 'goodbye']
    assert game.teams == [m.TeamWord.BLUE, m.TeamWord.BLACK]
    assert game.status == m.GameStatus.BLUE_TEAM_GIVE


def test_game_commit(db):
    """
    Create a Game object, commit it, pull it, manipulate it, recommit, and
    repull. Make sure in every case our changes are commited.

    This is to make sure that our `@property`s that have setters are
    working as expected.
    """
    game = m.Game(['hello', 'goodbye'], [m.TeamWord.BLUE, m.TeamWord.BLACK])
    db.session.add(game)
    db.session.commit()

    game_id = game.id
    game = db.session.query(m.Game).get(game_id)
    game.status = m.GameStatus.BLUE_TEAM_GUESS
    assert game.status_encoded == m.GameStatus.BLUE_TEAM_GUESS.value
    assert game.status == m.GameStatus.BLUE_TEAM_GUESS

    db.session.commit()

    game = db.session.query(m.Game).get(game_id)
    assert game.status == m.GameStatus.BLUE_TEAM_GUESS
    assert game.status_encoded == m.GameStatus.BLUE_TEAM_GUESS.value

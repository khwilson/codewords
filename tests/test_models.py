from codewords import models as m


def test_enums():
    assert m.GameStatus.from_index(0) == m.GameStatus.BLUE_TEAM
    assert m.GameStatus.from_index(1) == m.GameStatus.RED_TEAM
    assert m.GameStatus.from_index(2) == m.GameStatus.DONE


    assert m.GameWinner.from_index(0) == m.GameWinner.BLUE_TEAM
    assert m.GameWinner.from_index(1) == m.GameWinner.RED_TEAM
    assert m.GameWinner.from_index(2) == m.GameWinner.NOT_DONE

    assert m.TeamWord.from_index(0) == m.TeamWord.BLUE
    assert m.TeamWord.from_index(1) == m.TeamWord.RED
    assert m.TeamWord.from_index(2) == m.TeamWord.WHITE
    assert m.TeamWord.from_index(3) == m.TeamWord.BLACK


def test_game():
    game = m.Game([b'hello', b'goodbye'], [m.TeamWord.BLUE, m.TeamWord.BLACK])
    assert game.words == [b'hello', b'goodbye']
    assert game.teams == [m.TeamWord.BLUE, m.TeamWord.BLACK]
    assert game.status == m.GameStatus.BLUE_TEAM

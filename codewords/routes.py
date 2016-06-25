from __future__ import absolute_import, print_function, unicode_literals

from flask import (jsonify, make_response, redirect, render_template, request,
                   send_from_directory, url_for)

from ._app import app
from . import models as m
from .models import db
from .game_logic import word_gen


@app.route("/")
def index():
    """ The landing page """
    return render_template("index.html")


@app.route("/css/<path:css_path>")
def css_route(css_path):
    """ A basic route to send static css.

    This should be moved to nginx before you deploy!
    """
    return send_from_directory('css', css_path)


@app.route("/js/<path:js_path>")
def js_route(js_path):
    """ A basic route to send static js.

    This should be moved to nginx before you deploy!
    """
    return send_from_directory('js', js_path)


@app.route('/game', methods=['POST'])
def new_game():
    """
    Create a new game by POSTing at this route.

    Redirects to the game after creation.
    """
    game = m.Game(word_gen.gen_word_list(), word_gen.gen_team_list())
    db.session.add(game)
    db.session.commit()
    return redirect(url_for('display_game', game_id=game.id))


@app.route('/game/<int:game_id>')
def display_game(game_id):
    game = db.session.query(m.Game).get(game_id)
    return jsonify(message='Successful', game_id=game.id)


@app.route('/game/<int:game_id>/give', methods=['GET', 'POST'])
def giver_route(game_id):
    team = request.args.get('team')
    if not team or team not in ['blue', 'red']:
        return make_response(jsonify(msg='Invalid team'), 404)

    if team == 'blue':
        team = m.GameStatus.BLUE_TEAM_GIVE
    elif team == 'red':
        team = m.GameStatus.RED_TEAM_GIVE
    else:
        print("TTTTTTTTTAAAAAAAAAAWWWWWWWWW")

    print("Note: ", team)

    game = db.session.query(m.Game).get(game_id)
    my_turn = game.status == team
    is_done = game.status == m.GameStatus.DONE

    red_words = [word for word, the_team in zip(game.words, game.teams) if the_team == m.TeamWord.RED]
    blue_words = [word for word, the_team in zip(game.words, game.teams) if the_team == m.TeamWord.BLUE]
    white_words = [word for word, the_team in zip(game.words, game.teams) if the_team == m.TeamWord.WHITE]
    black_words = [word for word, the_team in zip(game.words, game.teams) if the_team == m.TeamWord.BLACK]
    my_words = red_words if team == m.GameStatus.RED_TEAM_GIVE else blue_words

    if request.method == 'GET':
        return jsonify(red_words=red_words, blue_words=blue_words,
                       black_words=black_words, white_words=white_words,
                       my_turn=my_turn, is_done=is_done)

    if request.method == 'POST':
        if not my_turn:
            return make_response(jsonify(msg="It's not your turn", 
                red_words=red_words, blue_words=blue_words,
                black_words=black_words, white_words=white_words,
                my_turn=my_turn, is_done=is_done), 400)
        word = request.json['word']
        if word not in my_words:
            return make_response(jsonify(msg="Word not recognized",
                red_words=red_words, blue_words=blue_words,
                black_words=black_words, white_words=white_words,
                my_turn=my_turn, is_done=is_done), 400)

        number = request.json['number']
        if not number or not (1 <= number <= len(game.words)):
            return make_response(jsonify(msg="Invalid number of words",
                red_words=red_words, blue_words=blue_words,
                black_words=black_words, white_words=white_words,
                my_turn=my_turn, is_done=is_done), 400)
        game_hint = m.GameHint(game_id=game.id, word=word, number=number)
        db.session.add(game_hint)

        if team == m.GameStatus.BLUE_TEAM_GIVE:
            game.status = m.GameStatus.BLUE_TEAM_GUESS
        elif team == m.GameStatus.RED_TEAM_GIVE:
            game.status = m.GameStatus.RED_TEAM_GUESS
        else:
            print("WWWWWWWWWWWAAAAAAAAAATTTTTTTT")
        print("Note2: ", team)
        db.session.commit()

        return jsonify(red_words=red_words, blue_words=blue_words,
                       black_words=black_words, white_words=white_words,
                       my_turn=my_turn, is_done=is_done, msg='Successful')

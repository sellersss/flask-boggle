from flask import Flask, render_template, redirect, request, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "random-secret1234"

# debug = DebugToolbarExtension(app)


@app.route('/')
def get_home():
    """ Display board and form on home page """

    board = boggle_game.make_board()

    # Add board to session
    session['board'] = board

    return render_template('home.html', board=board)


@app.route('/check-guess')
def check_guess():
    """ Checks the guess sent from AJAX """

    # Grab guess from the request args
    guess = request.args['guess']

    board = session['board']

    # Checks to see if the word is valid
    result = boggle_game.check_valid_word(board, guess)

    # Returns JSON response
    return jsonify({'result': result})


@app.route('/stats', methods=['POST'])
def update_stats():
    """ Updates the stats for the user on the backend """

    score = int(request.json["score"])
    highscore = session.get("highscore", 0)
    times_played = session.get("times_played", 0)

    session['times_played'] = times_played + 1
    session['highscore'] = max(score, highscore)

    return jsonify({'timesPlayed': times_played, 'highscore': highscore})

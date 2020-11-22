from flask import Flask, render_template, redirect, request, session
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "not0so0secret"


@app.route("/home")
@app.route("/")
def home():
    """Start page with start game"""


@app.route("/game")
def game_start():
    """Game page where boggle (form) is played"""

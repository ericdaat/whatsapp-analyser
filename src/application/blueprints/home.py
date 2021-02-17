import logging

import flask
import plotly.graph_objects as go
from plotly.offline.offline import plot

from src.parser.chat import read_chat, chat_pipeline
from src import viz

bp = flask.Blueprint("home", __name__)


@bp.route("/")
def index():
    return flask.render_template("home.html")


@bp.route("/chat")
def chat():
    # Load dataset
    chat = read_chat(path="/Users/eric/Downloads/_chat 2.txt")
    chat_df = chat_pipeline(chat)

    # Graphs
    graph_divs = []
    graph_function_list = [
        viz.nb_messages_per_author,
        viz.len_messages_per_author,
        viz.timeline_per_author,
        viz.hours_of_activity_per_author,
        viz.most_frequent_words
    ]

    for graph_function in graph_function_list:
        fig = graph_function(chat_df)
        div = viz.plotly_figure_to_div(fig)
        graph_divs.append(div)

    return flask.render_template(
        "chat.html",
        graph_divs=graph_divs
    )

import logging

import flask
import plotly.graph_objects as go
from plotly.offline.offline import plot

from src.parser.chat import read_chat, chat_pipeline
from src.application.viz import plotly_figure_to_div

bp = flask.Blueprint("home", __name__)


@bp.route("/")
def index():
    return flask.render_template("home.html")


@bp.route("/chat")
def chat():
    # Load dataset
    chat = read_chat(path=None)
    chat_df = chat_pipeline(chat)

    # Graphs
    data = chat_df\
        .groupby("author")["message"]\
        .count()\
        .sort_values(ascending=False)

    fig = go.Figure(
        data=go.Bar(x=data.index,
                    y=data.values)
    )

    div = plotly_figure_to_div(fig)

    return flask.render_template("chat.html", div=div)

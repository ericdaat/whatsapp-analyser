from collections import Counter

import pandas as pd
import plotly.graph_objects as go
import plotly.offline as opy
import plotly.express as px


def nb_messages_per_author(chat_df):
    data = chat_df\
        .groupby("author")["message"]\
        .count()\
        .rename("count")\
        .reset_index()\
        .sort_values(by="count", ascending=False)

    fig = px.bar(
        data,
        x="author",
        y="count",
        color="author"
    )

    fig.update_layout(
        title="Nombre de messages par utilisateur",
        xaxis_title="Utilisateur",
        yaxis_title="Nombre de messages",
        showlegend=False
    )

    return fig


def len_messages_per_author(chat_df):
    fig = px.box(
        chat_df,
        x="author",
        y="message_len",
        color="author"
    )

    fig.update_layout(
        title="Longueur des messages par utilisateur",
        xaxis_title="Utilisateur",
        yaxis_title="Longueur des messages",
        showlegend=False
    )

    return fig


def timeline_per_author(chat_df):
    data = chat_df\
            .groupby([pd.Grouper(freq="D"), "author"])["message"]\
            .count()\
            .rename("count")\
            .reset_index()

    fig = px.bar(
        data,
        x="timestamp",
        y="count",
        color="author"
    )

    fig.update_layout(
        title="Evolution du nombre de messages par utilisateur",
        xaxis_title="Utilisateur",
        yaxis_title="Nombre de messages"
    )

    return fig


def hours_of_activity_per_author(chat_df):
    data = chat_df
    data["hour"] = chat_df.index.hour.astype(str)

    data = data\
        .groupby(["hour", "author"])["message"]\
        .count()\
        .rename("count")\
        .reset_index()

    fig = px.bar(
        data,
        x="hour",
        y="count",
        color="author"
    )

    fig.update_layout(
        title="Nombre de messages par heure de la journée",
        xaxis_title="Heure de la journée",
        yaxis_title="Nombre de messages"
    )

    return fig



def most_frequent_words(chat_df):
    results = Counter()
    chat_df["message_nlp"].str.split().apply(results.update)
    data = pd.DataFrame(
        results.most_common(20),
        columns=["word", "count"]
    )

    fig = px.bar(
        data,
        y="word",
        x="count",
        orientation="h"
    )

    fig.update_layout(
        title="Termes les plus communs",
        yaxis_title="Termes",
        xaxis_title="Nombre d'apparitions",
        yaxis={"categoryorder": "total ascending"}
    )

    return fig


def plotly_figure_to_div(fig, include_plotlyjs=False, static_plot=False):
    """Convert a plotly figure to a div.
    Args:
        fig (plotly.Figure): Plotly figure
        include_plotlyjs (bool): Include Plotly JS
        static_plot (bool, optional): Display figure as static plot. Defaults to False.
    Returns:
        str: HTML div
    """
    fig.update_layout(
        template="plotly_white",
        margin=dict(t=90, b=40, l=20, r=20),
        autosize=True,
        height=500
    )

    div = opy.plot(
        fig,
        auto_open=False,
        output_type="div",
        include_plotlyjs=include_plotlyjs,
        config={
            "staticPlot": static_plot,
            "responsive": True
        }
    )

    return div

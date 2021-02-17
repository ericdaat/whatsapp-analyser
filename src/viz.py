from collections import Counter

import pandas as pd
import plotly.graph_objects as go
import plotly.offline as opy
import plotly.express as px
from plotly.subplots import make_subplots

DEFAULT_HEIGHT = 600


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
        showlegend=False,
        height=DEFAULT_HEIGHT
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
        showlegend=False,
        height=DEFAULT_HEIGHT
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
        yaxis_title="Nombre de messages",
        height=DEFAULT_HEIGHT
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
        yaxis_title="Nombre de messages",
        height=DEFAULT_HEIGHT
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
        title="Mots les plus utilisés",
        yaxis_title="Mots",
        xaxis_title="Nombre d'apparitions",
        yaxis={"categoryorder": "total ascending"},
        height=DEFAULT_HEIGHT
    )

    return fig


def plot_topics(topic_model, vectorizer):
    n_topics = topic_model.n_components_
    n_top_words = 10
    feature_names = vectorizer.get_feature_names()

    df_list = []

    for topic_idx, topic in enumerate(topic_model.components_):
        top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        df_tmp = pd.DataFrame(dict(topic=topic_idx,
                                words=top_features,
                                weights=weights))

        df_list.append(df_tmp)

    fig = make_subplots(
        rows=4,
        cols=3,
        subplot_titles=["Topic {0}".format(i) for i in range(10)]
    )

    for i, df in enumerate(df_list):
        fig.add_trace(
            go.Bar(
                x=df["weights"],
                y=df["words"],
                orientation="h"
            ),
            row=(i//3)+1,
            col=(i%3)+1
        )

    fig.update_layout(
        height=1200,
        width=1200,
        title_text="Topic Modeling",
        showlegend=False
    )

    fig.update_yaxes(categoryorder="total ascending")

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
        autosize=True
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

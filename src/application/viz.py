import pandas as pd
import plotly.graph_objects as go
import plotly.offline as opy


def nb_messages_per_author(chat_df):
    data = chat_df\
        .groupby("author")["message"]\
        .count()\
        .sort_values(ascending=False)

    fig = go.Figure(
        data=go.Bar(x=data.index,
                    y=data.values)
    )

    return fig


def len_messages_per_author(chat_df):
    data = chat_df\
        .groupby("author")["message_len"]\
        .mean()\
        .sort_values(ascending=False)

    fig = go.Figure(
        data=go.Bar(x=data.index,
                    y=data.values)
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
        margin=dict(t=40, b=20, l=10, r=10),
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

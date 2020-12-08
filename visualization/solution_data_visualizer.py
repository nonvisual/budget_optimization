import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np


def visualize_solution_data(solved_data: pd.DataFrame, grocery_threshold=None):
    assert "solution" in solved_data.columns, "Dataframe does not have solution column"
    solved_data["expense"] = abs(solved_data["Debit"])

    plot_pie_charts(solved_data)
    plot_sunbirst_charts(solved_data)
    plot_bar_plots(solved_data)
    plot_grocery_bar_chart(solved_data, grocery_threshold)
    plot_expense_by_month_and_type(solved_data)


def plot_pie_charts(solved_data: pd.DataFrame):
    agg_all = solved_data.groupby("type")[["expense"]].sum().reset_index()

    fig = make_subplots(
        rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]]
    )
    fig.add_trace(go.Pie(labels=agg_all["type"], values=agg_all["expense"]), 1, 1)

    agg_filtered = (
        solved_data[solved_data["solution"] == 1]
        .groupby("type")[["expense"]]
        .sum()
        .reset_index()
    )

    fig.add_trace(
        go.Pie(labels=agg_filtered["type"], values=agg_filtered["expense"]), 1, 2
    )

    fig.update_traces(hole=0.4, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="Expenses distribution in solution",
        # Add annotations in the center of the donut pies.
        annotations=[
            dict(text="Original", x=0.17, y=0.5, font_size=20, showarrow=False),
            dict(text="Optimized", x=0.84, y=0.5, font_size=20, showarrow=False),
        ],
    )
    fig.show()


def plot_sunbirst_charts(solved_data: pd.DataFrame):
    sb1 = px.sunburst(solved_data, values="expense", path=["type", "entity"])._data

    sb2 = px.sunburst(
        solved_data[solved_data["solution"] == 1],
        values="expense",
        path=["type", "entity"],
    )._data

    # use data and structure FROM sb1 and sb2 (trick)

    fig = make_subplots(
        rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]]
    )

    fig.add_trace(
        go.Sunburst(
            branchvalues="total",
            labels=sb1[0]["labels"],
            parents=sb1[0]["parents"],
            values=sb1[0]["values"],
        ),
        1,
        1,
    )

    fig.add_trace(
        go.Sunburst(
            branchvalues="total",
            labels=sb2[0]["labels"],
            parents=sb2[0]["parents"],
            values=sb2[0]["values"],
        ),
        1,
        2,
    )

    fig.update_layout(
        title_text="Expenses distribution in solution, sunbirst chart",
        # Add annotations in the center of the donut pies.
        annotations=[
            dict(text="Original", x=0.17, y=1.1, font_size=20, showarrow=False),
            dict(text="Optimized", x=0.84, y=1.1, font_size=20, showarrow=False),
        ],
    )
    # fig = go.Figure(data = [trace1, trace2], layout = layout)
    fig.show()


def plot_bar_plots(solved_data: pd.DataFrame):
    balance = solved_data.groupby(["month"]).sum().reset_index()
    balance["balance"] = balance["Credit"] + balance["Debit"]
    balance["color"] = np.where(balance["balance"] < 0, "Negative", "Positive")
    balance["savings"] = balance["balance"].cumsum()
    balance["data_type"] = "original"

    balance_optimized = (
        solved_data[solved_data["solution"] == 1].groupby(["month"]).sum().reset_index()
    )
    balance_optimized["balance"] = (
        balance_optimized["Credit"] + balance_optimized["Debit"]
    )
    balance_optimized["color"] = np.where(
        balance_optimized["balance"] < 0, "Negative", "Positive"
    )
    balance_optimized["savings"] = balance_optimized["balance"].cumsum()
    balance_optimized["data_type"] = "optimized"

    balance = pd.concat([balance, balance_optimized])

    fig = px.bar(
        balance,
        x="month",
        y="balance",
        color="color",
        facet_col="data_type",
        barmode="stack",
        labels={"color": "Balance", "balance": "Balance [EUR]", "month": "Month"},
        title=f"Monthly balance",
        height=400,
    )

    fig.show()
    fig = px.bar(
        balance,
        x="month",
        y="Debit",
        labels={"Debit": "Total expenses [EUR]", "month": "Month"},
        facet_col="data_type",
        color="data_type",
        color_discrete_sequence=["red", "green"],
        title=f"Total Expenses by month",
        barmode="group",
        height=400,
    )
    fig.show()

    fig = px.area(
        balance,
        x="month",
        y="savings",
        labels={"savings": "Savings [EUR]", "month": "Month"},
        facet_col="data_type",
        color="data_type",
        color_discrete_sequence=["red", "green"],
        title=f"Savings trend",
    )
    fig.show()


def plot_expense_by_month_and_type(solved_data: pd.DataFrame):
    grouped_all = solved_data.groupby(["month", "type"]).sum().reset_index()
    grouped_all["data_type"] = "original"
    grouped_optimized = (
        solved_data[solved_data["solution"] == 1]
        .groupby(["month", "type"])
        .sum()
        .reset_index()
    )
    grouped_optimized["data_type"] = "optimized"
    grouped = pd.concat([grouped_all, grouped_optimized])
    fig = px.bar(
        grouped,
        x="month",
        y="Debit",
        facet_col="data_type",
        color="type",
        barmode="group",
        labels={
            "type": "Transaction type",
            "month": "Month",
            "Debit": "Expenses [EUR]",
        },
        title=f"Total Expenses by month and type",
        height=400,
    )
    fig.show()


def plot_grocery_bar_chart(solved_data: pd.DataFrame, grocery_threshold=None):
    grocery_data_original = (
        solved_data[solved_data["type"] == "grocery"]
        .groupby(["week"])
        .sum()
        .reset_index()
    )
    grocery_data_original["data_type"] = "original"
    grocery_data_optimized = (
        solved_data[(solved_data["type"] == "grocery") & (solved_data["solution"] == 1)]
        .groupby(["week"])
        .sum()
        .reset_index()
    )
    grocery_data_optimized["data_type"] = "optimized"
    grocery_data = pd.concat([grocery_data_original, grocery_data_optimized])

    fig = px.bar(
        grocery_data,
        x="week",
        y="Debit",
        labels={"Debit": "Grocery expenses [EUR]", "week": "Week"},
        facet_col="data_type",
        color="data_type",
        color_discrete_sequence=["red", "green"],
        title=f"Weekly grocery Expenses vs threshold",
        barmode="group",
        height=400,
    )
    if grocery_threshold:
        shapes = [
            {
                "type": "line",
                "x0": 0,
                "y0": -grocery_threshold,
                "x1": 52,
                "y1": -grocery_threshold,
                "xref": "x1",
                "yref": "y1",
            },
            {
                "type": "line",
                "x0": 0,
                "y0": -grocery_threshold,
                "x1": 52,
                "y1": -grocery_threshold,
                "xref": "x2",
                "yref": "y2",
            },
        ]
        fig["layout"].update(shapes=shapes)

    fig.show()

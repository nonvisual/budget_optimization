import plotly.express as px
import pandas as pd
import numpy as np


def visualize_data(transactions: pd.DataFrame, year=2019):
    verify_data(transactions)
    selected_year = transactions[transactions["year"] == year].copy()
    transactions["expense"] = abs(selected_year["Debit"])

    balance = selected_year.groupby(["month"]).sum().reset_index()
    balance["balance"] = balance["Credit"] + balance["Debit"]
    balance["color"] = np.where(balance["balance"] < 0, "Negative", "Positive")
    balance["savings"] = balance["balance"].cumsum()

    fig = px.pie(
        transactions,
        values="expense",
        names="type",
        title=f"Ratio of expenses by type in year {year}",
        hole=0.3,
    )
    fig.show()

    fig = px.bar(
        balance,
        x="month",
        y="balance",
        color="color",
        barmode="stack",
        labels={"color": "Balance", "balance": "Balance [EUR]", "month": "Month"},
        title=f"Monthly balance in year {year}",
        height=400,
    )
    fig.show()

    fig = px.bar(
        balance,
        x="month",
        y="Debit",
        labels={"Debit": "Total expenses [EUR]", "month": "Month"},
        title=f"Total Expenses by month in year {year}",
        barmode="group",
        height=400,
    )
    fig.show()

    grouped_month_type = selected_year.groupby(["month", "type"]).sum().reset_index()

    fig = px.bar(
        grouped_month_type,
        x="month",
        y="Debit",
        color="type",
        barmode="group",
        labels={
            "type": "Transaction type",
            "month": "Month",
            "Debit": "Expenses [EUR]",
        },
        title=f"Total Expenses by month and type in year {year}",
        height=400,
    )
    fig.show()

    grouped_week = selected_year.groupby(["week"]).sum().reset_index()

    fig = px.bar(
        grouped_week,
        x="week",
        y="Debit",
        labels={"savings": "Expenses [EUR]", "week": "Week"},
        color_discrete_sequence=["green"],
        title=f"Expenses by calendar week for year {year}",
    )
    fig.show()
    fig = px.area(
        balance,
        x="month",
        y="savings",
        labels={"savings": "Savings [EUR]", "month": "Month"},
        color_discrete_sequence=["green"],
        title=f"Savings trend for year {year}",
    )
    fig.show()


def verify_data(transactions: pd.DataFrame):
    necessary_columns = ["year", "month", "week", "weekday", "Debit", "Credit", "type"]
    assert all(
        n in transactions.columns for n in necessary_columns
    ), f"Dataframe columns {transactions.columns}, necessary columns are not there {necessary_columns}"

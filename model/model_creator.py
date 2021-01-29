import pulp
import pandas as pd


def create_model(data: pd.DataFrame, savings: float, grocery_per_week: float):
    total_expenditure = abs(data.sum()["Debit"])
    model = pulp.LpProblem("Profit_maximizing_problem", pulp.constants.LpMaximize)
    decision_vars = pulp.LpVariable.dicts(
        "Transaction", data.index, 0, 1, pulp.LpInteger
    )
    objective = pulp.lpSum(
        [decision_vars[t] * data.loc[t, "importance"] for t in data.index]
    )
    model += objective

    savings_constraint = (
        pulp.lpSum([decision_vars[t] * abs(data.loc[t, "Debit"]) for t in data.index])
        <= (1 - savings) * total_expenditure
    )
    model += savings_constraint

    for t in data.index:
        if data.loc[t, "type"] == "rent":
            model += decision_vars[t] == 1

    agg_per_week = data[data["type"] == "grocery"].groupby("week").sum()
    for w in agg_per_week.index:
        week_grocery_spending = abs(agg_per_week.loc[w, "Debit"])
        summed = sum(
            [
                abs(data.loc[t, "Debit"])
                if (data.loc[t, "week"] == w) and (data.loc[t, "type"] == "grocery")
                else 0.0
                for t in data.index
            ]
        )
        model += pulp.lpSum(
            [
                decision_vars[t] * abs(data.loc[t, "Debit"])
                if (data.loc[t, "week"] == w) and (data.loc[t, "type"] == "grocery")
                else 0.0
                for t in data.index
            ]
        ) >= min(week_grocery_spending, grocery_per_week)

    return model, decision_vars

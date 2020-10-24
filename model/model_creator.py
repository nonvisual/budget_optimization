import pulp 
import pandas as pd

def create_model(data:pd.DataFrame, savings:float, grocery_per_week:float):
    total_expenditure = data.sum()['amount']

    model = pulp.LpProblem("Profit_maximizing_problem", -1)
    decision_vars = pulp.LpVariable.dicts("Transaction", range(len(data)), 0, 1, pulp.LpInteger)
    model += pulp.lpSum([decision_vars[t] * data.loc[t, 'importance'] for t in range(len(data))])
    model += pulp.lpSum([decision_vars[t] * data.loc[t, 'amount'] for t in range(len(data))]) <= (
                1 - savings) * total_expenditure
    model+=pulp.lpSum([decision_vars[t] if data.loc[t,'type'] == 3 else 0.0 for t in range(len(data))]) >= 12
    agg_per_week = data[data['type'] == 1].groupby('week').sum()

    for w in range(52):
        if w in agg_per_week.index:
            week_grocery_spending = agg_per_week.loc[w, 'amount']
            model += pulp.lpSum([decision_vars[t] * data.loc[t, 'amount'] \
                                     if data.loc[t, 'week'] == w else 0.0 for t in range(len(data))]) \
                     >= min(week_grocery_spending, grocery_per_week)

    return model, decision_vars
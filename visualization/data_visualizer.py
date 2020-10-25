import matplotlib.pyplot as plt
import numpy as np


def visualize_data(data):
    types = ["grocery", "fashion", "household", "online shopping", "travels"]
    summed = data.groupby(["type"]).sum().reset_index()
    plt.pie(
        summed["amount"], labels=np.take(types, summed["type"] - 1), autopct="%1.1f%%"
    )
    plt.title("My Expenses")
    plt.axis("equal")
    plt.show()
    print(f"Total expenses for the year are {data.sum()['amount']} Euros")

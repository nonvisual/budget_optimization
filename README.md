# budget_optimization
Toy Operations Research project for bank account expenses optimization for learning purposes

The code demonstrates how to use
* PuLP and CBC for optimization
* Plotly for data visualization
* ipywidgets for interactive notebooks
* numpy, pandas for data preparation


## Code structure
**Data** contains functions for mock data generation
**Model** contains all code related to the optimization model creation and solving
**Preparation** contains logic necessary for data preparation and cleaning
**Visualization** contains all plotting code

The main entry point for this simple application is Bank_account_optimization.ipynb.

## How to execute
First of all, one need to install all requirements (better to use virtual environment):
```
pip install -r requirements.txt
```
Then you just need to run the notebook:
1. Execute in terminal
```
jupyter notebook
```
2. Navigate to the directory containing the notebook Bank_account_optimization.ipynb
3. Run all cells

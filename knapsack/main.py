import os
import sys
import argparse
import json
import pandas as pd
from pyomo.environ import *

# --------------------------------------------------
# Knapsack Optimization Script
# --------------------------------------------------
# This script solves the knapsack optimization problem using Pyomo.
# Given a JSON file with item weights, values, and the knapsack's 
# maximum capacity, it runs an optimization to maximize the total value 
# of selected items without exceeding the capacity.
# The results are saved to an Excel file that lists the selected items 
# along with their weights and values.
#
# Dependencies:
# - Python packages: pyomo, pandas, json
# - Solver: GLPK (or another solver compatible with Pyomo)
#
# How to use:
# - Provide a path to a JSON input file via the `--input` argument.
# - The script will output an Excel file in the `outputs` folder.
# --------------------------------------------------

# -----------------------------------------------
# General Setup and Configuration
# -----------------------------------------------

# Avoid creating .pyc files
sys.dont_write_bytecode = True

# Directories setup (using relative paths for compatibility)
root_folder_path = os.getcwd()
setup_folder_path = os.path.join(root_folder_path, 'setup')  # Setup folder
outputs_folder_path = os.path.abspath(os.path.join(root_folder_path, '..', 'outputs')) # Outputs folder

# Ensure the output directory exists
if not os.path.exists(outputs_folder_path):
    os.makedirs(outputs_folder_path)

# Solver parameters
solvername = 'glpk'  # Solver name (using GLPK as default)
solver_path = os.path.join(setup_folder_path, "winglpk-4.65", "glpk-4.65", "w64", "glpsol")


# -----------------------------------------------
# Main Optimization Function
# -----------------------------------------------

def main(input_file):
    """
    This function performs the knapsack optimization using the input data provided
    in a JSON file. It uses the Pyomo optimization library to solve the problem.
    """
    
    # Load data from JSON input file
    with open(input_file, "r") as f:
        data = json.load(f)

    # Extract capacity and item data
    max_capacity = data["capacity"]
    items = data["items"]

    # Prepare data for Pyomo
    num_items = len(items)
    weights = {i + 1: item["weight"] for i, item in enumerate(items)}
    values = {i + 1: item["value"] for i, item in enumerate(items)}

    # Create Pyomo model
    model = ConcreteModel()

    # Define the set of items
    model.item_indexes = RangeSet(num_items)

    # Define the weight and value parameters
    model.weight = Param(model.item_indexes, initialize=weights)
    model.value = Param(model.item_indexes, initialize=values)

    # Define the knapsack capacity
    model.capacity = max_capacity

    # Define decision variables (1 if the item is selected, 0 otherwise)
    model.x = Var(model.item_indexes, domain=Binary)

    # Objective function: maximize the total value
    model.objective = Objective(
        expr=sum(model.value[i] * model.x[i] for i in model.item_indexes),
        sense=maximize
    )

    # Constraint: the total weight must not exceed the capacity
    def capacity_constraint_rule(model):
        return sum(model.weight[i] * model.x[i] for i in model.item_indexes) <= model.capacity

    model.constraint = Constraint(rule=capacity_constraint_rule)

    # Solve the model using the specified solver
    opt = SolverFactory(solvername, executable=solver_path, validate=False)

    results = opt.solve(model)

    # Extract selected items
    chosen_items = [i for i in model.item_indexes if model.x[i].value == 1]

    # Prepare the results in a DataFrame
    chosen_objects = [
        {"item": i, "weight": weights[i], "value": values[i]} for i in chosen_items
    ]
    df = pd.DataFrame(chosen_objects)

    # Save the results to an Excel file
    output_path = os.path.join(outputs_folder_path, 'chosen_items.xlsx')  
    df.to_excel(output_path, index=False)

    print(f"{len(chosen_items)} items selected. Results saved to '{output_path}'.")


# -----------------------------------------------
# Script Execution Entry Point
# -----------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Knapsack optimization script")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input JSON file containing knapsack data"
    )
    args = parser.parse_args()
    main(args.input)
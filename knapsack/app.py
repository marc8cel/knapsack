import streamlit as st
import pandas as pd
import os
import json
from subprocess import call

# --------------------------------------------------
# Streamlit UI for the Knapsack Optimization Problem
# --------------------------------------------------
# This script provides a user-friendly interface to solve the knapsack problem.
# Users can define item values, weights, and the maximum capacity of the knapsack.
# The optimization process runs a backend script (`main.py`) and outputs results
# as a downloadable Excel file.
#
# Dependencies:
# - Python packages: streamlit, pandas, json
# - Backend script: main.py
# --------------------------------------------------

# Title of the application
st.title("Knapsack Optimization")

# -------------------------------
# Context and Rules Section
# -------------------------------
with st.expander("Contexte et règles", expanded=False):
    st.markdown("""
    ### Problème du sac à dos
    L'objectif est de maximiser la valeur totale des objets sélectionnés tout en respectant une limite de poids.

    #### Comment utiliser l'application :
    1. **Définissez le nombre d'objets et la capacité maximale du sac à dos.**
    2. **Renseignez la valeur et le poids de chaque objet.**
    3. **Lancez l'optimisation pour sélectionner les objets optimaux.**

    #### Notes :
    - Les poids et valeurs des objets ne peuvent pas être négatives
    - Il n'est pas possible de sélectionner plusieurs fois le même objet.
    - Les résultats sont téléchargeables sous forme de fichier Excel.
    
    """)

# -------------------------------
# Input Parameters
# -------------------------------
st.header("Paramètres d'entrée")

# Number of items and maximum capacity
num_items = st.number_input("Nombre d'objets", min_value=1, step=1)
capacity = st.number_input("Capacité maximale du sac à dos", min_value=1, step=1)

# -------------------------------
# Item Details
# -------------------------------
st.subheader("Détails des objets")
items = []

for i in range(num_items):
    col1, col2 = st.columns(2)
    with col1:
        value = st.number_input(f"Valeur de l'objet {i + 1}", key=f"value_{i}", min_value=0, step=1, format="%d")
    with col2:
        weight = st.number_input(f"Poids de l'objet {i + 1}", key=f"weight_{i}", min_value=1, step=1, format="%d")
    items.append({"value": value, "weight": weight})


# -------------------------------
# Optimization Execution
# -------------------------------
if st.button("Lancer l'optimisation"):
    
    # Check for duplicate items
    items_values = [(item["value"], item["weight"]) for item in items]
    duplicate_found = False
    unique_items = set()

    
    for idx, (value, weight) in enumerate(items_values):
        if (value, weight) in unique_items:
            st.error(f"Erreur : L'objet {idx + 1} a des valeurs identiques à un autre objet. Veuillez les modifier.")
            duplicate_found = True
            break
        unique_items.add((value, weight))
    
    if duplicate_found:
        st.stop()  # Stop execution if a duplicate is found

    with st.spinner("Exécution en cours, veuillez patienter..."):
        # Generate input data in JSON format
        input_data = {
            "num_items": num_items,
            "capacity": capacity,
            "items": items
        }

        # Save input data as a JSON file
        current_dir = os.path.dirname(__file__)  # Current script's directory
        json_file_path = os.path.abspath(os.path.join(current_dir, "input.json"))

        with open(json_file_path, "w") as json_file:
            json.dump(input_data, json_file, indent=2)

        # Call the main optimization script
        main_script_path = os.path.abspath(os.path.join(current_dir, "main.py"))
        call(['python', main_script_path, '--input', json_file_path])

        # Display results
        try:
            output_path = os.path.join(os.getcwd(), '..', 'outputs', 'chosen_items.xlsx')
            results = pd.read_excel(output_path)

            if results.empty:
                st.error("Aucun objet n'a été sélectionné. Cela signifie probablement que tous les objets dépassent la capacité maximale du sac.")
            else:
                st.write("Objets sélectionnés :")
                st.dataframe(results)

                # Download Excel file
                with open(output_path, "rb") as file:
                    st.download_button("Télécharger le fichier Excel", file, file_name="results.xlsx")

        except FileNotFoundError:
            st.error("Le fichier de résultats n'a pas été trouvé. Assurez-vous que le script d'optimisation s'est exécuté correctement.")
        except Exception as e:
            st.error(f"Une erreur inattendue est survenue : {e}")
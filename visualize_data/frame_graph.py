import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def create_frame_graph(measurement_csv, variable_of_interest, destination_folder=".", x_axis="frames"):
    measurement_df = pd.read_csv(measurement_csv)
    #x_y_data = df[[variable_of_interest, y_axis]].dropna().sort_values(variable_of_interest)
    y_values = measurement_df[variable_of_interest]
    x_values = measurement_df[x_axis]










    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(x_values, y_values)

    title = str(variable_of_interest) + " vs " + str(x_axis)

    ax.set_xlabel(x_axis)
    ax.set_ylabel(variable_of_interest)
    ax.set_title(title)

    
    figure_path = str(destination_folder) + "/" + title 

    plt.savefig(figure_path,dpi=150)

#create_frame_graph("./F5.0_K0.5_theta0.0_measurements.csv", "Rg")

def run_for_all_columns(measurement_csv):
    measurement_df = pd.read_csv(measurement_csv)
    columns = measurement_df.columns.tolist()
    for column in columns:
        create_frame_graph(measurement_csv, column)

run_for_all_columns("./F5.0_K0.5_theta0.0_measurements.csv")

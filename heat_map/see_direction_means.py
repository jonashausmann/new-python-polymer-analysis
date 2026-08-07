import pandas as pd

def save_direction_means(parameter_averages_csv, new_csv_name):
    df = pd.read_csv(parameter_averages_csv)

    theta_zero_df = df[["direction_mean","F","K","theta"]]
    #theta_zero_df = df[(df["theta"]==0)][["direction_mean","F","K","theta"]]
    theta_zero_df.to_csv(new_csv_name, index=False)

save_direction_means("./parameter_averages.csv", "./theta_zero_direction_means.csv")

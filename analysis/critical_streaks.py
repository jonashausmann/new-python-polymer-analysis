import numpy as np
import pandas as pd

from . import parameters


def count_critical_value_streak_greater_than(
    measurement_df, critical_variable, critical_value
):
    df = measurement_df  # pd.read_csv(measurement_df)
    frames = int(parameters.nLoop / parameters.pInterval)
    frame = 0
    streak = 0
    streaks = []

    while frame < frames:
        frame_df = df[(df["frames"] == frame)]
        if float(frame_df[critical_variable].iloc[0]) >= critical_value:
            if len(streaks) != 0:
                streak = streak + 1
            else:
                streak = 1
        else:
            streak = 0
        streaks.append(streak)
        frame = frame + 1
    streak_name = critical_variable + "_over_" + str(critical_value) + "_streak"
    df[streak_name] = streaks
    return df


def count_critical_value_streak_less_than(
    measurement_df, critical_variable, critical_value
):
    df = measurement_df  # pd.read_csv(measurement_df)
    frames = int(parameters.nLoop / parameters.pInterval)
    frame = 0
    streak = 0
    streaks = []

    while frame < frames:
        frame_df = df[(df["frames"] == frame)]
        if float(frame_df[critical_variable].iloc[0]) <= critical_value:
            if len(streaks) != 0:
                streak = streak + 1
            else:
                streak = 1
        else:
            streak = 0
        streaks.append(streak)
        frame = frame + 1
    streak_name = critical_variable + "_under_" + str(critical_value) + "_streak"
    df[streak_name] = streaks
    return df

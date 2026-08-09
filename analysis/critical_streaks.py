import numpy as np
import pandas as pd

from . import parameters


def _consecutive_streak(condition):
    # Running count of consecutive True values ending at each frame:
    # resets to 0 on a False frame, increments by 1 on each True frame.
    idx = np.arange(len(condition))
    last_reset = np.maximum.accumulate(np.where(~condition, idx, -1))
    return np.where(condition, idx - last_reset, 0).astype(int)


def count_critical_value_streak_greater_than(
    measurement_df, critical_variable, critical_value
):
    df = measurement_df  # pd.read_csv(measurement_df)
    condition = df[critical_variable].to_numpy() >= critical_value
    streak_name = critical_variable + "_over_" + str(critical_value) + "_streak"
    df[streak_name] = _consecutive_streak(condition)
    return df


def count_critical_value_streak_less_than(
    measurement_df, critical_variable, critical_value
):
    df = measurement_df  # pd.read_csv(measurement_df)
    condition = df[critical_variable].to_numpy() <= critical_value
    streak_name = critical_variable + "_under_" + str(critical_value) + "_streak"
    df[streak_name] = _consecutive_streak(condition)
    return df

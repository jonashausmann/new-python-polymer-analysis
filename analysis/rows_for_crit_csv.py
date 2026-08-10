import numpy as np
import pandas as pd


def create_crit_over_row(
    measurement_df, crit_variable, crit_value, reg_values, row_dict
):
    df = measurement_df

    for reg_val in reg_values:
        mean_value_name = (
            "mean_"
            + reg_val
            + "_when_"
            + crit_variable
            + "_greaterthan_"
            + str(crit_value)
        )
        max_value_name = (
            "max_"
            + reg_val
            + "_when_"
            + crit_variable
            + "_greaterthan_"
            + str(crit_value)
        )
        var_mean = df[df[crit_variable] >= crit_value][crit_variable].mean()
        var_max = df[df[crit_variable] >= crit_value][crit_variable].max()
        row_dict.setdefault(mean_value_name, []).append(var_mean)
        row_dict.setdefault(max_value_name, []).append(var_max)
    return row_dict


def create_crit_under_row(
    measurement_df, crit_variable, crit_value, reg_values, row_dict
):
    df = measurement_df

    for reg_val in reg_values:
        mean_value_name = (
            "mean_"
            + reg_val
            + "_when_"
            + crit_variable
            + "_lessthan_"
            + str(crit_value)
        )
        min_value_name = (
            "min_" + reg_val + "_when_" + crit_variable + "_lessthan_" + str(crit_value)
        )
        var_mean = df[df[crit_variable] <= crit_value][reg_val].mean()
        var_min = df[df[crit_variable] <= crit_value][reg_val].min()
        row_dict.setdefault(mean_value_name, []).append(var_mean)
        row_dict.setdefault(min_value_name, []).append(var_min)
    return row_dict

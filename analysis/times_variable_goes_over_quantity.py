def count_surpass_critical_value(value, critical_point, measurements_csv, debug=False):
    if debug:
        print(f"Counting times {value} is over {critical_point}")

    measurement_df = measurements_csv  # pd.read_csv(measurements_csv)

    amount_of_times = (measurement_df[value] >= critical_point).sum()
    value_count_string = value + "_times_over_" + str(critical_point)

    return value_count_string, amount_of_times


def count_under_critical_value(value, critical_point, measurements_csv, debug=False):
    if debug:
        print(f"Counting times {value} is under {critical_point}")
    measurement_df = measurements_csv  # pd.read_csv(measurements_csv)
    amount_of_times = (measurement_df[value] <= critical_point).sum()
    value_count_string = value + "_times_under_" + str(critical_point)
    return value_count_string, amount_of_times

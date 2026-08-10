import numpy as np

# from . import parameters


def find_angle_between(measurement_df, coordinate_df, critical_monomer=2, debug=False):
    debugExtraTrue = False
    if debug:
        print("Calculating angle between head and tail")

    #    frames = parameters.nLoop / parameters.pInterval
    frames = 5000
    frame = 0
    df = measurement_df

    tail_rows = []
    tail_head_angle_diff_row = []
    max_neighbor_diff = []
    while frame < frames:
        head_degrees = df[(df["frames"] == frame)]["degrees"].iloc[0]
        x_1_tail = coordinate_df[
            (coordinate_df["frame"] == frame) & (coordinate_df["monomernumber"] == 50)
        ]["xcoord"]
        y_1_tail = coordinate_df[
            (coordinate_df["frame"] == frame) & (coordinate_df["monomernumber"] == 50)
        ]["ycoord"]
        x_2_tail = coordinate_df[
            (coordinate_df["frame"] == frame) & (coordinate_df["monomernumber"] == 49)
        ]["xcoord"]
        y_2_tail = coordinate_df[
            (coordinate_df["frame"] == frame) & (coordinate_df["monomernumber"] == 49)
        ]["ycoord"]

        x = float(x_2_tail.iloc[0]) - float(x_1_tail.iloc[0])
        y = float(y_2_tail.iloc[0]) - float(y_1_tail.iloc[0])
        tail_theta = np.arctan2(y, x)
        tail_degrees = (tail_theta * 180) / np.pi
        tail_rows.append(tail_degrees)
        if debugExtraTrue:
            print(
                f"x_1: {x_1_tail}, y_1: {y_1_tail}, x_2_tail: {x_2_tail}, y_2:{y_2_tail} x: {x}, y: {y}, theta: {tail_theta}, head: {head_degrees}, tail: {tail_degrees} "
            )

        tail_head_angle_diff_row.append(head_degrees - tail_degrees)

        max_neighbor_mon = int(
            df.loc[df["frames"] == frame, "max_neighbor_monomer"].iloc[0]
        )
        if debugExtraTrue:
            print(f"Max mon: {max_neighbor_mon}, Critical mon: {critical_monomer}")
        if max_neighbor_mon > critical_monomer:
            if debugExtraTrue:
                print(f"Yes, {max_neighbor_mon} > {critical_monomer}")
            x_1_neigh = coordinate_df[
                (coordinate_df["frame"] == frame)
                & (coordinate_df["monomernumber"] == max_neighbor_mon)
            ]["xcoord"]
            y_1_neigh = coordinate_df[
                (coordinate_df["frame"] == frame)
                & (coordinate_df["monomernumber"] == max_neighbor_mon)
            ]["ycoord"]
            x_2_neigh = coordinate_df[
                (coordinate_df["frame"] == frame)
                & (coordinate_df["monomernumber"] == max_neighbor_mon - 1)
            ]["xcoord"]
            y_2_neigh = coordinate_df[
                (coordinate_df["frame"] == frame)
                & (coordinate_df["monomernumber"] == max_neighbor_mon - 1)
            ]["ycoord"]
            x = float(x_2_neigh.iloc[0]) - float(x_1_neigh.iloc[0])
            y = float(y_2_neigh.iloc[0]) - float(y_1_neigh.iloc[0])
            neigh_theta = np.arctan2(y, x)
            neigh_degrees = (neigh_theta * 180) / np.pi
            degree_diff = head_degrees - neigh_degrees
            max_neighbor_diff.append(degree_diff)
            if debugExtraTrue:
                print(f"max diff: {degree_diff}, max mon: {max_neighbor_mon}")
            if False:
                print(f"Max monomer difference list:{max_neighbor_diff}")
        elif max_neighbor_mon <= 2:
            if debugExtraTrue:
                print(f"Nope, {max_neighbor_mon} < {critical_monomer}")
            max_neighbor_diff.append(np.nan)
        frame = frame + 1

    df["head_minus_max_neighbor_monomer_angle_difference"] = np.array(
        max_neighbor_diff, dtype=float
    )
    df["head_and_tail_angle_diff"] = np.array(tail_head_angle_diff_row, dtype=float)
    df["tail_direction"] = np.array(tail_rows, dtype=float)

    return df

import os
import pathlib

from matplotlib import pyplot as plt
import pandas as pd

import ifcopenshell
from ifcopenshell.ifcgeom import Alignment
from ifcopenshell.alignment_enums import AlignmentHorizontalSegmentType


def synthetic_test(transition_type: str, test_index: int = 1, interactive: bool = False) -> None:
    """
    Load synthetic data from https://github.com/bSI-RailwayRoom/IFC-Rail-Sample-Files
    and plot the provided X,Y coordinates against those calculated by `ifcopenshell`.

    @param transition_type: Transition typ (e.g. `Clothoid`) to load and test
    @param test_index: index of the Alignment With Cant (AWC) Unit Test (UT)
    @param interactive: True to display in jupyter notebook, False to write image to disk
    """
    
    if test_index < 1 or test_index > 8:
        msg = f"Invalid text index '{test_index}' provided. Must be between 1 and 8, inclusive."
        raise IndexError(msg)

    synthetic_path = os.path.join(
        pathlib.Path.home(),
        "src",
        "IFC-Rail-Sample-Files",
        "1_Alignment with Cant (AWC)",
        "UT_AWC_0_(Synthetic_Cases)",
        "Horizontal",
        "SyntheticTestcases",
    )
    type_path = os.path.join(synthetic_path, transition_type)
    test_data = {
        1: f"{transition_type}_100.0_inf_300_1_Meter",
        2: f"{transition_type}_100.0_-inf_-300_1_Meter",
        3: f"{transition_type}_100.0_300_inf_1_Meter",
        4: f"{transition_type}_100.0_-300_-inf_1_Meter",
        5: f"{transition_type}_100.0_1000_300_1_Meter",
        6: f"{transition_type}_100.0_-1000_-300_1_Meter",
        7: f"{transition_type}_100.0_300_1000_1_Meter",
        8: f"{transition_type}_100.0_-300_-1000_1_Meter",
    }
    test_case = test_data[test_index]
    test_title = f"TS{test_index}_{test_data[test_index]}"
    test_path = os.path.join(type_path, test_title)
    test_file = f"{test_case}.ifc"
    test_xlsx = f"TS{test_index}_{test_case}.xlsx"
    in_file = os.path.join(test_path, test_file)
    in_xlsx = os.path.join(test_path, test_xlsx)

    df1 = pd.read_excel(in_xlsx, sheet_name="horizontal 2D x,y", skiprows=2)
    df1.rename(
        columns={
            "Station on alignment": "Station",
            "Seg-specific X-coordinate": "X",
            "Seg-specific Y-coordinate": "Y",
        },
        inplace=True,
    )
    model = ifcopenshell.open(in_file)

    align_entity = model.by_type("IfcAlignment")[0]
    align = Alignment().from_entity(align_entity)

    s = ifcopenshell.geom.settings()
    s.set(s.INCLUDE_CURVES, True)
    xy = align.create_shape(settings=s, use_representation=False, point_interval=2)

    fg, ax = plt.subplots()
    ax.plot(xy[:, 1], xy[:, 2], marker=".", label="IfcOpenShell")
    ax.plot(df1["X"], df1["Y"], label="bSI-RailwayRoom")
    ax.legend()
    ax.set_title(test_file)
    ax.set_title(test_title)
    ax.grid(True, linestyle="-.")

    if interactive:
        plt.show()
    else:
        out_file = os.path.join("out", "png", f"{test_title}.png")
        print(f"[INFO] writing output to {out_file}...")
        plt.savefig(out_file)
        print(f"[INFO] done.")


if __name__ == "__main__":

    synthetic_test(transition_type="Clothoid", test_index=7, interactive=False)
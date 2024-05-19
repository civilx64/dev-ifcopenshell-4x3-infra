from enum import Enum
import os
import pathlib

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

import ifcopenshell
import ifcopenshell.geom as geom


class LayoutTypeEnum(Enum):
    HORIZONTAL = "H"
    VERTICAL = "V"
    CANT = "C"


class SegmentTypeEnum(Enum):
    LINE = "Line"
    CIRCULARARC = "CircularArc"
    CLOTHOID = "Clothoid"
    CUBIC = "Cubic"
    HELMERTCURVE = "HelmertCurve"
    BLOSSCURVE = "BlossCurve"
    COSINECURVE = "CosineCurve"
    SINECURVE = "SineCurve"
    VIENNESEBEND = "VienneseBend"

    CONSTANTGRADIENT = "ConstantGradient"
    PARABOLICARC = "ParabolicArc"

    LINEARTRANSITION = "LinearTransition"
    CONSTANTCANT = "ConstantCant"


def synthetic_test(
    layout_type: LayoutTypeEnum,
    segment_type: SegmentTypeEnum,
    test_index: int = 1,
    interactive: bool = False,
) -> None:
    """
    Load synthetic data from https://github.com/bSI-RailwayRoom/IFC-Rail-Unit-Test-Reference-Code/tree/master/alignment_testset
    and plot the provided X,Y coordinates against those calculated by `ifcopenshell`.

    @param transition_type: Transition typ (e.g. `Clothoid`) to load and test
    @param test_index: index of the Alignment With Cant (AWC) Unit Test (UT)
    @param interactive: True to display in jupyter notebook, False to write image to disk
    """

    if test_index < 1 or test_index > 16:
        msg = f"Invalid text index '{test_index}' provided. Must be between 1 and 16, inclusive."
        raise IndexError(msg)

    layout_name = str.capitalize(layout_type.name)
    layout_tag = f"{layout_name}Alignment"
    base_path = os.path.join(
        pathlib.PurePath("/root"),
        "src",
        "IFC-Rail-Unit-Test-Reference-Code",
        "alignment_testset",
    )

    ifc_path = os.path.join(base_path, "IFC-WithGeneratedGeometry")
    txt_path = os.path.join(
        base_path,
        f"ToolboxProcess-{layout_type.value}",
        layout_tag,
        segment_type.value,
    )

    segment_tag = segment_type.value
    test_data = {
        "Horizontal": {
            1: f"{segment_tag}_100.0_-1000_-300_1_Meter",
            2: f"{segment_tag}_100.0_-300_-1000_1_Meter",
            3: f"{segment_tag}_100.0_-300_-inf_1_Meter",
            4: f"{segment_tag}_100.0_-inf_-300_1_Meter",
            5: f"{segment_tag}_100.0_1000_300_1_Meter",
            6: f"{segment_tag}_100.0_300_1000_1_Meter",
            7: f"{segment_tag}_100.0_300_inf_1_Meter",
            8: f"{segment_tag}_100.0_inf_300_1_Meter",
        },
        "Vertical": {
            1: f"{segment_tag}_100.0_10.0_-0.5_-1.0_1_Meter",
            2: f"{segment_tag}_100.0_10.0_-0.5_0.0_1_Meter",
            3: f"{segment_tag}_100.0_10.0_-1.0_-0.5_1_Meter",
            4: f"{segment_tag}_100.0_10.0_0.0_-0.5_1_Meter",
            5: f"{segment_tag}_100.0_10.0_0.0_0.5_1_Meter",
            6: f"{segment_tag}_100.0_10.0_0.5_0.0_1_Meter",
            7: f"{segment_tag}_100.0_10.0_0.5_1.0_1_Meter",
            8: f"{segment_tag}_100.0_10.0_1.0_0.5_1_Meter",
        },
        "Cant": {
            1: f"{segment_tag}_100.0_-300_-1000_1_Meter-2CS",
            2: f"{segment_tag}_100.0_-300_-inf_1_Meter-2CS",
            3: f"{segment_tag}_100.0_-1000_-300_1_Meter-2CS",
            4: f"{segment_tag}_100.0_-inf_-300_1_Meter-2CS",
            5: f"{segment_tag}_100.0_300_1000_1_Meter-2CS",
            6: f"{segment_tag}_100.0_300_inf_1_Meter-2CS",
            7: f"{segment_tag}_100.0_1000_300_1_Meter-2CS",
            8: f"{segment_tag}_100.0_inf_300_1_Meter-2CS",
            9: f"{segment_tag}_100.0_-300_-1000_1_Meter-H",
            10: f"{segment_tag}_100.0_-300_-inf_1_Meter-H",
            11: f"{segment_tag}_100.0_-1000_-300_1_Meter-H",
            12: f"{segment_tag}_100.0_-inf_-300_1_Meter-H",
            13: f"{segment_tag}_100.0_300_1000_1_Meter-H",
            14: f"{segment_tag}_100.0_300_inf_1_Meter-H",
            15: f"{segment_tag}_100.0_1000_300_1_Meter-H",
            16: f"{segment_tag}_100.0_inf_300_1_Meter-H",
        },
    }
    test_case = test_data[layout_name][test_index]

    txt_file = f"{test_case}.txt"
    in_txt = os.path.join(txt_path, txt_file)

    test_title = f"{layout_tag}_{test_case}"
    test_file = f"GENERATED__{layout_tag}_{test_case}.ifc"

    # cant input files are not exact matches of the calc file names
    if layout_type == LayoutTypeEnum.CANT:
        test_file = f"{test_file[:-6]}.ifc"
    in_file = os.path.join(ifc_path, test_file)

    df1 = pd.read_csv(in_txt, delimiter="\t", skiprows=2, header=None)
    df1 = df1.set_axis(
        [
            "CurveLength",
            "X",
            "Y",
            "Z",
            "BaseCurve",
        ],
        axis="columns",
    )
    model = ifcopenshell.open(in_file)

    if layout_type == LayoutTypeEnum.HORIZONTAL:
        rep_entity_type = "IfcCompositeCurve"
    elif layout_type == LayoutTypeEnum.VERTICAL:
        rep_entity_type = "IfcGradientCurve"
    elif layout_type == LayoutTypeEnum.CANT:
        rep_entity_type = "IfcSegmentedReferenceCurve"

    curve = model.by_type(type=rep_entity_type, include_subtypes=False)[0]
    if curve is None:
        raise ValueError("Alignment representation not found.")

    s = geom.settings()
    s.set("PIECEWISE_STEP_PARAM", 1.0)
    shape = geom.create_shape(s, curve)
    verts = shape.verts
    msg = f"[INFO] Model '{test_file}' is schema '{model.schema_identifier}'."
    if len(verts) == 0:
        msg += f"\n[ERROR] No vertices generated by ifcopenshell.geom.create_shape()."
        print(msg)
    verts = np.array(shape.verts).reshape((-1, 3))
    
    x, y, z = verts.T

    if layout_type == LayoutTypeEnum.HORIZONTAL:
        y_vals = y
        y_calcs = df1["Y"]
    else:
    # elif layout_type == LayoutTypeEnum.VERTICAL:
        y_vals = z
        y_calcs = df1["Z"]

    _, ax = plt.subplots()
    ax.plot(x, y_vals, linewidth=1, linestyle="-", color="red", label="IfcOpenShell")
    ax.plot(
        df1["X"],
        y_calcs,
        linewidth=5,
        color="grey",
        alpha=0.4,
        label="bSI-RailwayRoom",
    )
    ax.legend()
    ax.set_title(test_title)
    if layout_type == LayoutTypeEnum.HORIZONTAL:
        ax.set_xlabel("X (Easting)")
        ax.set_ylabel("Y (Northing)")
    else:
        ax.set_xlabel("Distance along alignment")
        ax.set_ylabel("Z (Height)")
    ax.grid(True, linestyle="-.")

    if interactive:
        plt.show()
    else:
        out_file = os.path.join("out", "png", f"{test_title}.png")
        if not "[ERROR]" in msg:
            print(f"[INFO] writing output to {out_file}...")
            plt.savefig(out_file)

    plt.close()


if __name__ == "__main__":

    for i in range(8):
        synthetic_test(LayoutTypeEnum.HORIZONTAL, SegmentTypeEnum.LINE, i + 1, False)
        synthetic_test(LayoutTypeEnum.HORIZONTAL, SegmentTypeEnum.CIRCULARARC, i + 1, False)
        synthetic_test(LayoutTypeEnum.HORIZONTAL, SegmentTypeEnum.CLOTHOID, i + 1, False)
        synthetic_test(LayoutTypeEnum.HORIZONTAL, SegmentTypeEnum.CUBIC, i + 1, False)
        synthetic_test(LayoutTypeEnum.HORIZONTAL, SegmentTypeEnum.HELMERTCURVE, i + 1, False)
        synthetic_test(LayoutTypeEnum.HORIZONTAL, SegmentTypeEnum.BLOSSCURVE, i + 1, False)
        synthetic_test(LayoutTypeEnum.HORIZONTAL, SegmentTypeEnum.COSINECURVE, i + 1, False)
        synthetic_test(LayoutTypeEnum.HORIZONTAL, SegmentTypeEnum.SINECURVE, i + 1, False)
        synthetic_test(LayoutTypeEnum.HORIZONTAL, SegmentTypeEnum.VIENNESEBEND, i + 1, False)

        synthetic_test(LayoutTypeEnum.VERTICAL, SegmentTypeEnum.CIRCULARARC, i + 1, False)
        # segfault on CLOTHOID
        # synthetic_test(LayoutTypeEnum.VERTICAL, SegmentTypeEnum.CLOTHOID, i + 1, False)
        synthetic_test(LayoutTypeEnum.VERTICAL, SegmentTypeEnum.CONSTANTGRADIENT, i + 1, False)
        synthetic_test(LayoutTypeEnum.VERTICAL, SegmentTypeEnum.PARABOLICARC, i + 1, False)

        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.BLOSSCURVE, i + 1, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.CONSTANTCANT, i + 1, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.COSINECURVE, i + 1, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.HELMERTCURVE, i + 1, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.LINEARTRANSITION, i + 1, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.SINECURVE, i + 1, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.VIENNESEBEND, i + 1, False)

        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.BLOSSCURVE, i + 9, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.CONSTANTCANT, i + 9, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.COSINECURVE, i + 9, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.HELMERTCURVE, i + 9, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.LINEARTRANSITION, i + 9, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.SINECURVE, i + 9, False)
        synthetic_test(LayoutTypeEnum.CANT, SegmentTypeEnum.VIENNESEBEND, i + 9, False)


    print(f"[INFO] done.")

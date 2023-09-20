import pathlib
import os

import ifcopenshell
import ifcopenshell.geom
from ifcopenshell.ifcgeom import Alignment
# from ifcopenshell.ifcgeom.IfcCompositeCurve import IfcCompositeCurve

s= ifcopenshell.geom.settings()

# s.set(s.USE_PYTHON_OPENCASCADE, True)
s.set(s.INCLUDE_CURVES, True)

index = 3
geometry = True

test_name = f"UT_AWC_{index}"
awc_path = os.path.join(
    pathlib.Path.home(),
    "src",
    "IFC-Rail-Sample-Files",
    "1_Alignment with Cant (AWC)",
    test_name,
    "IFC reference files",
    "RC4",
)
if geometry:
    test_file = f"{test_name}.ifc"
else:
    test_file = f"{test_name}_no_geometry.ifc"

lp_path = os.path.join("tests", "data")

# in_file = os.path.join(awc_path, test_file)
in_file = os.path.join(lp_path, "UT_LinearPlacement_2.ifc")

model = ifcopenshell.open(in_file)

align = model.by_type("IfcAlignment")[0]

# clot = model.by_type("IfcClothoid")[0]
# seg = model.by_type("IfcCurveSegment")[0]
# comp_curve_ent = model.by_type("IfcCompositeCurve")[0]

# comp_curve = IfcCompositeCurve(comp_curve_ent)
# comp_curve.convert()


"""
try:
    shp = ifcopenshell.geom.create_shape(s, seg)
    shp
except RuntimeError:
    msg = ifcopenshell.get_log()
    raise RuntimeError(msg)
"""

alignment = Alignment().from_entity(align)
pts = alignment.create_shape(use_representation=False)

print(pts.shape)
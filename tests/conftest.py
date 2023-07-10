import os
import pathlib

import pytest

import ifcopenshell
from ifcopenshell.ifcgeom.IfcAlignmentCant import AlignmentCant


@pytest.fixture(scope="session")
def ut_awc_1_model():
    test_name = "UT_AWC_1"
    awc_path = os.path.join(
        pathlib.Path.home(),
        "src",
        "IFC-Rail-Sample-Files",
        "1_Alignment with Cant (AWC)",
        test_name,
        "IFC reference files",
        "RC4",
    )
    in_file = os.path.join(awc_path, f"{test_name}.ifc")
    model = ifcopenshell.open(in_file)

    yield model


@pytest.fixture(scope="session")
def ut_awc_1_alignment_entity(ut_awc_1_model):
    yield ut_awc_1_model.by_type("IfcAlignment")[0]


@pytest.fixture(scope="session")
def alignment_cant(ut_awc_1_model):
    ent = ut_awc_1_model.by_type("IfcAlignmentCant")[0]
    yield AlignmentCant().from_entity(ent)


@pytest.fixture(scope="session")
def constant_cant_segment(alignment_cant):
    yield alignment_cant.segments[3]


@pytest.fixture(scope="session")
def linear_cant_segment(alignment_cant):
    yield alignment_cant.segments[2]

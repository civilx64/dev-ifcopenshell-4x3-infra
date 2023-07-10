import pytest

from ifcopenshell.ifcgeom.IfcAlignment import Alignment


@pytest.fixture(scope="module")
def alignment(ut_awc_1_alignment_entity):
    al = Alignment().from_entity(ut_awc_1_alignment_entity)
    yield al


class TestAlignment:
    """
    Test calculation of alignment geometry.
    """

    def test_calc_alignment_vertical(self, alignment):
        """
        Alignment shall correctly calculate heights per the vertical alignment data
        """
        pts = alignment.create_shape(use_representation=False)
        assert len(pts) == 521

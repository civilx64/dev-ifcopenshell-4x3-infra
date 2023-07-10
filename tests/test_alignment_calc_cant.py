import pytest

from ifcopenshell.ifcgeom.IfcAlignmentCant import c_on_CONSTANTCANT
from ifcopenshell.ifcgeom.IfcAlignmentCant import c_on_LINEARTRANSITION
from ifcopenshell.ifcgeom.IfcAlignmentCant import AlignmentCantSide
from ifcopenshell.ifcgeom.IfcAlignmentCant import AlignmentCantSegment


class TestCant:
    """
    Test calculation of cant.
    """

    def test_determine_side(self, constant_cant_segment):
        """
        ValueError shall be raised if side of the alignment is not specified properly
        """
        with pytest.raises(ValueError):
            assert c_on_CONSTANTCANT(
                constant_cant_segment, 10.0, "left"
            ) == pytest.approx(1337)

    def test_constant_cant_left(self, constant_cant_segment):
        """
        Amount of cant on a constant segment shall be calculated correctly.
        """
        assert c_on_CONSTANTCANT(
            constant_cant_segment, 10.0, AlignmentCantSide.LEFT
        ) == pytest.approx(-0.063)

    def test_constant_cant_right(self, constant_cant_segment):
        """
        Amount of cant on a constant segment shall be calculated correctly.
        """
        assert c_on_CONSTANTCANT(
            constant_cant_segment, 10.0, AlignmentCantSide.RIGHT
        ) == pytest.approx(0.063)


@pytest.mark.parametrize(
    "u, cant",
    [
        (00.0, 0.00),
        (05.0, 0.004375),
        (10.0, 0.008750),
        (15.0, 0.013125),
        (20.0, 0.017500),
        (25.0, 0.021875),
        (30.0, 0.026250),
        (55.0, 0.048125),
        (60.0, 0.052500),
        (65.0, 0.056875),
        (70.0, 0.061250),
        (72.0, 0.063000),
    ],
)
def test_linear_c_at_distance(linear_cant_segment, u, cant):
    """
    Cant amounts along a linear transition curve shall be calculated correctly
    """
    assert c_on_LINEARTRANSITION(
        segment=linear_cant_segment, u=u, side=AlignmentCantSide.LEFT
    ) == pytest.approx(-cant)
    assert c_on_LINEARTRANSITION(
        segment=linear_cant_segment, u=u, side=AlignmentCantSide.RIGHT
    ) == pytest.approx(cant)

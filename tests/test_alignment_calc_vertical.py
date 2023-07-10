import pytest

from ifcopenshell.ifcgeom.IfcAlignmentVertical import AlignmentVerticalSegment
from ifcopenshell.alignment_enums import AlignmentVerticalSegmentType
from ifcopenshell.ifcgeom import ParabolicArc


@pytest.fixture(scope="module")
def vertical_curve() -> AlignmentVerticalSegment:
    "IR-31358, Des 9826510 Sheet 216 of 324 Ramp 'REN'"
    vc = AlignmentVerticalSegment(
        StartDistAlong=385965.00,
        HorizontalLength=900.0,
        StartHeight=779.9407,
        StartGradient=0.046063,
        EndGradient=-0.040500,
        PredefinedType=AlignmentVerticalSegmentType.PARABOLICARC,
    )
    yield vc


@pytest.fixture(scope="module")
def parabolic_arc(vertical_curve) -> ParabolicArc:
    yield ParabolicArc(segment=vertical_curve)


class TestParabolicArc:
    """
    Test calculation of vertical curve.
    """

    def test_PVC(self, parabolic_arc):
        """
        PVC station and elevation shall be calculated correctly.
        """
        (sta, el) = parabolic_arc.PVC
        assert sta == pytest.approx(385965.00)
        assert el == pytest.approx(779.9407)

    def test_PVI(self, parabolic_arc):
        """
        PVI station and elevation shall be calculated correctly.
        """
        (sta, el) = parabolic_arc.PVI
        assert sta == pytest.approx(386415.00)
        assert el == pytest.approx(800.6689)

    def test_PVT(self, parabolic_arc):
        """
        PVT station and elevation shall be calculated correctly.
        """
        (sta, el) = parabolic_arc.PVT
        assert sta == pytest.approx(386865.00)
        assert el == pytest.approx(782.4439)

    def test_extreme_point(self, parabolic_arc):
        """
        Extreme point (sag or crest) shall be calculated correctly.
        """
        (sta, el) = parabolic_arc.extreme_point
        assert sta == pytest.approx(386443.9187)
        assert el == pytest.approx(790.9708)


@pytest.mark.parametrize(
    "u, elev",
    [
        (035.0, 781.4939),
        (085.0, 783.5085),
        (135.0, 785.2827),
        (185.0, 786.8164),
        (235.0, 788.1096),
        (285.0, 789.1624),
        (335.0, 789.9748),
        (435.0, 790.8781),
        (485.0, 790.9691),
        (735.0, 787.8173),
        (785.0, 786.4656),
        (835.0, 784.8734),
        (885.0, 783.0408),
    ],
)
def test_z_at_distance(parabolic_arc, u, elev):
    """
    Elevations along the vertical curve shall be calculated correctly
    """
    assert parabolic_arc.z_at_distance(u) == pytest.approx(elev)

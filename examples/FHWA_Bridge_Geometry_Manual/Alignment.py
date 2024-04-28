import ifcopenshell
from ifcopenshell.api import run
import math

# creates geometry and business logic segments for horizontal alignment tangent turns
def create_tangent(file,p,dir,length):
    # geometry
    parent_curve = file.createIfcLine(file.createIfcCartesianPoint((0.,0.)),
                                      file.createIfcVector(file.createIfcDirection((1.0,0.0)), 1.0))

    curve_segment = file.createIfcCurveSegment(Transition="CONTSAMEGRADIENT",
                                               Placement=file.createIfcAxis2Placement2D(p, file.createIfcDirection((math.cos(dir),math.sin(dir)))),
                                               SegmentStart=file.createIfcLengthMeasure(0.0),
                                               SegmentLength=file.createIfcLengthMeasure(length),
                                               ParentCurve=parent_curve)

    # business logic
    design_parameters = file.createIfcAlignmentHorizontalSegment(StartPoint=p,StartDirection=dir,SegmentLength=length,PredefinedType="LINE")

    alignment_segment = file.createIfcAlignmentSegment(ifcopenshell.guid.new(),DesignParameters=design_parameters)

    return curve_segment, alignment_segment

# creates geometry and business logic segments for horizontal alignment horizonal curves
def create_hcurve(file,pc,dir,radius,lc):
    # geometry
    sign = radius/abs(radius)
    parent_curve = file.createIfcCircle(file.createIfcAxis2Placement2D(file.createIfcCartesianPoint((0.,0.)),file.createIfcDirection((1.0,0.0))),
                                        abs(radius))

    curve_segment = file.createIfcCurveSegment(Transition="CONTSAMEGRADIENT",
                                               Placement=file.createIfcAxis2Placement2D(pc, file.createIfcDirection((math.cos(dir),math.sin(dir)))),
                                               SegmentStart=file.createIfcLengthMeasure(0.0),
                                               SegmentLength=file.createIfcLengthMeasure(sign*lc),
                                               ParentCurve=parent_curve)

    #business logic
    design_parameters = file.createIfcAlignmentHorizontalSegment(StartPoint=pc,StartDirection=dir,SegmentLength=lc,PredefinedType="CIRCULARARC")

    alignment_segment = file.createIfcAlignmentSegment(ifcopenshell.guid.new(),DesignParameters=design_parameters)

    return curve_segment, alignment_segment
                                                                    
# creates geometry and business logic segments for vertical profile gradient runs
def create_gradient(file,p,slope,length):
    # geometry
    parent_curve = file.createIfcLine(file.createIfcCartesianPoint((0.,0.)),file.createIfcDirection((1.0,0.0)))
    curve_segment = file.createIfcCurveSegment(Transition="CONTSAMEGRADIENT",
                                               Placement=file.createIfcAxis2Placement2D(p, file.createIfcDirection((math.sqrt(1-slope*slope),slope))),
                                               SegmentStart=file.createIfcLengthMeasure(0.0),
                                               SegmentLength=file.createIfcLengthMeasure(length),
                                               ParentCurve=parent_curve)

    #business logic
    design_parameters = file.createIfcAlignmentVerticalSegment(StartDistAlong=file.createIfcLengthMeasure(p.Coordinates[0]),
                                                               HorizontalLength=file.createIfcNonNegativeLengthMeasure(length),
                                                               StartHeight=file.createIfcLengthMeasure(p.Coordinates[1]),
                                                               StartGradient=file.createIfcRatioMeasure(slope),
                                                               EndGradient=file.createIfcRatioMeasure(slope),
                                                               PredefinedType="CONSTANTGRADIENT")

    alignment_segment = file.createIfcAlignmentSegment(ifcopenshell.guid.new(),DesignParameters=design_parameters)

    return curve_segment, alignment_segment

# creates geometry and business logic segments for vertical profile parabolic vertical curves
def create_vcurve(file,p,start_slope,end_slope,length):
    #geometry
    A = 0.0;
    B = start_slope;
    C = (end_slope - start_slope)/(2.0*length)

    parent_curve = file.createIfcPolynomialCurve(file.createIfcAxis2Placement2D(file.createIfcCartesianPoint((0.0,0.0)),file.createIfcDirection((1.0,0.0))),
                                                 [0.0,1.0],
                                                 [A,B,C]);
    curve_segment = file.createIfcCurveSegment(Transition="CONTSAMEGRADIENT",
                                               Placement=file.createIfcAxis2Placement2D(p,file.createIfcDirection((1.0,0.0))),
                                               SegmentStart=file.createIfcLengthMeasure(0.0),
                                               SegmentLength=file.createIfcLengthMeasure(length),
                                               ParentCurve=parent_curve)

    #business logic
    k = (end_slope - start_slope)/length
    design_parameters = file.createIfcAlignmentVerticalSegment(StartDistAlong=file.createIfcLengthMeasure(p.Coordinates[0]),
                                                               HorizontalLength=file.createIfcNonNegativeLengthMeasure(length),
                                                               StartHeight=file.createIfcLengthMeasure(p.Coordinates[1]),
                                                               StartGradient=file.createIfcRatioMeasure(slope),
                                                               EndGradient=file.createIfcRatioMeasure(slope),
                                                               RadiusOfCurvature=1.0/k,
                                                               PredefinedType="PARABOLICARC")

    alignment_segment = file.createIfcAlignmentSegment(ifcopenshell.guid.new(),DesignParameters=design_parameters)

    return curve_segment, alignment_segment

# creates representations for each IfcAlignmentSegment per CT 4.1.7.1.1.4
# https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/concepts/Product_Shape/Product_Geometric_Representation/Alignment_Geometry/Alignment_Geometry_-_Segments/content.html
def create_segment_representations(file,global_placement,segment_axis_subcontext,curve_segments,alignment_segments):
    for curve_segment, alignment_segment in zip(curve_segments,alignment_segments):
        representation_items = [curve_segment]
        axis_representation = file.createIfcShapeRepresentation(segment_axis_subcontext,"Axis","Segment",representation_items)

        representations = [axis_representation]
        product = file.createIfcProductDefinitionShape(Representations=representations)

        algnment_segment.ObjectPlacement = global_placement
        alignment_segment.Representation = product
    return


def main():
    file = ifcopenshell.file(schema="IFC4X3_ADD2")

    project = run("root.create_entity", file, ifc_class="IfcProject", name="FHWA Bridge Geometry Manual Example Alignment")

    geometric_representation_context = run("context.add_context",file,context_type="Model")
    axis_model_representation_subcontext = file.createIfcGeometricRepresentationSubContext(
        ContextIdentifier="Axis",
        ContextType="Model",
        ParentContext=geometric_representation_context,
        TargetView="MODEL_VIEW")

    global_placement = file.createIfcAxis2Placement3D()

    #
    # Define horizontal alignment
    #

    # define key points
    # B.1.4 pg 212
    pob = file.createIfcCartesianPoint((500.,2500.))               # beginning
    pc1 = file.createIfcCartesianPoint((2142.237995, 1436.014820)) # Point of curve (PC),   Curve #1
    pt1 = file.createIfcCartesianPoint((3660.446123, 2050.736173)) # Point of tangent (PT), Curve #1
    pc2 = file.createIfcCartesianPoint((4084.115884, 3889.462938)) # Point of curve (PC),   Curve #2
    pt2 = file.createIfcCartesianPoint((5469.395067, 4847.566310)) # Point of tangent (PT), Curve #2
    pc3 = file.createIfcCartesianPoint((7019.971367, 4638.286073)) # Point of curve (PC),   Curve #3
    pt3 = file.createIfcCartesianPoint((7790.932128, 4006.730765)) # Point of tangent (PT), Curve #3
    poe = file.createIfcCartesianPoint((8480., 2010.))             # ending

    # define tangent runs and curve lengths
    run_1 = 1956.785654
    lc_1 = 1919.222667
    run_2 = 1886.905454
    lc_2 = 1848.115835
    run_3 = 1564.635765
    lc_3 = 1049.119737
    run_4 = 2112.285084

    # define curve radii
    rc_1 = 1000.
    rc_2 = -1250. # negative radius for curves to the right
    rc_3 = -950.

    # bearing of tangents
    angle_1 = math.radians(327.0613)
    angle_2 = math.radians(77.0247)
    angle_3 = math.radians(352.3133)
    angle_4 = math.radians(289.0395)

    # create containers to store the curve segments
    horizontal_curve_segments = []
    horizontal_segments= []

    # Build the horizontal alignment segments

    # POB to PC1
    curve_segment, alignment_segment = create_tangent(file,pob,angle_1,run_1)
    horizontal_curve_segments.append(curve_segment)
    horizontal_segments.append(alignment_segment)

    # Curve 1
    curve_segment, alignment_segment = create_hcurve(file,pc1,angle_1,rc_1,lc_1)
    horizontal_curve_segments.append(curve_segment)
    horizontal_segments.append(alignment_segment)

    # PT1 to PC2
    curve_segment, alignment_segment = create_tangent(file,pt1,angle_2,run_2)
    horizontal_curve_segments.append(curve_segment)
    horizontal_segments.append(alignment_segment)

    # Curve 2
    curve_segment, alignment_segment = create_hcurve(file,pc2,angle_2,rc_2,lc_2)
    horizontal_curve_segments.append(curve_segment)
    horizontal_segments.append(alignment_segment)

    # PT2 to PC3
    curve_segment, alignment_segment = create_tangent(file,pt2,angle_3,run_3)
    horizontal_curve_segments.append(curve_segment)
    horizontal_segments.append(alignment_segment)

    # Curve 3
    curve_segment, alignment_segment = create_hcurve(file,pc3,angle_3,rc_3,lc_3)
    horizontal_curve_segments.append(curve_segment)
    horizontal_segments.append(alignment_segment)

    # PT3 to POE
    curve_segment, alignment_segment = create_tangent(file,pt3,angle_4,run_4)
    horizontal_curve_segments.append(curve_segment)
    horizontal_segments.append(alignment_segment)

    # Zero-length terminator segment
    curve_segment, alignment_segment = create_tangent(file,poe,angle_4,0.0)
    curve_segment.Transition="DISCONTINUOUS"
    horizontal_curve_segments.append(curve_segment)
    horizontal_segments.append(alignment_segment)

    # Create the horizontal alignment and nest the alignment segments
    horizontal_alignment = file.createIfcAlignmentHorizontal(ifcopenshell.guid.new(),Description="Horizontal Alignment")
    nests_horizontal_segments = file.createIfcRelNests(ifcopenshell.guid.new(),
                                                       Description="Nests alignment segments with horizontal alignment",
                                                       RelatingObject=horizontal_alignment,
                                                       RelatedObjects=horizontal_segments)

    #
    # Create plan view footprint model representation for the horizontal alignment
    #
    composite_curve = file.createIfcCompositeCurve(horizontal_curve_segments)
    alignment_representation_items = [composite_curve]
    footprint_shape_representation = file.createIfcShapeRepresentation(axis_model_representation_subcontext,"FootPrint", "Curve2D", alignment_representation_items)

    #
    # Define vertical profile segments
    #

    # create containers to store the curve segments
    vertical_curve_segments = []
    vertical_segments = []

    #define key profile points
    vpob = file.createIfcCartesianPoint((0.0, 100.0))     # beginning
    vpc1 = file.createIfcCartesianPoint((1200.0, 121.0))  # Vertical Curve Point (VPC),   Vertical Curve #1
    vpt1 = file.createIfcCartesianPoint((2800.0, 127.0))  # Vertical Curve Tangent (VPT), Vertical Curve #1
    vpc2 = file.createIfcCartesianPoint((4400.0, 111.0))  # Vertical Curve Point (VPC),   Vertical Curve #2
    vpt2 = file.createIfcCartesianPoint((5600.0, 117.0))  # Vertical Curve Tangent (VPT), Vertical Curve #2
    vpc3 = file.createIfcCartesianPoint((6400.0, 133.0))  # Vertical Curve Point (VPC),   Vertical Curve #3
    vpt3 = file.createIfcCartesianPoint((8400.0, 133.0))  # Vertical Curve Tangent (VPT), Vertical Curve #3
    vpc4 = file.createIfcCartesianPoint((9400.0, 113.0))  # Vertical Curve Point (VPC),   Vertical Curve #4
    vpt4 = file.createIfcCartesianPoint((10200.0, 103.0)) # Vertical Curve Tangent (VPT), Vertical Curve #4
    vpoe = file.createIfcCartesianPoint((12800.0, 90.0))  # ending

    #
    # Build the vertical alignment segments
    #

    # Grade start to VPC1
    curve_segment, alignment_segment = create_gradient(file, vpob, 1.75 / 100., 1200.);
    vertical_curve_segments.append(curve_segment)
    vertical_segments.append(alignment_segment)

    # Vertical Curve 1
    curve_segment, alignment_segment = create_vcurve(file, vpc1, 1.75 / 100., -1.0 / 100, 1600.);
    vertical_curve_segments.append(curve_segment)
    vertical_segments.append(alignment_segment)

    # Grade VPT1 to VPC2
    curve_segment, alignment_segment = create_gradient(file, vpt1, -1.0 / 100., 1600.);
    vertical_curve_segments.append(curve_segment)
    vertical_segments.append(alignment_segment)

    # Vertical Curve 2
    curve_segment, alignment_segment = create_vcurve(file, vpc2, -1.0 / 100., 2.0 / 100, 1200.);
    vertical_curve_segments.append(curve_segment)
    vertical_segments.append(alignment_segment)

    # Grade PVT2 to VPC3
    curve_segment, alignment_segment = create_gradient(file, vpt2, 2.0 / 100., 800.);
    vertical_curve_segments.append(curve_segment)
    vertical_segments.append(alignment_segment)

    # Vertical Curve 3
    curve_segment, alignment_segment = create_vcurve(file, vpc3, 2.0 / 100., -2.0 / 100, 2000.);
    vertical_curve_segments.append(curve_segment)
    vertical_segments.append(alignment_segment)

    # Grade PVT3 to VPC4
    curve_segment, alignment_segment = create_gradient(file, vpt3, -2.0 / 100., 1000.);
    vertical_curve_segments.append(curve_segment)
    vertical_segments.append(alignment_segment)

    # Vertical Curve 4
    curve_segment, alignment_segment = create_vcurve(file, vpc4, -2.0 / 100., -0.5 / 100, 800.);
    vertical_curve_segments.append(curve_segment)
    vertical_segments.append(alignment_segment)

    # Grade VPT4 to End
    curve_segment, alignment_segment = create_gradient(file, vpt4, -0.5 / 100., 2600.);
    vertical_curve_segments.append(curve_segment)
    vertical_segments.append(alignment_segment)

    # Zero-length terminator
    curve_segment, alignment_segment = create_gradient(file, vpoe, -0.5 / 100., 0.0);
    curve_segment.Transition="DISCONTINUOUS"
    vertical_curve_segments.append(curve_segment)
    vertical_segments.append(alignment_segment)

    #
    # Create the vertical alignment (IfcAlignmentVertical) and nest alignemnt segments
    #
    vertical_profile = file.createIfcAlignmentVertical(ifcopenshell.guid.new(), Description="Vertical Alignment")
    nests_vertical_segments = file.createIfcRelNests(ifcopenshell.guid.new(),
                                                     Description="Nests alignment segments with vertical alignment",
                                                     RelatingObject=vertical_alignment,
                                                     RelatedObjects=vertical_segments)

    #
    # Create profile view axis model representation for the vertical profile
    #

    # start by defining a gradient curve composed of the vertical curve segments and associated with the horizontal composite curve
    gradient_curve = file.createIfcGradientCurve(Segments=vertical_curve_segments,
                                                 SelfIntersection=false,
                                                 BaseCurve=composite_curve)

    # the gradient curve is a representation item
    profile_representation_items = [gradient_curve]

    # create the axis representation
    axis3d_shape_representation = file.createIfcShapeRepresentation(axis_model_representation_subcontext, "Axis", "Curve3D", profile_representation_items)

    # create the axis representations
    create_segment_representations(file, global_placement, axis_model_representation_subcontext, horizontal_curve_segments, horizontal_segments)
    create_segment_representations(file, global_placement, axis_model_representation_subcontext, vertical_curve_segments, vertical_segments)

    #
    # Create the IfcAlignment
    #

    # the alignment has two representations, a plan view footprint and a 3d curve
    alignment_representations = [footprint_shape_representation,axis3d_shape_representation]

    # create the alignment product definition
    alignment_product = file.createIfcProductDefinitionShape(Name="Alignment Product Shape Definition",Representations=alignment_representations)

    # create the alignment
    alignment = file.createIfcAlignment(ifcopenshell.guid.new(),Description="Example Alignment",ObjectPlacement=global_placement,Representation=alignment_product)

    # Nest the IfcAlignmentHorizontal and IfcAlignmentVertical with the IfcAlignment to complete the business logic
    # 4.1.4.4.1 Alignments nest horizontal and vertical layouts
    # https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/concepts/Object_Composition/Nesting/Alignment_Layouts/content.html
    alignment_layout_list = [horizontal_alignment,vertical_alignment]
    nests_alignment_layouts = file.createIfcRelNests(ifcopenshell.guid.new(),Description="Nest horizontal and vertical alignment layouts with the alignment",RelatingObject=alignment,RelatedObjects=alignment_layout_list)

    # Define the relationship with the project

    # IFC 4.1.4.1.1 "Every IfcAlignment must be related to IfcProject using the IfcRelAggregates relationship"
    # https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/concepts/Object_Composition/Aggregation/Alignment_Aggregation_To_Project/content.html
    # IfcProject <-> IfcRelAggregates <-> IfcAlignment
    list_of_alignments_in_project = [alignment]
    file.createIfcRelAggregates(ifcopenshell.guid.new(),Description="Alignments in project",RelatingObject=project,RelatedObjects=list_of_alignments_in_project)

    # Define the spatial structure of the alignment with respect to the site

    # IFC 4.1.5.1 alignment is referenced in spatial structure of an IfcSpatialElement. In this case IfcSite is the highest level IfcSpatialElement
    # https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/concepts/Object_Connectivity/Alignment_Spatial_Reference/content.html
    # IfcSite <-> IfcRelReferencedInSpatialStructure <-> IfcAlignment
    # This means IfcAlignment is not part of the IfcSite (it is not an aggregate component) but instead IfcAlignment is used within
    # the IfcSite by reference. This implies an IfcAlignment can traverse many IfcSite instances within an IfcProject
    list_alignments_referenced_in_site = [alignment]

    # this alignment traverse 3 bridge sites
    for i in Range(1,3):
        name = "Site of Bridge %d",i
        site = file.createIfcSite(ifcopenshell.guid.new(),Name=name)
        file.createIfcRelReferencedInSpatialStructure(ifcopenshell.guid.new(),list_alignemnts_referenced_in_site,site)


    # save the model
    file.write("FHWA_Bridge_Geometry_Alignment_Example(py).ifc")



if __name__ == "__main__":
    main()

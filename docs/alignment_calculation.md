# Alignment Geometry Calculation

The implementation of alignment geometry in IfcOpenShell results in
a polyline of points calculated at discrete locations along an alignment.

## Input data

For the purposes of this document we will consider an alignment with the following:

### Horizontal Input

1. Line of length 120.00 m with direction 0 (positive x-axis) and tag `H1`
2. Clothoid transition of length 90.00 m and tag `H2`
3. Circular arc of length 110.00 m and radius 300.00 m and tag `H3`

### Vertical Input

1. Tangent grade of -5.00% beginning at distance 20.00 with start elevation of 95.00 m and tag `V1`
2. Parabolic arc of length 140.00 m beginning at distance 90.00 m and tag `V2`
3. Tangent grade of +2.00% beginning at distance 230.00 m with length 80.000 m and tag `V3`

### Cant Input

(future addition...)

## Calculation procedure

### Distances

First we determine the distance interval at which we would like to calculate the alignment geometry.
For sake of illustration we'll start with 25 m.
We'll also add the end of the horizontal alignment,
which in this case is a distance of 320.000 m.

Our initial dataframe looks like this:

| Distance |
| -------- |
| 0.000    |
| 25.000   |
| 50.000   |
| 75.000   |
| 100.000  |
| 125.000  |
| 150.000  |
| 175.000  |
| 200.000  |
| 225.000  |
| 250.000  |
| 275.000  |
| 300.000  |
| 320.000  |

### Horizontal Mapping

We map the distances to the horizontal segments like so:

| Distance | Horiz. Segment | u on Horiz Segment |
| -------- | -------------- | ------------------ |
| 0.000    | H1             | 0.000              |
| 25.000   | H1             | 25.000             |
| 50.000   | H1             | 50.000             |
| 75.000   | H1             | 75.000             |
| 100.000  | H1             | 100.000            |
| 125.000  | H2             | 5.000              |
| 150.000  | H2             | 30.000             |
| 175.000  | H2             | 55.000             |
| 200.000  | H2             | 85.000             |
| 225.000  | H3             | 15.000             |
| 250.000  | H3             | 40.000             |
| 275.000  | H3             | 65.000             |
| 300.000  | H3             | 90.000             |
| 320.000  | H3             | 110.000            |

We realize that we want to also calculate a point at the beginning of each horizontal segment.
To do this we add additional distances to the array resulting in:

| Distance    | Horiz. Segment | u on Horiz Segment |
| ----------- | -------------- | ------------------ |
| 0.000       | H1             | 0.000              |
| 25.000      | H1             | 25.000             |
| 50.000      | H1             | 50.000             |
| 75.000      | H1             | 75.000             |
| 100.000     | H1             | 100.000            |
| **120.000** | **H2**         | **0.000**          |
| 125.000     | H2             | 5.000              |
| 150.000     | H2             | 30.000             |
| 175.000     | H2             | 55.000             |
| 200.000     | H2             | 85.000             |
| **210.000** | **H3**         | **0.000**          |
| 225.000     | H3             | 15.000             |
| 250.000     | H3             | 40.000             |
| 275.000     | H3             | 65.000             |
| 300.000     | H3             | 90.000             |
| 320.000     | H3             | 110.000            |

Next we do a piecewise mapping to calculate the x,y coordinates of the horizontal alignment.

| Distance | Horiz. Segment | u on Horiz Segment | (x,y)                             |
| -------- | -------------- | ------------------ | --------------------------------- |
| 0.000    | H1             | 0.000              | point_on_LINE(H1, 0.000)          |
| 25.000   | H1             | 25.000             | point_on_LINE(H1, 25.000)         |
| 50.000   | H1             | 50.000             | point_on_LINE(H1, 50.000)         |
| 75.000   | H1             | 75.000             | point_on_LINE(H1, 75.000)         |
| 100.000  | H1             | 100.000            | point_on_LINE(H1, 100.000)        |
| 120.000  | H2             | 0.000              | point_on_CLOTHOID(H2, 0.000)      |
| 125.000  | H2             | 5.000              | point_on_CLOTHOID(H2, 5.000)      |
| 150.000  | H2             | 30.000             | point_on_CLOTHOID(H2, 30.000)     |
| 175.000  | H2             | 55.000             | point_on_CLOTHOID(H2, 55.000)     |
| 200.000  | H2             | 85.000             | point_on_CLOTHOID(H2, 85.000)     |
| 210.000  | H3             | 0.000              | point_on_CIRCULARARC(H3, 0.000)   |
| 225.000  | H3             | 15.000             | point_on_CIRCULARARC(H3, 15.000)  |
| 250.000  | H3             | 40.000             | point_on_CIRCULARARC(H3, 40.000)  |
| 275.000  | H3             | 65.000             | point_on_CIRCULARARC(H3, 65.000)  |
| 300.000  | H3             | 90.000             | point_on_CIRCULARARC(H3, 90.000)  |
| 320.000  | H3             | 110.000            | point_on_CIRCULARARC(H3, 110.000) |

### Vertical Mapping

Next we do a similar step and map the distances to the vertical segments:

| Distance | Horiz. Segment | u on Horiz Segment | (x,y)                             | Vert. Segment | u on Vert Segment |
| -------- | -------------- | ------------------ | --------------------------------- | ------------- | ----------------- |
| 0.000    | H1             | 0.000              | point_on_LINE(H1, 0.000)          | `None`        | `None`            |
| 25.000   | H1             | 25.000             | point_on_LINE(H1, 25.000)         | V1            | 5.000             |
| 50.000   | H1             | 50.000             | point_on_LINE(H1, 50.000)         | V1            | 30.000            |
| 75.000   | H1             | 75.000             | point_on_LINE(H1, 75.000)         | V1            | 55.000            |
| 100.000  | H1             | 100.000            | point_on_LINE(H1, 100.000)        | V2            | 10.000            |
| 120.000  | H2             | 0.000              | point_on_CLOTHOID(H2, 0.000)      | V2            | 30.000            |
| 125.000  | H2             | 5.000              | point_on_CLOTHOID(H2, 5.000)      | V2            | 35.000            |
| 150.000  | H2             | 30.000             | point_on_CLOTHOID(H2, 30.000)     | V2            | 60.000            |
| 175.000  | H2             | 55.000             | point_on_CLOTHOID(H2, 55.000)     | V2            | 85.000            |
| 200.000  | H2             | 85.000             | point_on_CLOTHOID(H2, 85.000)     | V2            | 110.000           |
| 210.000  | H3             | 0.000              | point_on_CIRCULARARC(H3, 0.000)   | V2            | 120.000           |
| 225.000  | H3             | 15.000             | point_on_CIRCULARARC(H3, 15.000)  | V2            | 135.000           |
| 250.000  | H3             | 40.000             | point_on_CIRCULARARC(H3, 40.000)  | V3            | 20.000            |
| 275.000  | H3             | 65.000             | point_on_CIRCULARARC(H3, 65.000)  | V3            | 45.000            |
| 300.000  | H3             | 90.000             | point_on_CIRCULARARC(H3, 90.000)  | V3            | 70.000            |
| 320.000  | H3             | 110.000            | point_on_CIRCULARARC(H3, 110.000) | `None`        | `None`            |

Of course we now want to add additional points for the beginnings and ends of the vertical alignments:

| Distance    | Horiz. Segment | u on Horiz Segment | (x,y)                             | Vert. Segment | u on Vert Segment |
| ----------- | -------------- | ------------------ | --------------------------------- | ------------- | ----------------- |
| 0.000       | H1             | 0.000              | point_on_LINE(H1, 0.000)          | `None`        | `None`            |
| **20.000**  | H1             | 20.000             | point_on_LINE(H1, 20.000)         | **V1**        | **0.000**         |
| 25.000      | H1             | 25.000             | point_on_LINE(H1, 25.000)         | V1            | 5.000             |
| 50.000      | H1             | 50.000             | point_on_LINE(H1, 50.000)         | V1            | 30.000            |
| 75.000      | H1             | 75.000             | point_on_LINE(H1, 75.000)         | V1            | 55.000            |
| **90.000**  | H1             | 90.000             | point_on_LINE(H1, 90.000)         | **V2**        | **0.000**         |
| 100.000     | H1             | 100.000            | point_on_LINE(H1, 100.000)        | V2            | 10.000            |
| 120.000     | H2             | 0.000              | point_on_CLOTHOID(H2, 0.000)      | V2            | 30.000            |
| 125.000     | H2             | 5.000              | point_on_CLOTHOID(H2, 5.000)      | V2            | 35.000            |
| 150.000     | H2             | 30.000             | point_on_CLOTHOID(H2, 30.000)     | V2            | 60.000            |
| 175.000     | H2             | 55.000             | point_on_CLOTHOID(H2, 55.000)     | V2            | 85.000            |
| 200.000     | H2             | 85.000             | point_on_CLOTHOID(H2, 85.000)     | V2            | 110.000           |
| 210.000     | H3             | 0.000              | point_on_CIRCULARARC(H3, 0.000)   | V2            | 120.000           |
| 225.000     | H3             | 15.000             | point_on_CIRCULARARC(H3, 15.000)  | V2            | 135.000           |
| **230.000** | H3             | 20.000             | point_on_CIRCULARARC(H3, 20.000)  | **V3**        | **0.000**         |
| 250.000     | H3             | 40.000             | point_on_CIRCULARARC(H3, 40.000)  | V3            | 20.000            |
| 275.000     | H3             | 65.000             | point_on_CIRCULARARC(H3, 65.000)  | V3            | 45.000            |
| 300.000     | H3             | 90.000             | point_on_CIRCULARARC(H3, 90.000)  | V3            | 70.000            |
| **310.000** | H3             | 100.000            | point_on_CIRCULARARC(H3, 100.000) | **V3**        | **80.000**        |
| 320.000     | H3             | 110.000            | point_on_CIRCULARARC(H3, 110.000) | `None`        | `None`            |

Again, we do a piecewise mapping to calculate the z coordinate at each point:

| Distance | Horiz. Segment | u on Horiz Segment | (x,y)                             | Vert. Segment | u on Vert Segment | z                                 |
| -------- | -------------- | ------------------ | --------------------------------- | ------------- | ----------------- | --------------------------------- |
| 0.000    | H1             | 0.000              | point_on_LINE(H1, 0.000)          | `None`        | `None`            | `None`                            |
| 20.000   | H1             | 20.000             | point_on_LINE(H1, 20.000)         | V1            | 0.000             | h_on_CONSTANTGRADIENT(V1, 0.000)  |
| 25.000   | H1             | 25.000             | point_on_LINE(H1, 25.000)         | V1            | 5.000             | h_on_CONSTANTGRADIENT(V1, 5.000)  |
| 50.000   | H1             | 50.000             | point_on_LINE(H1, 50.000)         | V1            | 30.000            | h_on_CONSTANTGRADIENT(V1, 30.000) |
| 75.000   | H1             | 75.000             | point_on_LINE(H1, 75.000)         | V1            | 55.000            | h_on_CONSTANTGRADIENT(V1, 55.000) |
| 90.000   | H1             | 90.000             | point_on_LINE(H1, 90.000)         | V2            | 0.000             | h_on_PARABOLICARC(V2, 0.000)      |
| 100.000  | H1             | 100.000            | point_on_LINE(H1, 100.000)        | V2            | 10.000            | h_on_PARABOLICARC(V2, 10.000)     |
| 120.000  | H2             | 0.000              | point_on_CLOTHOID(H2, 0.000)      | V2            | 30.000            | h_on_PARABOLICARC(V2, 30.000)     |
| 125.000  | H2             | 5.000              | point_on_CLOTHOID(H2, 5.000)      | V2            | 35.000            | h_on_PARABOLICARC(V2, 35.000)     |
| 150.000  | H2             | 30.000             | point_on_CLOTHOID(H2, 30.000)     | V2            | 60.000            | h_on_PARABOLICARC(V2, 60.000)     |
| 175.000  | H2             | 55.000             | point_on_CLOTHOID(H2, 55.000)     | V2            | 85.000            | h_on_PARABOLICARC(V2, 85.000)     |
| 200.000  | H2             | 85.000             | point_on_CLOTHOID(H2, 85.000)     | V2            | 110.000           | h_on_PARABOLICARC(V2, 110.000)    |
| 210.000  | H3             | 0.000              | point_on_CIRCULARARC(H3, 0.000)   | V2            | 120.000           | h_on_PARABOLICARC(V2, 120.000)    |
| 225.000  | H3             | 15.000             | point_on_CIRCULARARC(H3, 15.000)  | V2            | 135.000           | h_on_PARABOLICARC(V2, 135.000)    |
| 230.000  | H3             | 20.000             | point_on_CIRCULARARC(H3, 20.000)  | V3            | 0.000             | h_on_LINE(V3, 0.000)              |
| 250.000  | H3             | 40.000             | point_on_CIRCULARARC(H3, 40.000)  | V3            | 20.000            | h_on_CONSTANTGRADIENT(V3, 20.000) |
| 275.000  | H3             | 65.000             | point_on_CIRCULARARC(H3, 65.000)  | V3            | 45.000            | h_on_CONSTANTGRADIENT(V3, 45.000) |
| 300.000  | H3             | 90.000             | point_on_CIRCULARARC(H3, 90.000)  | V3            | 70.000            | h_on_CONSTANTGRADIENT(V3, 70.000) |
| 310.000  | H3             | 100.000            | point_on_CIRCULARARC(H3, 100.000) | V3            | 80.000            | h_on_CONSTANTGRADIENT(V3, 80.000) |
| 320.000  | H3             | 110.000            | point_on_CIRCULARARC(H3, 110.000) | `None`        | `None`            | `None`                            |

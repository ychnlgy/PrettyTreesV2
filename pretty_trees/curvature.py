from .geometry import Circle, Point


def computeCurvatureCircle(midThickness: float, endThickness: float) -> Circle:
    return Circle.from3Points(
        Point(x=0, y=1),
        Point(x=0.5, y=midThickness),
        Point(x=1, y=endThickness),
    )

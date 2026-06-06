import math

import pytest

from pretty_trees.geometry import Circle, Point


def testCirclePointsAtAngle():
    c = Circle(
        origin=Point(x=0, y=0),
        radius=1,
    )
    assert c.getPointAtAngle(0) == Point(x=1, y=0)

    p2 = c.getPointAtAngle(math.pi / 2)
    assert p2.x == pytest.approx(0)
    assert p2.y == pytest.approx(1)

    p3 = c.getPointAtAngle(math.pi)
    assert p3.x == pytest.approx(-1)
    assert p3.y == pytest.approx(0)

    p4 = c.getPointAtAngle(3 * math.pi / 2)
    assert p4.x == pytest.approx(0)
    assert p4.y == pytest.approx(-1)

    p5 = c.getPointAtAngle(2 * math.pi)
    assert p5.x == pytest.approx(1)
    assert p5.y == pytest.approx(0)


def testCirclePointsAtAngleWithOffset():
    c = Circle(
        origin=Point(x=1, y=2),
        radius=3,
    )
    p1 = c.getPointAtAngle(0)
    assert p1.x == pytest.approx(4)
    assert p1.y == pytest.approx(2)

    p2 = c.getPointAtAngle(math.pi / 2)
    assert p2.x == pytest.approx(1)
    assert p2.y == pytest.approx(5)

    p3 = c.getPointAtAngle(math.pi)
    assert p3.x == pytest.approx(-2)
    assert p3.y == pytest.approx(2)

    p4 = c.getPointAtAngle(3 * math.pi / 2)
    assert p4.x == pytest.approx(1)
    assert p4.y == pytest.approx(-1)

    p5 = c.getPointAtAngle(2 * math.pi)
    assert p5.x == pytest.approx(4)
    assert p5.y == pytest.approx(2)


def testCreateCircleFromPoints():
    c = Circle.from3Points(
        Point(x=-2, y=2),
        Point(x=4, y=2),
        Point(x=1, y=5),
    )
    assert c.origin.x == pytest.approx(1)
    assert c.origin.y == pytest.approx(2)
    assert c.radius == pytest.approx(3)

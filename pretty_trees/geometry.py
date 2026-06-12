import math
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Point:
    x: float
    y: float

    def asTuple(self) -> tuple[float, float]:
        return (self.x, self.y)


@dataclass(frozen=True, kw_only=True)
class Circle:
    origin: Point
    radius: float

    def getPointAtAngle(self, angle: float) -> Point:
        return Point(
            x=self.origin.x + self.radius * math.cos(angle),
            y=self.origin.y + self.radius * math.sin(angle),
        )

    @staticmethod
    def from3Points(p1: Point, p2: Point, p3: Point) -> "Circle":
        f12 = Circle._calculateFactor(p1, p2)
        f13 = Circle._calculateFactor(p1, p3)
        ratios = (p1.x - p3.x) / (p1.x - p2.x)
        originY = (f13 - f12 * ratios) / (p1.y - p3.y - ratios * (p1.y - p2.y))
        originX = (f12 - (p1.y - p2.y) * originY) / (p1.x - p2.x)
        radius = math.sqrt((p1.x - originX) ** 2 + (p1.y - originY) ** 2)
        return Circle(origin=Point(x=originX, y=originY), radius=radius)

    # === PRIVATE ===

    @staticmethod
    def _calculateFactor(p1: Point, p2: Point) -> float:
        return (p1.x**2 - p2.x**2 + p1.y**2 - p2.y**2) / 2

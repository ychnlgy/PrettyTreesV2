import math
import pathlib
import random


def readFile(path: str | pathlib.Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def cosineInterpolate(a: float, b: float, t: float) -> float:
    """Cosine interpolation between a and b with t in [0, 1]."""
    t2 = (1 - math.cos(t * math.pi)) / 2.0
    return a * (1 - t2) + b * t2


def randVariance(base: float, variance: float) -> float:
    return base + random.uniform(-variance, variance)


def randDecay(base: float, decayRange: tuple[float, float]) -> float:
    minDecay, maxDecay = decayRange
    return base * random.uniform(minDecay, maxDecay)

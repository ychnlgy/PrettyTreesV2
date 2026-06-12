from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Color:
    r: int
    g: int
    b: int
    a: int = 255

    def asTuple(self) -> tuple[int, int, int, int]:
        return self.r, self.g, self.b, self.a

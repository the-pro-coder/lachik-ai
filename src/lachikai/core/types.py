from __future__ import annotations

from dataclasses import dataclass
from math import hypot


@dataclass(frozen=True, slots=True)
class Vector2:
    """An immutable two-dimensional vector."""

    x: float
    y: float

    def __add__(self, other: Vector2) -> Vector2:
        if not isinstance(other, Vector2):
            return NotImplemented
        return Vector2(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other: Vector2) -> Vector2:
        if not isinstance(other, Vector2):
            return NotImplemented
        return Vector2(
            self.x - other.x,
            self.y - other.y,
        )

    def __mul__(self, scalar: float) -> Vector2:
        if not isinstance(scalar, int | float):
            return NotImplemented
        return Vector2(
            self.x * scalar,
            self.y * scalar,
        )

    def __rmul__(self, scalar: float) -> Vector2:
        return self * scalar

    def __truediv__(self, scalar: float) -> Vector2:
        if not isinstance(scalar, int | float):
            return NotImplemented
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide Vector2 by 0")
        return Vector2(
            self.x / scalar,
            self.y / scalar,
        )

    @property
    def magnitude(self) -> float:
        """Return the vector's length"""
        return hypot(self.x, self.y)

    def distance_to(self, other: Vector2) -> float:
        """Return the Euclidean distance to another vector."""

        if not isinstance(other, Vector2):
            raise TypeError(
                f"distance_to() expected a Vector2, received {type(other).__name__}"
            )

        return (self - other).magnitude

    def normalized(self) -> Vector2:
        """Return a normalized copy of the vector."""

        magnitude = self.magnitude

        if magnitude == 0:
            raise ValueError("Cannot normalize a zero-length vector.")
        return self / magnitude

    def dot(self, other: Vector2) -> float:
        """Return the dot product with another vector."""

        if not isinstance(other, Vector2):
            raise TypeError(
                f"dot() expected a Vector2, received {type(other).__name__}"
            )

        return self.x * other.x + self.y * other.y

    def to_tuple(self) -> tuple[float, float]:
        """Return the vector as an '(x, y)' tuple."""
        return self.x, self.y

    @classmethod
    def from_tuple(cls, value: tuple[float, float]) -> Vector2:
        """Create a vector from an '(x, y)' tuple."""

        if len(value) != 2:
            raise ValueError("Vector2.from_tuple() requires exactly two values.")

        return cls(x=float(value[0]), y=float(value[1]))

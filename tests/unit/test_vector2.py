import math

import pytest

from lachikai import Vector2


def test_vector_addition() -> None:
    result = Vector2(1, 2) + Vector2(3, 4)
    assert result == Vector2(4, 6)


def test_vector_substraction() -> None:
    result = Vector2(5, 7) - Vector2(2, 3)

    assert result == Vector2(3, 4)


def test_vector_scalar_multiplication() -> None:
    result = Vector2(2, 3) * 4
    assert result == Vector2(8, 12)


def test_vector_reverse_scalar_multiplication() -> None:
    result = 4 * Vector2(2, 3)
    assert result == Vector2(8, 12)


def test_vector_scalar_division() -> None:
    result = Vector2(8, 12) / 4

    assert result == Vector2(2, 3)


def test_vector_division_by_zero_raises_error() -> None:
    with pytest.raises(ZeroDivisionError, match="Cannot divide Vector2 by 0"):
        Vector2(1, 2) / 0


def test_vector_magnitude() -> None:
    vector = Vector2(3, 4)

    assert vector.magnitude == 5


def test_vector_distance() -> None:
    start = Vector2(0, 0)
    end = Vector2(3, 4)

    assert start.distance_to(end) == 5


def test_vector_normalization() -> None:
    result = Vector2(3, 4).normalized()

    assert math.isclose(result.magnitude, 1.0)


def test_zero_vector_cannot_be_normalized() -> None:
    with pytest.raises(
        ValueError,
        match="Cannot normalize a zero-length vector.",
    ):
        Vector2(0, 0).normalized()


def test_dot_product() -> None:
    result = Vector2(1, 2).dot(Vector2(3, 4))

    assert result == 11


def test_vector_to_tuple() -> None:
    assert Vector2(1, 2).to_tuple() == (1, 2)


def test_vector_from_tuple() -> None:
    assert Vector2.from_tuple((1, 2)) == Vector2(1.0, 2.0)


def test_vector_is_immutable() -> None:
    vector = Vector2(1, 2)

    with pytest.raises(AttributeError):
        vector.x = 10

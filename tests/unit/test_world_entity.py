from types import MappingProxyType

import pytest

from lachikai import Vector2, WorldEntity


def test_world_entity_creation() -> None:
    entity = WorldEntity(
        entity_id="player",
        position=Vector2(10, 20),
        tags={"player", "friendly"},
        velocity=Vector2(2, 3),
        metadata={"health": 100},
    )

    assert entity.entity_id == "player"
    assert entity.position == Vector2(10, 20)
    assert entity.velocity == Vector2(2, 3)
    assert entity.tags == frozenset({"player", "friendly"})
    assert entity.enabled is True


def test_world_entity_defaults() -> None:
    entity = WorldEntity(
        entity_id="obstacle",
        position=Vector2(0, 0),
    )

    assert entity.tags == frozenset()
    assert entity.velocity == Vector2(0.0, 0.0)
    assert entity.enabled is True
    assert dict(entity.metadata) == {}


def test_entity_id_cannot_be_empty() -> None:
    with pytest.raises(ValueError, match="entity_id cannot be empty"):
        WorldEntity(
            entity_id="",
            position=Vector2(0, 0),
        )


def test_tags_are_converted_to_frozenset() -> None:
    entity = WorldEntity(
        entity_id="enemy",
        position=Vector2(0, 0),
        tags={"hostile", "npc"},
    )

    assert entity.tags == frozenset({"hostile", "npc"})


def test_metadata_is_read_only() -> None:
    entity = WorldEntity(
        entity_id="player",
        position=Vector2(0, 0),
        metadata={"health": 100},
    )

    assert isinstance(entity.metadata, MappingProxyType)

    with pytest.raises(TypeError):
        entity.metadata["health"] = 50  # type: ignore[index]


def test_world_entity_is_immutable() -> None:
    entity = WorldEntity(
        entity_id="player",
        position=Vector2(0, 0),
    )

    with pytest.raises(AttributeError):
        entity.position = Vector2(5, 5)  # type: ignore[misc]


def test_has_tag() -> None:
    entity = WorldEntity(
        entity_id="enemy",
        position=Vector2(0, 0),
        tags={"hostile"},
    )

    assert entity.has_tag("hostile")
    assert not entity.has_tag("friendly")


def test_distance_to_entity() -> None:
    first = WorldEntity(
        entity_id="first",
        position=Vector2(0, 0),
    )
    second = WorldEntity(
        entity_id="second",
        position=Vector2(3, 4),
    )

    assert first.distance_to(second) == 5


def test_distance_to_position() -> None:
    entity = WorldEntity(
        entity_id="player",
        position=Vector2(0, 0),
    )

    assert entity.distance_to(Vector2(6, 8)) == 10


def test_distance_to_invalid_type_raises_error() -> None:
    entity = WorldEntity(
        entity_id="player",
        position=Vector2(0, 0),
    )

    with pytest.raises(
        TypeError,
        match="expected WorldEntity or Vector2",
    ):
        entity.distance_to("invalid")  # type: ignore[arg-type]


def test_to_dict() -> None:
    entity = WorldEntity(
        entity_id="enemy",
        position=Vector2(1, 2),
        velocity=Vector2(3, 4),
        tags={"npc", "hostile"},
        enabled=False,
        metadata={"health": 50},
    )

    assert entity.to_dict() == {
        "entity_id": "enemy",
        "position": {
            "x": 1,
            "y": 2,
        },
        "velocity": {
            "x": 3,
            "y": 4,
        },
        "tags": ["hostile", "npc"],
        "enabled": False,
        "metadata": {
            "health": 50,
        },
    }

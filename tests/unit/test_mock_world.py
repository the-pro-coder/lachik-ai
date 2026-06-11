import pytest

from lachikai import MockWorld, Vector2, WorldEntity


def test_mock_world_starts_empty() -> None:
    world = MockWorld()

    assert world.time == 0.0
    assert world.entities == ()


def test_add_and_get_entity() -> None:
    world = MockWorld()
    entity = WorldEntity(
        entity_id="player",
        position=Vector2(10, 20),
    )

    result = world.add_entity(entity)

    assert result is entity
    assert world.get_entity("player") == entity
    assert world.entities == (entity,)


def test_duplicate_entity_is_rejected() -> None:
    world = MockWorld()
    entity = WorldEntity(
        entity_id="player",
        position=Vector2(0, 0),
    )

    world.add_entity(entity)

    with pytest.raises(
        ValueError,
        match="Entity 'player' is already registered",
    ):
        world.add_entity(entity)


def test_get_missing_entity_raises_error() -> None:
    world = MockWorld()

    with pytest.raises(
        KeyError,
        match="Entity 'missing' is not registered",
    ):
        world.get_entity("missing")


def test_find_missing_entity_returns_none() -> None:
    world = MockWorld()

    assert world.find_entity("missing") is None


def test_remove_entity() -> None:
    world = MockWorld()
    entity = WorldEntity(
        entity_id="player",
        position=Vector2(0, 0),
    )
    world.add_entity(entity)

    removed = world.remove_entity("player")

    assert removed == entity
    assert world.find_entity("player") is None


def test_remove_missing_entity_raises_error() -> None:
    world = MockWorld()

    with pytest.raises(
        KeyError,
        match="Entity 'missing' is not registered",
    ):
        world.remove_entity("missing")


def test_step_advances_simulated_time() -> None:
    world = MockWorld()

    world.step(0.25)
    world.step(0.75)

    assert world.time == 1.0


def test_negative_delta_time_is_rejected() -> None:
    world = MockWorld()

    with pytest.raises(
        ValueError,
        match="delta_time cannot be negative",
    ):
        world.step(-0.1)


def test_set_position_replaces_entity_snapshot() -> None:
    world = MockWorld()
    original = WorldEntity(
        entity_id="player",
        position=Vector2(0, 0),
    )
    world.add_entity(original)

    updated = world.set_position(
        "player",
        Vector2(10, 20),
    )

    assert updated.position == Vector2(10, 20)
    assert world.get_entity("player") == updated
    assert original.position == Vector2(0, 0)
    assert updated is not original


def test_set_velocity_replaces_entity_snapshot() -> None:
    world = MockWorld()
    world.add_entity(
        WorldEntity(
            entity_id="player",
            position=Vector2(0, 0),
        )
    )

    updated = world.set_velocity(
        "player",
        Vector2(2, 3),
    )

    assert updated.velocity == Vector2(2, 3)


def test_set_enabled_replaces_entity_snapshot() -> None:
    world = MockWorld()
    world.add_entity(
        WorldEntity(
            entity_id="enemy",
            position=Vector2(0, 0),
        )
    )

    updated = world.set_enabled("enemy", False)

    assert updated.enabled is False


def test_nearby_entities_are_sorted_by_distance() -> None:
    world = MockWorld()

    world.add_entity(
        WorldEntity(
            entity_id="observer",
            position=Vector2(0, 0),
        )
    )
    world.add_entity(
        WorldEntity(
            entity_id="far",
            position=Vector2(8, 0),
        )
    )
    world.add_entity(
        WorldEntity(
            entity_id="near",
            position=Vector2(2, 0),
        )
    )
    world.add_entity(
        WorldEntity(
            entity_id="outside",
            position=Vector2(20, 0),
        )
    )

    nearby = world.get_nearby_entities(
        observer_id="observer",
        radius=10,
    )

    assert [entity.entity_id for entity in nearby] == [
        "near",
        "far",
    ]


def test_observer_is_not_returned_by_nearby_query() -> None:
    world = MockWorld()
    world.add_entity(
        WorldEntity(
            entity_id="observer",
            position=Vector2(0, 0),
        )
    )

    nearby = world.get_nearby_entities(
        observer_id="observer",
        radius=100,
    )

    assert nearby == ()


def test_nearby_query_filters_by_required_tags() -> None:
    world = MockWorld()

    world.add_entity(
        WorldEntity(
            entity_id="observer",
            position=Vector2(0, 0),
        )
    )
    world.add_entity(
        WorldEntity(
            entity_id="enemy",
            position=Vector2(2, 0),
            tags={"npc", "hostile"},
        )
    )
    world.add_entity(
        WorldEntity(
            entity_id="friendly",
            position=Vector2(3, 0),
            tags={"npc", "friendly"},
        )
    )

    nearby = world.get_nearby_entities(
        observer_id="observer",
        radius=10,
        required_tags={"hostile"},
    )

    assert [entity.entity_id for entity in nearby] == ["enemy"]


def test_disabled_entities_are_excluded_by_default() -> None:
    world = MockWorld()

    world.add_entity(
        WorldEntity(
            entity_id="observer",
            position=Vector2(0, 0),
        )
    )
    world.add_entity(
        WorldEntity(
            entity_id="disabled",
            position=Vector2(2, 0),
            enabled=False,
        )
    )

    nearby = world.get_nearby_entities(
        observer_id="observer",
        radius=10,
    )

    assert nearby == ()


def test_disabled_entities_can_be_included() -> None:
    world = MockWorld()

    world.add_entity(
        WorldEntity(
            entity_id="observer",
            position=Vector2(0, 0),
        )
    )
    world.add_entity(
        WorldEntity(
            entity_id="disabled",
            position=Vector2(2, 0),
            enabled=False,
        )
    )

    nearby = world.get_nearby_entities(
        observer_id="observer",
        radius=10,
        include_disabled=True,
    )

    assert [entity.entity_id for entity in nearby] == [
        "disabled",
    ]


def test_negative_query_radius_is_rejected() -> None:
    world = MockWorld()
    world.add_entity(
        WorldEntity(
            entity_id="observer",
            position=Vector2(0, 0),
        )
    )

    with pytest.raises(
        ValueError,
        match="radius cannot be negative",
    ):
        world.get_nearby_entities(
            observer_id="observer",
            radius=-1,
        )


def test_seeded_randomness_is_reproducible() -> None:
    first_world = MockWorld(seed=42)
    second_world = MockWorld(seed=42)

    first_values = [first_world.random.random() for _ in range(5)]
    second_values = [second_world.random.random() for _ in range(5)]

    assert first_values == second_values

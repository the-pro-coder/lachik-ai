from types import MappingProxyType

import pytest

from lachikai import Observation, Vector2


def test_observation_creation() -> None:
    observation = Observation(
        observation_type="entity_detected",
        timestamp=1.5,
        source_sensor_id="proximity",
        observer_id="guard",
        entity_id="player",
        position=Vector2(10, 20),
        distance=15.0,
        tags=frozenset({"player", "hostile"}),
        confidence=0.9,
        metadata={"visible": True},
    )

    assert observation.observation_type == "entity_detected"
    assert observation.entity_id == "player"
    assert observation.position == Vector2(10, 20)
    assert observation.distance == 15.0
    assert observation.confidence == 0.9


def test_observation_defaults() -> None:
    observation = Observation(
        observation_type="temperature",
        timestamp=0.0,
        source_sensor_id="temperature_sensor",
        observer_id="agent",
    )

    assert observation.entity_id is None
    assert observation.position is None
    assert observation.distance is None
    assert observation.tags == frozenset()
    assert observation.value is None
    assert observation.confidence == 1.0


def test_tags_are_converted_to_frozenset() -> None:
    observation = Observation(
        observation_type="entity_detected",
        timestamp=0.0,
        source_sensor_id="sensor",
        observer_id="agent",
        tags={"enemy", "visible"},
    )

    assert observation.tags == frozenset({"enemy", "visible"})


def test_metadata_is_read_only() -> None:
    observation = Observation(
        observation_type="entity_detected",
        timestamp=0.0,
        source_sensor_id="sensor",
        observer_id="agent",
        metadata={"danger": True},
    )

    assert isinstance(observation.metadata, MappingProxyType)

    with pytest.raises(TypeError):
        observation.metadata["danger"] = False  # type: ignore[index]


def test_observation_is_immutable() -> None:
    observation = Observation(
        observation_type="entity_detected",
        timestamp=0.0,
        source_sensor_id="sensor",
        observer_id="agent",
    )

    with pytest.raises(AttributeError):
        observation.entity_id = "other"  # type: ignore[misc]


def test_has_tag() -> None:
    observation = Observation(
        observation_type="entity_detected",
        timestamp=0.0,
        source_sensor_id="sensor",
        observer_id="agent",
        tags=frozenset({"enemy"}),
    )

    assert observation.has_tag("enemy")
    assert not observation.has_tag("friendly")


@pytest.mark.parametrize(
    ("field_name", "value", "message"),
    [
        ("observation_type", "", "observation_type cannot be empty"),
        ("source_sensor_id", "", "source_sensor_id cannot be empty"),
        ("observer_id", "", "observer_id cannot be empty"),
    ],
)
def test_required_string_fields_cannot_be_empty(
    field_name: str,
    value: str,
    message: str,
) -> None:
    values = {
        "observation_type": "entity_detected",
        "timestamp": 0.0,
        "source_sensor_id": "sensor",
        "observer_id": "agent",
    }
    values[field_name] = value

    with pytest.raises(ValueError, match=message):
        Observation(**values)  # type: ignore[arg-type]


def test_negative_timestamp_is_rejected() -> None:
    with pytest.raises(ValueError, match="timestamp cannot be negative"):
        Observation(
            observation_type="entity_detected",
            timestamp=-1.0,
            source_sensor_id="sensor",
            observer_id="agent",
        )


def test_negative_distance_is_rejected() -> None:
    with pytest.raises(ValueError, match="distance cannot be negative"):
        Observation(
            observation_type="entity_detected",
            timestamp=0.0,
            source_sensor_id="sensor",
            observer_id="agent",
            distance=-5.0,
        )


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_invalid_confidence_is_rejected(confidence: float) -> None:
    with pytest.raises(
        ValueError,
        match="confidence must be between 0.0 and 1.0",
    ):
        Observation(
            observation_type="entity_detected",
            timestamp=0.0,
            source_sensor_id="sensor",
            observer_id="agent",
            confidence=confidence,
        )


def test_to_dict() -> None:
    observation = Observation(
        observation_type="entity_detected",
        timestamp=2.0,
        source_sensor_id="proximity",
        observer_id="guard",
        entity_id="player",
        position=Vector2(3, 4),
        distance=5.0,
        tags=frozenset({"enemy", "player"}),
        value="detected",
        confidence=0.8,
        metadata={"visible": True},
    )

    result = observation.to_dict()

    assert result == {
        "observation_type": "entity_detected",
        "timestamp": 2.0,
        "source_sensor_id": "proximity",
        "observer_id": "guard",
        "entity_id": "player",
        "position": {"x": 3, "y": 4},
        "distance": 5.0,
        "tags": ["enemy", "player"],
        "value": "detected",
        "confidence": 0.8,
        "metadata": {"visible": True},
    }

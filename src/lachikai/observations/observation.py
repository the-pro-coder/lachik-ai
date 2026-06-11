from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from lachikai.core import Vector2


@dataclass(frozen=True, slots=True)
class Observation:
    """Immutable information perceived by an agent through a sensor."""

    observation_type: str
    timestamp: float
    source_sensor_id: str
    observer_id: str
    entity_id: str | None = None
    position: Vector2 | None = None
    distance: float | None = None
    tags: frozenset[str] = field(default_factory=frozenset)
    value: Any = None
    confidence: float = 1.0
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.observation_type.strip():
            raise ValueError("observation_type cannot be empty.")

        if not self.source_sensor_id.strip():
            raise ValueError("source_sensor_id cannot be empty.")

        if not self.observer_id.strip():
            raise ValueError("observer_id cannot be empty.")

        if self.timestamp < 0:
            raise ValueError("timestamp cannot be negative.")

        if self.distance is not None and self.distance < 0:
            raise ValueError("distance cannot be negative.")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0.")

        object.__setattr__(self, "tags", frozenset(self.tags))
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )

    def has_tag(self, tag: str) -> bool:
        """Return whether this observation contains the supplied tag."""

        return tag in self.tags

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible representation when values permit it."""

        return {
            "observation_type": self.observation_type,
            "timestamp": self.timestamp,
            "source_sensor_id": self.source_sensor_id,
            "observer_id": self.observer_id,
            "entity_id": self.entity_id,
            "position": (
                {
                    "x": self.position.x,
                    "y": self.position.y,
                }
                if self.position is not None
                else None
            ),
            "distance": self.distance,
            "tags": sorted(self.tags),
            "value": self.value,
            "confidence": self.confidence,
            "metadata": dict(self.metadata),
        }

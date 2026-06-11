from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from lachikai.core import Vector2


@dataclass(frozen=True, slots=True)
class WorldEntity:
    """An immutable snapshot of an entity in a logical world."""

    entity_id: str
    position: Vector2
    tags: frozenset[str] = field(default_factory=frozenset)
    velocity: Vector2 = field(default_factory=lambda: Vector2(0.0, 0.0))
    enabled: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.entity_id.strip():
            raise ValueError("entity_id cannot be empty.")

        object.__setattr__(self, "tags", frozenset(self.tags))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    def has_tag(self, tag: str) -> bool:
        """Return whether the entity contains a tag."""

        return tag in self.tags

    def distance_to(self, other: WorldEntity | Vector2) -> float:
        """Return the distance to another entity or position."""

        if isinstance(other, WorldEntity):
            destination = other.position
        elif isinstance(other, Vector2):
            destination = other
        else:
            raise TypeError(
                "distance_to() expected WorldEntity or Vector2, "
                f"received {type(other).__name__}"
            )

        return self.position.distance_to(destination)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible representation when metadata permits it."""

        return {
            "entity_id": self.entity_id,
            "position": {
                "x": self.position.x,
                "y": self.position.y,
            },
            "velocity": {
                "x": self.velocity.x,
                "y": self.velocity.y,
            },
            "tags": sorted(self.tags),
            "enabled": self.enabled,
            "metadata": dict(self.metadata),
        }

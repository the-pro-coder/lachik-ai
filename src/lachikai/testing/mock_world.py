from __future__ import annotations

import random
from collections.abc import Iterable
from dataclasses import replace

from lachikai.core import Vector2
from lachikai.world import WorldEntity


class MockWorld:
    """A lightweight engine-independent world for tests and simulations."""

    def __init__(self, *, seed: int | None = None) -> None:
        self._entities: dict[str, WorldEntity] = {}
        self._time = 0.0
        self._random = random.Random(seed)

    @property
    def time(self) -> float:
        """Return the current simulated time in seconds."""

        return self._time

    @property
    def random(self) -> random.Random:
        """Return the world's deterministic random-number generator."""

        return self._random

    @property
    def entities(self) -> tuple[WorldEntity, ...]:
        """Return an immutable snapshot of all registered entities."""

        return tuple(self._entities.values())

    def step(self, delta_time: float) -> None:
        """Advance simulated time."""

        if delta_time < 0:
            raise ValueError("delta_time cannot be negative.")

        self._time += delta_time

    def add_entity(self, entity: WorldEntity) -> WorldEntity:
        """Register an entity and return the stored snapshot."""

        if entity.entity_id in self._entities:
            raise ValueError(f"Entity '{entity.entity_id}' is already registered.")

        self._entities[entity.entity_id] = entity
        return entity

    def remove_entity(self, entity_id: str) -> WorldEntity:
        """Remove and return an entity."""

        try:
            return self._entities.pop(entity_id)
        except KeyError as error:
            raise KeyError(f"Entity '{entity_id}' is not registered.") from error

    def get_entity(self, entity_id: str) -> WorldEntity:
        """Return a registered entity."""

        try:
            return self._entities[entity_id]
        except KeyError as error:
            raise KeyError(f"Entity '{entity_id}' is not registered.") from error

    def find_entity(self, entity_id: str) -> WorldEntity | None:
        """Return an entity or ``None`` when it is not registered."""

        return self._entities.get(entity_id)

    def set_position(
        self,
        entity_id: str,
        position: Vector2,
    ) -> WorldEntity:
        """Replace an entity snapshot with an updated position."""

        entity = self.get_entity(entity_id)
        updated = replace(entity, position=position)
        self._entities[entity_id] = updated

        return updated

    def set_velocity(
        self,
        entity_id: str,
        velocity: Vector2,
    ) -> WorldEntity:
        """Replace an entity snapshot with an updated velocity."""

        entity = self.get_entity(entity_id)
        updated = replace(entity, velocity=velocity)
        self._entities[entity_id] = updated

        return updated

    def set_enabled(
        self,
        entity_id: str,
        enabled: bool,
    ) -> WorldEntity:
        """Enable or disable an entity."""

        entity = self.get_entity(entity_id)
        updated = replace(entity, enabled=enabled)
        self._entities[entity_id] = updated

        return updated

    def get_nearby_entities(
        self,
        observer_id: str,
        radius: float,
        *,
        required_tags: Iterable[str] = (),
        include_disabled: bool = False,
    ) -> tuple[WorldEntity, ...]:
        """Return nearby entities ordered from nearest to farthest."""

        if radius < 0:
            raise ValueError("radius cannot be negative.")

        observer = self.get_entity(observer_id)
        required_tag_set = frozenset(required_tags)

        nearby: list[tuple[float, WorldEntity]] = []

        for entity in self._entities.values():
            if entity.entity_id == observer_id:
                continue

            if not include_disabled and not entity.enabled:
                continue

            if not required_tag_set.issubset(entity.tags):
                continue

            distance = observer.distance_to(entity)

            if distance <= radius:
                nearby.append((distance, entity))

        nearby.sort(key=lambda item: (item[0], item[1].entity_id))

        return tuple(entity for _, entity in nearby)

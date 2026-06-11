"""Lachik AI: modular autonomous agents and game-AI systems."""

from .core import Vector2
from .observations import Observation
from .world import WorldEntity

__version__ = "0.1.0.dev0"

__all__ = [
    "Observation",
    "Vector2",
    "WorldEntity",
    "__version__",
]

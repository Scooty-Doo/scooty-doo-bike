"""
This module enables the application the handle multiple brain instances (bikes).
"""

from typing import Dict, Optional
from .brain import Brain

class Hivemind:
    """Handles multiple brain instances (bikes)."""
    def __init__(self):
        self.brains: Dict[int, Brain] = {}

    def add_brain(self, bike_id: int, brain: Brain):
        """Add a brain instance to the hivemind."""
        self.brains[bike_id] = brain

    def get_brain(self, bike_id: Optional[int] = None) -> Brain:
        """Retrieve a brain instance from the hivemind."""
        if bike_id is not None:
            brain = self.brains.get(bike_id)
            if not brain:
                raise ValueError(f"Brain with bike_id {bike_id} does not exist.")
            return brain
        if not self.brains:
            raise ValueError("No Brain instances available.")
        lowest_id = min(self.brains.keys())
        return self.brains[lowest_id]

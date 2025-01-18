"""Tests for the Hivemind class."""

import pytest
from src.brain.hivemind import Hivemind
from src.brain.brain import Brain

class TestHivemind:
    """Tests for the Hivemind class."""

    def test_empty_hivemind_get_brain_none_raises(self):
        """Test that get_brain() raises ValueError when hivemind is empty."""
        hivemind = Hivemind()
        with pytest.raises(ValueError, match="No Brain instances available."):
            hivemind.get_brain()

    def test_empty_hivemind_get_brain_specific_raises(self):
        """Test that get_brain(bike_id=999) raises ValueError when hivemind is empty."""
        hivemind = Hivemind()
        with pytest.raises(ValueError, match="Brain with bike_id 999 does not exist."):
            hivemind.get_brain(999)

    def test_add_brain_and_retrieve_specific(self):
        """Test adding a brain and retrieving it by bike_id."""
        hivemind = Hivemind()
        brain_1 = Brain(bike_id=1, longitude=0.0, latitude=0.0)
        hivemind.add_brain(1, brain_1)
        retrieved_brain = hivemind.get_brain(1)
        assert retrieved_brain is brain_1

    def test_add_brain_and_retrieve_none(self):
        """Test adding a brain and retrieving it without bike_id."""
        hivemind = Hivemind()
        brain_1 = Brain(bike_id=1, longitude=10.0, latitude=20.0)
        hivemind.add_brain(1, brain_1)
        retrieved = hivemind.get_brain()  # if no id, return the brain with lowest id
        assert retrieved is brain_1

    def test_get_brain_lowest_id(self):
        """Test that get_brain() returns the brain with the lowest bike_id."""
        hivemind = Hivemind()
        brain_10 = Brain(bike_id=10, longitude=99.0, latitude=99.0)
        brain_2 = Brain(bike_id=2, longitude=11.0, latitude=11.0)
        brain_5 = Brain(bike_id=5, longitude=22.0, latitude=22.0)
        hivemind.add_brain(10, brain_10)
        hivemind.add_brain(5, brain_5)
        hivemind.add_brain(2, brain_2)
        retrieved = hivemind.get_brain()
        assert retrieved is brain_2

    def test_get_brain_missing_id_raises(self):
        """Test that get_brain() raises ValueError when bike_id is not found."""
        hivemind = Hivemind()
        brain_1 = Brain(bike_id=1, longitude=0.0, latitude=0.0)
        hivemind.add_brain(1, brain_1)
        with pytest.raises(ValueError, match="Brain with bike_id 999 does not exist."):
            hivemind.get_brain(999)

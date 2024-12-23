import pytest
import json
from unittest.mock import patch
from src._utils._map import Map

@pytest.fixture
def sample_zones():
    return [
        {
            "id": 1,
            "zone_type": "parking",
            "city_id": "city1",
            "boundary": "POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"
        },
        {
            "id": 2,
            "zone_type": "charging",
            "city_id": "city1",
            "boundary": "POLYGON((2 0, 2 1, 3 1, 3 0, 2 0))"
        },
        {
            "id": 3,
            "zone_type": "slow",
            "city_id": "city1",
            "boundary": "POLYGON((4 0, 4 1, 5 1, 5 0, 4 0))"
        },
        {
            "id": 4,
            "zone_type": "parking",
            "city_id": "city1",
            "boundary": "POLYGON((6 0, 6 1, 7 1, 7 0, 6 0))"
        }
    ]

@pytest.fixture
def sample_zone_types():
    return {
        "parking": {
            "speed_limit": 5
        },
        "charging": {
            "speed_limit": 5
        },
        "slow": {
            "speed_limit": 10
        },
        "regular": {
            "speed_limit": 20
        }
    }

class TestMap:

    def test_get_parking_zones(self, sample_zones):
        parking_zones = Map.Zones.get_parking_zones(sample_zones)
        assert len(parking_zones) == 2
        for zone in parking_zones:
            assert zone["zone_type"] == "parking"

    @patch('src._utils._map.random.choice')
    def test_get_deployment_zone(self, mock_random_choice, sample_zones):
        parking_zones = Map.Zones.get_parking_zones(sample_zones)
        mock_choice_zone = parking_zones[0]
        mock_random_choice.return_value = mock_choice_zone
        deployment_zone = Map.Zone.get_deployment_zone(sample_zones)
        mock_random_choice.assert_called_once_with(parking_zones)
        assert deployment_zone == mock_choice_zone

    def test_get_deployment_zone_no_parking_zones(self, sample_zones):
        non_parking_zones = [zone for zone in sample_zones if zone["zone_type"] != "parking"]
        with pytest.raises(IndexError):
            Map.Zone.get_deployment_zone(non_parking_zones)

    def test_get_position_after_minutes_travelled_normal(self):
        """
        Test normal case where the bike travels more than the distance to the end position,
        resulting in the bike reaching the end position.
        """
        start_position = (0.0, 0.0)
        end_position = (1.0, 1.0)
        minutes_travelled = 30
        speed_in_kmh = 60
        expected_position = end_position
        new_position = Map.Position.get_position_after_minutes_travelled(
            start_position, end_position, minutes_travelled, speed_in_kmh
        )
        assert new_position == expected_position

    def test_get_position_after_minutes_travelled_exact(self):
        start_position = (0.0, 0.0)
        end_position = (1.0, 1.0)
        # Distance between start and end is sqrt(2) km assuming coordinates are in km
        distance = ((1.0 - 0.0)**2 + (1.0 - 0.0)**2) ** 0.5  # sqrt(2)
        speed_in_kmh = 60
        minutes_travelled = (distance / speed_in_kmh) * 60  # time to reach end_position
        new_position = Map.Position.get_position_after_minutes_travelled(
            start_position, end_position, minutes_travelled, speed_in_kmh)
        assert new_position == end_position

    def test_get_position_after_minutes_travelled_over(self):
        """
        Test the case where the bike travels more than the distance to the end position.
        """
        start_position = (0.0, 0.0)
        end_position = (1.0, 1.0)
        speed_in_kmh = 60
        minutes_travelled = 120
        new_position = Map.Position.get_position_after_minutes_travelled(
            start_position, end_position, minutes_travelled, speed_in_kmh)
        assert new_position == end_position

    def test_get_position_after_minutes_travelled_zero_minutes(self):
        """
        Test the case where the bike doesn't travel at all.
        """
        start_position = (2.0, 2.0)
        end_position = (3.0, 3.0)
        minutes_travelled = 0
        speed_in_kmh = 60
        new_position = Map.Position.get_position_after_minutes_travelled(
            start_position, end_position, minutes_travelled, speed_in_kmh)
        assert new_position == start_position

    def test_get_position_after_minutes_travelled_zero_speed(self):
        """
        Test the case where the speed is zero, resulting in no movement.
        """
        start_position = (4.0, 4.0)
        end_position = (5.0, 5.0)
        minutes_travelled = 30
        speed_in_kmh = 0
        expected_position = start_position
        new_position = Map.Position.get_position_after_minutes_travelled(
            start_position, end_position, minutes_travelled, speed_in_kmh)
        assert new_position == expected_position


    def test_get_closest_zone(self, sample_zones):
        """
        Test that get_closest_zone returns the zone with the shortest distance to the given position.
        """
        position = (0.5, 0.5)  # Inside zone 1
        closest_zone = Map.Position.get_closest_zone(sample_zones, position)
        assert closest_zone["id"] == 1

        position = (2.5, 0.5)  # Inside zone 2
        closest_zone = Map.Position.get_closest_zone(sample_zones, position)
        assert closest_zone["id"] == 2

        position = (10.0, 10.0)  # Outside all zones, closest to zone 4
        closest_zone = Map.Position.get_closest_zone(sample_zones, position)
        assert closest_zone["id"] == 4

    def test_get_speed_limit_inside_zone(self, sample_zones, sample_zone_types):
        """
        Test that get_speed_limit returns the correct speed limit for a position inside a zone.
        """
        position = (0.5, 0.5)  # Inside zone 1 (parking)
        speed_limit = Map.Zone.get_speed_limit(sample_zones, sample_zone_types, position)
        assert speed_limit == 5

        position = (2.5, 0.5)  # Inside zone 2 (charging)
        speed_limit = Map.Zone.get_speed_limit(sample_zones, sample_zone_types, position)
        assert speed_limit == 5

        position = (4.5, 0.5)  # Inside zone 3 (slow)
        speed_limit = Map.Zone.get_speed_limit(sample_zones, sample_zone_types, position)
        assert speed_limit == 10

        position = (6.5, 0.5)  # Inside zone 4 (parking)
        speed_limit = Map.Zone.get_speed_limit(sample_zones, sample_zone_types, position)
        assert speed_limit == 5

    def test_get_speed_limit_outside_zone(self, sample_zones, sample_zone_types):
        """
        Test that get_speed_limit returns the speed limit of the closest zone when the position is outside all zones.
        """
        position = (10.0, 10.0)  # Outside all zones
        # The closest zone in sample_zones is zone 4 with speed_limit 5
        expected_speed_limit = sample_zone_types["parking"]["speed_limit"]  # 5
        speed_limit = Map.Zone.get_speed_limit(sample_zones, sample_zone_types, position)
        assert speed_limit == expected_speed_limit

    def test_is_charging_zone_true(self, sample_zones):
        """
        Test that is_charging_zone returns True for positions inside charging zones.
        """
        position = (2.5, 0.5)  # Inside zone 2 (charging)
        assert Map.Zone.is_charging_zone(sample_zones, position) is True

    def test_is_charging_zone_false(self, sample_zones):
        """
        Test that is_charging_zone returns False for positions not inside charging zones.
        """
        position = (0.5, 0.5)  # Inside zone 1 (parking)
        assert Map.Zone.is_charging_zone(sample_zones, position) is False

        position = (4.5, 0.5)  # Inside zone 3 (slow)
        assert Map.Zone.is_charging_zone(sample_zones, position) is False

        position = (6.5, 0.5)  # Inside zone 4 (parking)
        assert Map.Zone.is_charging_zone(sample_zones, position) is False

    def test_get_centroid_position(self, sample_zones):
        """
        Test that get_centroid_position correctly calculates the centroid of a zone.
        """
        zone = sample_zones[0]  # Zone 1
        expected_centroid = (0.5, 0.5)
        centroid = Map.Zone.get_centroid_position(zone)
        assert centroid == expected_centroid
        zone = sample_zones[1]  # Zone 2
        expected_centroid = (2.5, 0.5)
        centroid = Map.Zone.get_centroid_position(zone)
        assert centroid == expected_centroid

    def test_load_zones_empty_file(self, tmp_path):
        """
        Test that load returns an empty list when the zones file is empty.
        """
        # Arrange: Create an empty _zones.json file
        zones_file = tmp_path / "_zones.json"
        zones_file.write_text('[]')

        with patch('os.path.dirname', return_value=str(tmp_path)):
            zones = Map.Zones.load()
            assert zones == []

    def test_load_zones_non_empty_file(self, tmp_path):
        """
        Test that load correctly loads zones from a non-empty file.
        """
        # Arrange: Create a _zones.json file with sample data
        zones_data = [
            {
                "id": 1,
                "zone_type": "parking",
                "city_id": "city1",
                "boundary": "POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"
            }
        ]
        zones_file = tmp_path / "_zones.json"
        zones_file.write_text(json.dumps(zones_data))

        with patch('os.path.dirname', return_value=str(tmp_path)):
            zones = Map.Zones.load()
            assert zones == zones_data

    def test_load_zone_types_empty_file(self, tmp_path):
        """
        Test that load returns an empty list when the zone types file is empty.
        """
        # Arrange: Create an empty _zone_types.json file
        zone_types_file = tmp_path / "_zone_types.json"
        zone_types_file.write_text('{}')

        with patch('os.path.dirname', return_value=str(tmp_path)):
            zone_types = Map.ZoneTypes.load()
            assert zone_types == {}

    def test_load_zone_types_non_empty_file(self, tmp_path):
        """
        Test that load correctly loads zone types from a non-empty file.
        """
        # Arrange: Create a _zone_types.json file with sample data
        zone_types_data = {
            "parking": {
                "speed_limit": 5
            },
            "charging": {
                "speed_limit": 5
            }
        }
        zone_types_file = tmp_path / "_zone_types.json"
        zone_types_file.write_text(json.dumps(zone_types_data))

        with patch('os.path.dirname', return_value=str(tmp_path)):
            zone_types = Map.ZoneTypes.load()
            assert zone_types == zone_types_data

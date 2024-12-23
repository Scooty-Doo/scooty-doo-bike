import pytest
from unittest.mock import patch
from src.bike.bike import Bike
from src._utils._errors import AlreadyUnlockedError, AlreadyLockedError, NotChargingZoneError, PositionNotWithinZoneError, InvalidPositionTypeError, OutOfBoundsError, InvalidPositionLengthError
from src._utils._map import Map

@pytest.mark.usefixtures("mock_environment")
class TestBike:

    def test_unlocking_bike(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        assert bike.mode.is_locked()
        assert bike.user is None
        bike.unlock(user_id=123, trip_id=456)
        assert bike.mode.is_unlocked()
        assert bike.user.user_id == 123
        with pytest.raises(AlreadyUnlockedError):
            bike.unlock(user_id=456, trip_id=789)

    def test_locking_bike_in_parking_zone(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        assert bike.mode.is_unlocked()
        bike.lock()
        assert bike.mode.is_locked()
        assert bike.user is None
        with pytest.raises(AlreadyLockedError):
            bike.lock()

    def test_locking_bike_outside_zone(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        position = (999.0, 999.0)
        bike.relocate(position, ignore_zone=True)
        with pytest.raises(PositionNotWithinZoneError):
            bike.lock(maintenance=False, ignore_zone=False)

    def test_moving_bike(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        initial_battery = bike.battery.level
        charging_zone = Map.Zone.get_charging_zone(bike.zones)
        charging_position = Map.Zone.get_centroid_position(charging_zone)
        bike.move(charging_position)
        assert bike.battery.level < initial_battery
        bike.speed.limit(bike.zones, bike.zone_types, bike.position.current)
        assert bike.speed.current == mock_zone_types["charging"]["speed_limit"]

    def test_move_when_locked(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        with pytest.raises(AlreadyLockedError):
            bike.move((0.001, 0.001))

    def test_move_invalid_position_type(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        with pytest.raises(InvalidPositionTypeError):
            bike.move("invalid_position_type")

    def test_move_invalid_position_length(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        with pytest.raises(InvalidPositionLengthError):
            bike.move([0.001])

    def test_move_with_tuple(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        new_position = (0.002, 0.002)
        bike.move(new_position)
        assert bike.position.current == new_position

    def test_move_with_two_element_list(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        new_position = [0.002, 0.002]
        bike.move(new_position)
        assert bike.position.current == tuple(new_position)

    def test_move_with_multiple_positions_list(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        positions = [(0.001, 0.001), (0.002, 0.002), (0.003, 0.003)]
        bike.move(positions)
        assert bike.position.current == positions[-1]

    def test_relocate_to_charging_zone_success(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        charging_zone = Map.Zone.get_charging_zone(bike.zones)
        expected_position = Map.Zone.get_centroid_position(charging_zone)
        with patch('random.choice', return_value=charging_zone):
            bike.relocate_to_charging_zone()
        assert bike.position.current == expected_position

    def test_relocate_to_charging_zone_out_of_bounds(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        bike.relocate_to_charging_zone()
        with pytest.raises(OutOfBoundsError):
            position = (999.0, 999.0)
            bike.relocate(position, ignore_zone=False)

    def test_relocate_position_is_invalid_position(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        with pytest.raises(InvalidPositionTypeError):
            bike.relocate("invalid_position")

    def test_charging_in_charging_zone(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        charging_zone = Map.Zone.get_charging_zone(bike.zones)
        charging_position = Map.Zone.get_centroid_position(charging_zone)
        bike.relocate(charging_position)
        bike.battery.level = 50.0
        bike.charge(desired_level=100.0)
        assert bike.battery.level == 100.0

    def test_charging_outside_charging_zone(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        with pytest.raises(NotChargingZoneError):
            bike.charge(desired_level=100.0)

    def test_maintenance_mode_when_battery_is_low(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123, trip_id=456)
        bike.battery.level = 15.0
        bike.lock(ignore_zone=False)
        assert bike.mode.is_sleep()
        bike.check()
        assert bike.mode.is_maintenance()

    def test_deploy_bike(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        deployment_zone = next(zone for zone in mock_zones if zone["zone_type"] == "parking")
        expected_position = Map.Zone.get_centroid_position(deployment_zone)
        with patch('src._utils._map.Map.Zone.get_deployment_zone', return_value=deployment_zone):
            bike.deploy()
        deployed_position = bike.position.current
        assert deployed_position == expected_position, f"Deployed position {deployed_position} does not match expected {expected_position}"

    def test_check_out_of_bounds(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        with patch('src._utils._map.Map.Position.get_closest_zone') as mock_get_closest_zone:
            mock_closest_zone = {
                "id": 11,
                "zone_type": "regular",
                "city_id": 2,
                "boundary": "POLYGON((0.030 0.000, 0.030 0.001, 0.031 0.001, 0.031 0.000, 0.030 0.000))"
            }
            mock_get_closest_zone.return_value = mock_closest_zone
            with patch.object(bike, 'report') as mock_report:
                with pytest.raises(OutOfBoundsError) as exc_info:
                    bike.check()
                assert bike.mode.is_maintenance(), "Bike should be in maintenance mode."
                mock_report.assert_called_once(), "Report should be sent once."
                assert str(exc_info.value) == "This position is out of bounds. It is not in one of the zones on the map.", "Incorrect error message."

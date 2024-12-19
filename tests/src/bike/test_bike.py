import pytest
from src.bike.bike import Bike
from src._utils._errors import AlreadyUnlockedError, AlreadyLockedError, NotParkingZoneError, NotChargingZoneError
from src._utils._map import Map

@pytest.mark.usefixtures("mock_environment")
class TestBike:

    def test_unlocking_bike(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="bike_1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        assert bike.mode.is_locked()
        assert bike.user is None
        bike.unlock(user_id=123)
        assert bike.mode.is_unlocked()
        assert bike.user.user_id == 123
        with pytest.raises(AlreadyUnlockedError): # Attempt to unlock again should raise AlreadyUnlockedError.
            bike.unlock(user_id=456)

    def test_locking_bike_in_parking_zone(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="bike_1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123)
        assert bike.mode.is_unlocked()
        bike.lock(ignore_zone=False)
        assert bike.mode.is_locked()
        assert bike.user is None  # Trip ended.
        with pytest.raises(AlreadyLockedError): # Attempt to lock again without unlocking should raise AlreadyLockedError.
            bike.lock()

    def test_locking_bike_outside_parking_zone(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="bike_1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123)
        bike.relocate(0.0065, 0.0005) # Relocate the bike to a regular zone without draining battery.
        with pytest.raises(NotParkingZoneError): # Attempt to lock in non-parking zone without ignore_zone=True should fail.
            bike.lock(ignore_zone=False)
        bike.lock(ignore_zone=True) # Locking with ignore_zone=True should succeed.
        assert bike.mode.is_locked()

    def test_moving_bike(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="bike_1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123)
        initial_battery = bike.battery.level
        charging_zone = Map.Zone.get_charging_zone(bike.zones)
        charging_position = Map.Zone.get_position(charging_zone)
        bike.move(charging_position[0], charging_position[1])
        assert bike.battery.level < initial_battery # Check if battery drained.
        bike.speed.limit(bike.zones, bike.zone_types, bike.position.current)
        assert bike.speed.current == mock_zone_types["charging"]["speed_limit"]

    def test_charging_in_charging_zone(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="bike_1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123)
        charging_zone = Map.Zone.get_charging_zone(bike.zones)
        charging_position = Map.Zone.get_position(charging_zone)
        bike.relocate(charging_position[0], charging_position[1])
        bike.battery.level = 50.0  # Simulate partial battery.
        bike.charge(desired_level=100.0)
        assert bike.battery.level == 100.0

    def test_charging_outside_charging_zone(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="bike_1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123)
        with pytest.raises(NotChargingZoneError):
            bike.charge(desired_level=100.0)

    def test_maintenance_mode_when_battery_is_low(self, mock_zones, mock_zone_types):
        bike = Bike(bike_id="bike_1", longitude=0.0, latitude=0.0)
        bike.update(mock_zones, mock_zone_types)
        bike.unlock(user_id=123)
        bike.battery.level = 15.0 # Drain battery to below threshold.
        bike.lock(ignore_zone=False) # Lock bike (goes to sleep mode).
        assert bike.mode.is_sleep()
        bike.check() # Check() should detect low battery and switch to maintenance.
        assert bike.mode.is_maintenance()

import pytest
from src.bike._battery import Battery
from src._utils._errors import FullyChargedError
from src._utils._settings import Settings

class TestBattery:

    def test_initial_battery_level(self):
        battery = Battery()
        assert battery.level == 100.0

    def test_charge_battery(self):
        minutes = 5
        battery = Battery(battery_level=50.0)
        battery.charge(minutes=5)
        assert battery.level == 50.0 + Settings.Battery.recharge_per_minute * minutes

    def test_overcharge_battery(self):
        battery = Battery(battery_level=98.0)
        battery.charge(minutes=1)
        assert battery.level == 100.0

    def test_fully_charged_error(self):
        battery_level = 100.0
        battery = Battery(battery_level=battery_level)
        with pytest.raises(FullyChargedError):
            battery.get_charge_time(desired_level=battery_level)

    def test_drain_usage_mode(self):
        battery = Battery(battery_level=100.0)
        minutes = 10
        battery.drain(minutes=minutes, mode='usage')
        assert battery.level == 100.0 - (Settings.Battery.drain_per_minute * minutes * Settings.Battery.drain_factor_usage_mode)

    def test_drain_sleep_mode(self):
        minutes = 10
        battery_level = 100.0
        battery = Battery(battery_level=battery_level)
        battery.drain(minutes=minutes, mode='sleep')
        assert battery.level == 100.0 - (Settings.Battery.drain_per_minute * minutes * Settings.Battery.drain_factor_sleep_mode)

    def test_drain_maintenance_mode(self):
        battery_level = 100.0
        minutes = 10
        battery = Battery(battery_level=battery_level)
        battery.drain(minutes=minutes, mode='maintenance')
        assert battery.level == 100.0 - (Settings.Battery.drain_per_minute * minutes * Settings.Battery.drain_factor_maintenance_mode)

    def test_drain_invalid_mode(self):
        battery = Battery()
        with pytest.raises(Exception):
            battery.drain(minutes=10, mode='invalid_mode')

    def test_is_low_battery(self):
        battery = Battery(battery_level=19.9)
        assert battery.is_low() is True
        battery.level = 20.0
        assert battery.is_low() is False

    def test_get_charge_time_no_charging_needed(self):
        battery = Battery(battery_level=80.0)
        minutes_spent = battery.get_charge_time(desired_level=80.0)
        assert minutes_spent == 0
        minutes_spent = battery.get_charge_time(desired_level=70.0)
        assert minutes_spent == 0

    def test_drain_battery_below_zero(self):
        minutes = 5
        battery_level = 0.1 
        battery = Battery(battery_level=battery_level)
        battery.drain(minutes=minutes, mode='usage')
        assert battery.level == 0.0
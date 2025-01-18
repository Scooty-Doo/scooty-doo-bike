"""Tests for the Battery class."""

import pytest
from src.bike._battery import Battery
from src._utils._errors import FullyChargedError
from src._utils._settings import Settings

class TestBattery:
    """Tests for the Battery class."""

    def test_initial_battery_level(self):
        """Test the initial battery level."""
        battery = Battery()
        assert battery.level == 100.0

    def test_charge_battery(self):
        """Test charging the battery."""
        minutes = 5
        battery = Battery(battery_level=50.0)
        battery.charge(minutes=5)
        assert battery.level == 50.0 + Settings.Battery.recharge_per_minute * minutes

    def test_overcharge_battery(self):
        """Test overcharging the battery."""
        battery = Battery(battery_level=98.0)
        battery.charge(minutes=1)
        assert battery.level == 100.0

    def test_fully_charged_error(self):
        """Test the FullyChargedError exception."""
        battery_level = 100.0
        battery = Battery(battery_level=battery_level)
        with pytest.raises(FullyChargedError):
            battery.get_charge_time(desired_level=battery_level)

    def test_drain_usage_mode(self):
        """Test draining the battery in usage mode."""
        battery = Battery(battery_level=100.0)
        minutes = 10
        battery.drain(minutes=minutes, mode='usage')
        assert battery.level == 100.0 - \
            (Settings.Battery.drain_per_minute * minutes \
             * Settings.Battery.drain_factor_usage_mode)

    def test_drain_sleep_mode(self):
        """Test draining the battery in sleep mode."""
        minutes = 10
        battery_level = 100.0
        battery = Battery(battery_level=battery_level)
        battery.drain(minutes=minutes, mode='sleep')
        assert battery.level == 100.0 - \
            (Settings.Battery.drain_per_minute * minutes \
             * Settings.Battery.drain_factor_sleep_mode)

    def test_drain_maintenance_mode(self):
        """Test draining the battery in maintenance mode."""
        battery_level = 100.0
        minutes = 10
        battery = Battery(battery_level=battery_level)
        battery.drain(minutes=minutes, mode='maintenance')
        assert battery.level == 100.0 - \
            (Settings.Battery.drain_per_minute * minutes \
             * Settings.Battery.drain_factor_maintenance_mode)

    def test_drain_invalid_mode(self):
        """Test draining the battery with an invalid mode."""
        battery = Battery()
        with pytest.raises(Exception):
            battery.drain(minutes=10, mode='invalid_mode')

    def test_is_low_battery(self):
        """Test checking if the battery level is low."""
        battery = Battery(battery_level=19.9)
        assert battery.is_low() is True
        battery.level = 20.0
        assert battery.is_low() is False

    def test_get_charge_time_no_charging_needed(self):
        """Test getting the charge time when no charging is needed."""
        battery = Battery(battery_level=80.0)
        minutes_spent = battery.get_charge_time(desired_level=80.0)
        assert minutes_spent == 0
        minutes_spent = battery.get_charge_time(desired_level=70.0)
        assert minutes_spent == 0

    def test_drain_battery_below_zero(self):
        """Test draining the battery below zero."""
        minutes = 5
        battery_level = 0.1
        battery = Battery(battery_level=battery_level)
        battery.drain(minutes=minutes, mode='usage')
        assert battery.level == 0.0

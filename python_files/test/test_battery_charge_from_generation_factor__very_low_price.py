from src.entities.battery_charge_from_generation_factor import BatteryChargeFromGenerationFactor
from unittest import TestCase


BATTERY_CHARGE_FROM_GRID_FACTOR = 3


class TestBatteryChargeFromGenerationFactor__VeryLowPrice(TestCase):

    def test__get_factor__very_very_poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=0.1
        )
        assert factor == 1166666666.67

    def test__get_factor__very_poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=1
        )
        assert factor == 116666.67

    def test__get_factor__poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=3
        )
        assert factor == 1440.33
        # assert BatteryParameterSetter.get_power(factor) == 3000

    def test__get_factor__ok_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=5
        )
        assert factor == 186.67

    def test__get_factor__good_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=10
        )
        assert factor == 11.67

    def test__get_factor__very_good_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=15
        )
        assert factor == 2.3

    def test__get_factor__very_good_forecast__(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=4.3,
            battery_left_to_charge=3,
            energy_still_to_be_produced=15
        )
        assert factor == 0.15

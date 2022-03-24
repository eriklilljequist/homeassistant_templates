from src.entities.battery_charge_from_generation_factor import BatteryChargeFromGenerationFactor
from src.battery_parameter_setter import BatteryParameterSetter
from unittest import TestCase


BATTERY_CHARGE_FROM_GRID_FACTOR = 0.1


class TestBatteryChargeFromGenerationFactor__VeryHighPrice(TestCase):

    def test__get_factor__very_very_poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=0.1
        )
        assert factor == 3070.18

    def test__get_factor__very_poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=1
        )
        assert factor == 30.7

    def test__get_factor__poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=3
        )
        assert factor == 3.41
        # assert BatteryParameterSetter.get_power(factor) == 3000

    def test__get_factor__ok_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=5
        )
        assert factor == 1.23

    def test__get_factor__good_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=10
        )
        assert factor == 0.31

    def test__get_factor__very_good_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            energy_still_to_be_produced=15
        )
        assert factor == 0.14

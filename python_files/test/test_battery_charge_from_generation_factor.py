from src.entities.battery_charge_from_generation_factor import BatteryChargeFromGenerationFactor
from src.battery_parameter_setter import BatteryParameterSetter
from unittest import TestCase


class TestBatteryChargeFromGenerationFactor(TestCase):

    def test__get_factor__poor_forecast__low_price(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=1.5,
            battery_left_to_charge=5,
            energy_still_to_be_produced=3
        )
        assert factor == 3.5
        assert BatteryParameterSetter.get_power(factor) == 3000

    def test__get_factor__good_forecast__very_low_price(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=3,
            battery_left_to_charge=5,
            energy_still_to_be_produced=10
        )
        assert factor == 2.1

    def test__get_factor__good_forecast__low_price(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=1.5,
            battery_left_to_charge=5,
            energy_still_to_be_produced=10
        )
        assert factor == 1.05

    def test__get_factor__very_poor_forecast_very_high_price(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=0.1,
            battery_left_to_charge=5,
            energy_still_to_be_produced=1
        )
        assert factor == 0.7

    def test__get_factor__ok_forecast__very_high_price(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=0.1,
            battery_left_to_charge=5,
            energy_still_to_be_produced=5
        )
        assert factor == 0.14

    def test__get_factor__good_forecast__very_high_price(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=0.1,
            battery_left_to_charge=5,
            energy_still_to_be_produced=8
        )
        assert factor == 0.09

    def test__get_factor__very_good_forecast__very_high_price(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=0.1,
            battery_left_to_charge=5,
            energy_still_to_be_produced=15
        )
        assert factor == 0.05

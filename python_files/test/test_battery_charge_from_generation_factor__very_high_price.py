from src.entities.battery_charge_from_generation_factor import BatteryChargeFromGenerationFactor
from src.battery_parameter_setter import BatteryParameterSetter
from unittest import TestCase


BATTERY_CHARGE_FROM_GRID_FACTOR = 0.1


class TestBatteryChargeFromGenerationFactor__VeryHighPrice(TestCase):

    def test__get_factor__very_very_poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=11,
            daily_yield_battery_accounted=10
        )
        assert factor > 302.5

    def test__get_factor__very_poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=12,
            daily_yield_battery_accounted=10
        )
        assert factor == 90

    def test__get_factor__poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=13,
            daily_yield_battery_accounted=10
        )
        assert factor == 20.86
        assert BatteryParameterSetter.get_power(factor) == 3000

    def test__get_factor__ok_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=6,
            estimated_energy_production_today=15,
            daily_yield_battery_accounted=10
        )
        assert factor == 5.18
        assert BatteryParameterSetter.get_power(factor) == 3000

    def test__get_factor__good_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=15,
            daily_yield_battery_accounted=5
        )
        assert factor == 0.23
        assert BatteryParameterSetter.get_power(factor) == 345

    def test__get_factor__very_good_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=20,
            daily_yield_battery_accounted=5
        )
        assert factor == 0.08

    def test__get_factor__very_good_forecast__battery_empty(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=9,
            estimated_energy_production_today=20,
            daily_yield_battery_accounted=5
        )
        assert factor == 0.26

    def test__get_factor__very_good_forecast__battery_full(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=0,
            estimated_energy_production_today=20,
            daily_yield_battery_accounted=5
        )
        assert factor == 0.0

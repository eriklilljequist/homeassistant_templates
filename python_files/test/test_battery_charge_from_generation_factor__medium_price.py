from src.entities.battery_charge_from_generation_factor import BatteryChargeFromGenerationFactor
from src.battery_parameter_setter import BatteryParameterSetter
from unittest import TestCase


BATTERY_CHARGE_FROM_GRID_FACTOR = 1


class TestBatteryChargeFromGenerationFactor__MediumPrice(TestCase):

    def test__get_factor__very_very_poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=1,
            daily_yield_battery_accounted=0
        )
        assert factor > 20

    def test__get_factor__very_poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=2,
            daily_yield_battery_accounted=0
        )
        assert factor > 6.25 and factor < 30

    def test__get_factor__poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=3,
            daily_yield_battery_accounted=0
        )
        assert factor == 11.11
        assert BatteryParameterSetter.get_power(factor) == 3000

    def test__get_factor__ok_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=10,
            daily_yield_battery_accounted=5
        )
        assert factor == 16
        assert BatteryParameterSetter.get_power(factor) == 3000

    def test__get_factor__good_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=20,
            daily_yield_battery_accounted=10
        )
        assert factor == 4
        assert BatteryParameterSetter.get_power(factor) == 3000

    def test__get_factor__very_good_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=20,
            daily_yield_battery_accounted=5
        )
        assert factor == 0.79

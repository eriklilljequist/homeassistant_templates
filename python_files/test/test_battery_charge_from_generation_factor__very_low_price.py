from src.entities.battery_charge_from_generation_factor import BatteryChargeFromGenerationFactor
from unittest import TestCase


BATTERY_CHARGE_FROM_GRID_FACTOR = 3


class TestBatteryChargeFromGenerationFactor__VeryLowPrice(TestCase):

    def test__get_factor__very_very_poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=0.1,
            daily_yield_battery_accounted=0
        )
        assert factor == 30603

    def test__get_factor__very_poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=1,
            daily_yield_battery_accounted=0
        )
        assert factor == 363

    def test__get_factor__poor_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=3,
            daily_yield_battery_accounted=0
        )
        assert factor == 56.33
        # assert BatteryParameterSetter.get_power(factor) == 3000

    def test__get_factor__ok_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=5,
            daily_yield_battery_accounted=0
        )
        assert factor == 27

    def test__get_factor__good_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=10,
            daily_yield_battery_accounted=0
        )
        assert factor == 12

    def test__get_factor__very_good_forecast(self):
        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=BATTERY_CHARGE_FROM_GRID_FACTOR,
            battery_left_to_charge=5,
            estimated_energy_production_today=15,
            daily_yield_battery_accounted=0
        )
        assert factor == 8.33

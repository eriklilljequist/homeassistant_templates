from src.battery_charge_from_grid_factor import BatteryChargeFromGridFactor
from unittest import TestCase

march_8th = {
    'today': [2.12, 1.31, 1.61, 2.06, 2.38, 3.03, 3.23, 9.1, 8.58, 5.45, 3.12, 2.9, 2.83, 2.82, 2.78, 2.93, 2.72, 3.16, 3.73, 3.41, 3.12, 3.03, 2.94, 2.2],
    'tomorrow': [2.04, 1.98, 1.94, 1.78, 2.23, 3.03, 3.4, 7.88, 7.36, 3.33, 3.17, 3.12, 3.09, 3.03, 2.99, 3, 2.95, 3.06, 3.13, 3.08, 3.02, 2.97, 1.07, 0.42]
}

march_9th = {
    'tomorrow': [],
    'today': [2.04, 1.98, 1.94, 1.78, 2.23, 3.03, 3.4, 7.88, 7.36, 3.33, 3.17, 3.12, 3.09, 3.03, 2.99, 3, 2.95, 3.06, 3.13, 3.08, 3.02, 2.97, 1.07, 0.42]
}


class TestBatteryChargeFromGridFactor(TestCase):

    def test__march_8th__1200(self):
        hour_current = 12
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_8th['today'] + march_8th['tomorrow'],
            price_current=march_8th['today'][hour_current]
        )
        assert factor > 0.61 and factor < 0.7

    def test__march_8th__2200(self):
        hour_current = 22
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_8th['today'] + march_8th['tomorrow'],
            price_current=march_8th['today'][hour_current]
        )
        assert factor > 0.62 and factor < 0.7

    def test__march_8th__2300(self):
        hour_current = 23
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_8th['today'] + march_8th['tomorrow'],
            price_current=march_8th['today'][hour_current]
        )
        assert factor > 1 and factor < 1.1
        assert BatteryChargeFromGridFactor.get_max_grid_charging_power(factor) > 1500

    def test__march_9th__0800(self):
        hour_current = 8
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_9th['today'] + march_9th['tomorrow'],
            price_current=march_9th['today'][hour_current]
        )
        assert factor > 0.1 and factor < 0.2
        assert BatteryChargeFromGridFactor.get_max_grid_charging_power(factor) < 500

    def test__march_9th__0900(self):
        hour_current = 9
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_9th['today'] + march_9th['tomorrow'],
            price_current=march_9th['today'][hour_current]
        )
        assert factor > 0.4 and factor < 0.5

    def test__get_max_grid_charging_power(self):
        assert BatteryChargeFromGridFactor.get_max_grid_charging_power(factor=2.34) == 3000
        assert BatteryChargeFromGridFactor.get_max_grid_charging_power(factor=1.3) == 1950
        assert BatteryChargeFromGridFactor.get_max_grid_charging_power(factor=1) == 1500
        assert BatteryChargeFromGridFactor.get_max_grid_charging_power(factor=0.34) == 510

    def test__get_max_discharging_power(self):
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=2.34) == 641
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=1.3) == 1153
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=1) == 1500
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=0.51) == 2941
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=0.5) == 3000
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=0.34) == 3000
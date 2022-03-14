from src.battery_charge_from_grid_factor import BatteryChargeFromGridFactor
from unittest import TestCase
from datetime import datetime
import pytz


def test__time():
    zone_se = pytz.timezone('Europe/Stockholm')
    datetime.now(tz=zone_se).hour
    pass

march_8th = {
    'today': [2.12, 1.31, 1.61, 2.06, 2.38, 3.03, 3.23, 9.1, 8.58, 5.45, 3.12, 2.9, 2.83, 2.82, 2.78, 2.93, 2.72, 3.16, 3.73, 3.41, 3.12, 3.03, 2.94, 2.2],
    'tomorrow': [2.04, 1.98, 1.94, 1.78, 2.23, 3.03, 3.4, 7.88, 7.36, 3.33, 3.17, 3.12, 3.09, 3.03, 2.99, 3, 2.95, 3.06, 3.13, 3.08, 3.02, 2.97, 1.07, 0.42]
}

march_9th = {
    'today': [2.04, 1.98, 1.94, 1.78, 2.23, 3.03, 3.4, 7.88, 7.36, 3.33, 3.17, 3.12, 3.09, 3.03, 2.99, 3, 2.95, 3.06, 3.13, 3.08, 3.02, 2.97, 1.07, 0.42],
    'tomorrow': [0.29, 0.17, 0.17, 0.19, 0.27, 0.84, 0.98, 3.13, 3.14, 3.06, 1.61, 1.39, 1.67, 1.97, 1.61, 2.63, 2.91, 2.97, 3.01, 2.97, 2.35, 0.83, 0.68, 0.19]
}

march_10th = {
    'today': [0.29, 0.17, 0.17, 0.19, 0.27, 0.84, 0.98, 3.13, 3.14, 3.06, 1.61, 1.39, 1.67, 1.97, 1.61, 2.63, 2.91, 2.97, 3.01, 2.97, 2.35, 0.83, 0.68, 0.19],
    'tomorrow': []
}


class TestBatteryChargeFromGridFactor(TestCase):

    def test__march_8th__1200(self):
        hour_current = 12
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_8th['today'] + march_8th['tomorrow'],
            price_current=march_8th['today'][hour_current]
        )
        assert factor > 0.7 and factor < 0.8

    def test__march_8th__2200(self):
        hour_current = 22
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_8th['today'] + march_8th['tomorrow'],
            price_current=march_8th['today'][hour_current]
        )
        assert factor > 0.8 and factor < 0.9

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
        assert factor > 0.3 and factor < 0.4

    def test__march_9th__0900(self):
        hour_current = 9
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_9th['today'] + march_9th['tomorrow'],
            price_current=march_9th['today'][hour_current]
        )
        assert factor > 0.6 and factor < 0.7

    def test__march_9th__2100(self):
        hour_current = 21
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_9th['today'] + march_9th['tomorrow'],
            price_current=march_9th['today'][hour_current]
        )
        assert factor > 0.2 and factor < 0.3

    def test__march_9th__2200(self):
        hour_current = 22
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_9th['today'] + march_9th['tomorrow'],
            price_current=march_9th['today'][hour_current]
        )
        assert factor > 0.7 and factor < 0.8

    def test__march_9th__2300(self):
        hour_current = 23
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_9th['today'] + march_9th['tomorrow'],
            price_current=march_9th['today'][hour_current]
        )
        assert factor > 1.9 and factor < 2.1

    def test__march_10th__0000(self):
        hour_current = 0
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_10th['today'] + march_10th['tomorrow'],
            price_current=march_10th['today'][hour_current]
        )
        assert 3000 == BatteryChargeFromGridFactor.get_max_grid_charging_power(factor)
        assert factor > 3 and factor < 3.2

    def test__march_10th__0300(self):
        hour_current = 3
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_10th['today'] + march_10th['tomorrow'],
            price_current=march_10th['today'][hour_current]
        )
        assert 3000 == BatteryChargeFromGridFactor.get_max_grid_charging_power(factor)
        assert factor > 6 and factor < 6.5

    def test__march_10th__0600(self):
        hour_current = 6
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_10th['today'] + march_10th['tomorrow'],
            price_current=march_10th['today'][hour_current]
        )
        assert factor > 1.6 and factor < 1.7

    def test__march_10th__1100(self):
        hour_current = 11
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_10th['today'] + march_10th['tomorrow'],
            price_current=march_10th['today'][hour_current]
        )
        assert factor > 1 and factor < 1.1

    def test__march_10th__1200(self):
        hour_current = 12
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            hour_current=hour_current,
            prices_all=march_10th['today'] + march_10th['tomorrow'],
            price_current=march_10th['today'][hour_current]
        )
        assert factor > 0.8 and factor < 0.9

    def test__get_max_grid_charging_power(self):
        assert BatteryChargeFromGridFactor.get_max_grid_charging_power(factor=2.34) == 3000
        assert BatteryChargeFromGridFactor.get_max_grid_charging_power(factor=1.3) == 1950
        assert BatteryChargeFromGridFactor.get_max_grid_charging_power(factor=1) == 1500
        assert BatteryChargeFromGridFactor.get_max_grid_charging_power(factor=0.34) == 510

    def test__get_max_discharging_power(self):
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=2.34) == 641
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=1.3) == 1153
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=1) == 1500
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=0.48) == 3000
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=0.5) == 3000
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=0.51) == 2941
        assert BatteryChargeFromGridFactor.get_max_discharging_power(factor=0.34) == 3000

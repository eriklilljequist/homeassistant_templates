from src.entities.battery_discharge_factor import BatteryDischargeFactor
from src.battery_parameter_setter import BatteryParameterSetter
from unittest import TestCase
from src.utilities import config


class TestBatteryDischargeFactor(TestCase):

    def test__get_factor__low_price(self):
        price_threshold_factor = 0.3 / config.THRESHOLD_FACTOR
        factor = BatteryDischargeFactor.get_factor(battery_charge_from_grid_factor=1.5, price_threshold_factor=price_threshold_factor)
        assert factor == 0.14
        assert BatteryParameterSetter.get_power(factor) == 210

    def test__get_factor__medium_price(self):
        price_threshold_factor = 1.3 / config.THRESHOLD_FACTOR
        factor = BatteryDischargeFactor.get_factor(battery_charge_from_grid_factor=1.5, price_threshold_factor=price_threshold_factor)
        assert factor == 0.62
        assert BatteryParameterSetter.get_power(factor) == 930

    def test__get_factor__high_price(self):
        price_threshold_factor = 0.24 / config.THRESHOLD_FACTOR
        factor = BatteryDischargeFactor.get_factor(battery_charge_from_grid_factor=0.65, price_threshold_factor=price_threshold_factor)
        assert factor == 0.26
        assert BatteryParameterSetter.get_power(factor) == 390

    def test__get_max_discharging_power(self):
        assert BatteryParameterSetter.get_power(factor=1 / 2.34) == 641
        assert BatteryParameterSetter.get_power(factor=1 / 1.3) == 1153
        assert BatteryParameterSetter.get_power(factor=1 / 1) == 1500
        assert BatteryParameterSetter.get_power(factor=1 / 0.48) == 3000
        assert BatteryParameterSetter.get_power(factor=1 / 0.5) == 3000
        assert BatteryParameterSetter.get_power(factor=1 / 0.51) == 2941
        assert BatteryParameterSetter.get_power(factor=1 / 0.34) == 3000

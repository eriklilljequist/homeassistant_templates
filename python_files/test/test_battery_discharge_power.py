from src.entities.battery_discharge_factor import BatteryDischargeFactor
from src.entities.price_threshold_factor import PriceThresholdFactor
from src.battery_parameter_setter import BatteryParameterSetter
from unittest import TestCase


class TestBatteryDischargeFactor(TestCase):

    def test__get_factor__low_price(self):
        price_threshold_factor = PriceThresholdFactor.get_factor(price_current=0.3)
        factor = BatteryDischargeFactor.get_factor(battery_charge_from_grid_factor=2, price_threshold_factor=price_threshold_factor)
        assert factor == 0.1
        assert BatteryParameterSetter.get_power(factor) == 150

    def test__get_factor__medium_price(self):
        price_threshold_factor = PriceThresholdFactor.get_factor(price_current=1.3)
        factor = BatteryDischargeFactor.get_factor(battery_charge_from_grid_factor=1.5, price_threshold_factor=price_threshold_factor)
        assert factor == 0.62
        assert BatteryParameterSetter.get_power(factor) == 930

    def test__get_factor__high_price(self):
        price_threshold_factor = PriceThresholdFactor.get_factor(price_current=2.24)
        factor = BatteryDischargeFactor.get_factor(battery_charge_from_grid_factor=0.5, price_threshold_factor=price_threshold_factor)
        assert factor == 3.2
        assert BatteryParameterSetter.get_power(factor) == 3000

    def test__get_max_discharging_power(self):
        assert BatteryParameterSetter.get_power(factor=1 / 2.34) == 641
        assert BatteryParameterSetter.get_power(factor=1 / 1.3) == 1153
        assert BatteryParameterSetter.get_power(factor=1 / 1) == 1500
        assert BatteryParameterSetter.get_power(factor=1 / 0.48) == 3000
        assert BatteryParameterSetter.get_power(factor=1 / 0.5) == 3000
        assert BatteryParameterSetter.get_power(factor=1 / 0.51) == 2941
        assert BatteryParameterSetter.get_power(factor=1 / 0.34) == 3000

from src.entities.battery_discharge_factor import BatteryDischargeFactor
from src.battery_parameter_setter import BatteryParameterSetter
from unittest import TestCase


class TestBatteryDischargeFactor(TestCase):

    def test__get_factor__low_price(self):
        factor = BatteryDischargeFactor.get_factor(battery_charge_from_grid_factor=1.5)
        assert factor == 0.67
        assert BatteryParameterSetter.get_power(factor) == 1005

    def test__get_max_discharging_power(self):
        assert BatteryParameterSetter.get_power(factor=1 / 2.34) == 641
        assert BatteryParameterSetter.get_power(factor=1 / 1.3) == 1153
        assert BatteryParameterSetter.get_power(factor=1 / 1) == 1500
        assert BatteryParameterSetter.get_power(factor=1 / 0.48) == 3000
        assert BatteryParameterSetter.get_power(factor=1 / 0.5) == 3000
        assert BatteryParameterSetter.get_power(factor=1 / 0.51) == 2941
        assert BatteryParameterSetter.get_power(factor=1 / 0.34) == 3000

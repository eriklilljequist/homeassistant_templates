from src.utilities import config
import hassapi


class BatteryParameterSetter(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.set_battery_working_mode, 'sensor.battery_charge_from_grid_factor', constrain_presence='everyone')
        self.listen_state(self.set_battery_charge_from_grid, 'sensor.battery_charge_from_grid_factor', constrain_presence='everyone')
        self.listen_state(self.set_maximum_discharging_power, 'sensor.battery_discharge_factor', constrain_presence='everyone')
        self.listen_state(self.set_maximum_charging_power, 'sensor.battery_charge_from_generation_factor', constrain_presence='everyone')

    def set_battery_working_mode(self, entity, attribute, old, new, kwargs):
        battery_charge_from_grid_factor = float(self.entities.sensor.battery_charge_from_grid_factor.state)
        if battery_charge_from_grid_factor > 1:
            self.log('battery_charge_from_grid_factor is greater than 1, setting Time Of Use and charge from grid')
            self.select_option('select.working_mode', 'Time Of Use')
            self.turn_on('switch.charge_from_grid')
        else:
            self.log('battery_charge_from_grid_factor is less than 1, setting Maximise Self Consumption and NOT charge from grid')
            self.select_option('select.working_mode', 'Maximise Self Consumption')
            self.turn_off('switch.charge_from_grid')

    def set_battery_charge_from_grid(self, entity, attribute, old, new, kwargs):
        battery_charge_from_grid_factor = float(self.entities.sensor.battery_charge_from_grid_factor.state)
        power = BatteryParameterSetter.get_power(battery_charge_from_grid_factor)
        self.log(f'battery_charge_from_grid_factor is {battery_charge_from_grid_factor} setting grid_charge_maximum_power to {power}')
        self.set_value('number.grid_charge_maximum_power', value=power)

    def set_maximum_discharging_power(self, entity, attribute, old, new, kwargs):
        battery_discharge_factor = float(self.entities.sensor.battery_discharge_factor.state)
        power = BatteryParameterSetter.get_power(factor=battery_discharge_factor, nominal_power=2500)
        self.log(f'battery_discharge_factor is {battery_discharge_factor} setting maximum_discharging_power to {power}')
        self.set_value('number.maximum_discharging_power', value=power)

    def set_maximum_charging_power(self, entity, attribute, old, new, kwargs):
        battery_charge_from_generation_factor = float(self.entities.sensor.battery_charge_from_generation_factor.state)
        power = BatteryParameterSetter.get_power(
            factor=battery_charge_from_generation_factor,
            nominal_power=config.BATTERY_MAXIMUM_CHARGE_POWER,
            max_power=config.BATTERY_MAXIMUM_CHARGE_POWER)
        self.log(f'battery_charge_from_generation_factor is {battery_charge_from_generation_factor} setting maximum_charging_power to {power}')
        self.set_value('number.maximum_charging_power', value=power)

    @staticmethod
    def get_power(factor, nominal_power=1500, max_power=3000):
        return min(int(nominal_power * factor), max_power)

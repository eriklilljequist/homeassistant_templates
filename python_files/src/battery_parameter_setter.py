import hassapi


class BatteryParameterSetter(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.set_battery_working_mode, 'sensor.battery_charge_from_grid_factor', constrain_presence='everyone')
        self.listen_state(self.set_battery_charge_from_grid_power, 'sensor.battery_charge_from_grid_factor', constrain_presence='everyone')
        self.listen_state(self.set_maximum_discharging_power, 'sensor.battery_discharge_factor', constrain_presence='everyone')
        self.listen_state(self.set_maximum_charging_power, 'sensor.battery_charge_from_generation_factor', constrain_presence='everyone')
        self.listen_state(self.set_grid_charge_cutoff_soc, 'sensor.energy_production_today_2', constrain_presence='everyone')

    def set_grid_charge_cutoff_soc(self, *_):
        estimated_energy_production_today = float(self.entities.sensor.energy_production_today_2.state)
        if estimated_energy_production_today > 15:
            self.set_value('number.grid_charge_cutoff_soc', value=90)
        else:
            self.set_value('number.grid_charge_cutoff_soc', value=70)

    def set_battery_working_mode(self, entity, attribute, old, new, kwargs):
        battery_charge_from_grid_factor = float(self.entities.sensor.battery_charge_from_grid_factor.state)
        if battery_charge_from_grid_factor > 1:
            self.log('battery_charge_from_grid_factor is greater than 1, setting charge from grid')
            self.select_option('select.working_mode', 'Time Of Use')
            self.turn_on('switch.charge_from_grid')
        else:
            self.log('battery_charge_from_grid_factor is less than 1, Setting NOT charge from grid')
            self.select_option('select.working_mode', 'Maximise Self Consumption')
            self.turn_off('switch.charge_from_grid')

    def set_battery_charge_from_grid_power(self, entity, attribute, old, new, kwargs):
        battery_charge_from_grid_factor = float(self.entities.sensor.battery_charge_from_grid_factor.state)
        power = BatteryParameterSetter.get_power(battery_charge_from_grid_factor)
        self.log(f'battery_charge_from_grid_factor is {battery_charge_from_grid_factor} setting grid_charge_maximum_power to {power}')
        self.set_value('number.grid_charge_maximum_power', value=power)

    def set_maximum_discharging_power(self, entity, attribute, old, new, kwargs):
        battery_discharge_factor = float(self.entities.sensor.battery_discharge_factor.state)
        power = BatteryParameterSetter.get_power(factor=battery_discharge_factor)
        self.log(f'battery_discharge_factor is {battery_discharge_factor} setting maximum_discharging_power to {power}')
        self.set_value('number.maximum_discharging_power', value=power)

    def set_maximum_charging_power(self, entity, attribute, old, new, kwargs):
        battery_charge_from_generation_factor = float(self.entities.sensor.battery_charge_from_generation_factor.state)
        grid_charge_power = int(self.entities.number.grid_charge_maximum_power.state)
        power = BatteryParameterSetter.get_power(
            factor=battery_charge_from_generation_factor)
        self.log(f'Maximum charge power calculated to {power}')
        self.log(f'Maximum grid_charge_power is {grid_charge_power}')
        selected_power = max(power, grid_charge_power)
        self.log(f'Setting maximum_charging_power to {selected_power}')
        self.set_value('number.maximum_charging_power', value=selected_power)

    @staticmethod
    def get_power(factor, nominal_power=1500, max_power=3000):
        return min(int(nominal_power * factor), max_power)

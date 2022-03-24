import hassapi
from src.utilities import config


class BatteryChargeFromGenerationFactor(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.charge_from_grid_factor_change, 'sensor.battery_charge_from_grid_factor', constrain_presence='everyone')

    def charge_from_grid_factor_change(self, entity, attribute, old, new, kwargs):
        self.execute()

    def execute(self):
        daily_yield_battery_accounted = round(float(self.entities.sensor.daily_yield_battery_accounted.state))
        estimated_energy_production_today = float(self.entities.sensor.energy_production_today_2.state)
        battery_soc = float(self.entities.sensor.battery_state_of_capacity.state)
        battery_charge_from_grid_factor = float(self.entities.sensor.battery_charge_from_grid_factor.state)

        energy_still_to_be_produced = estimated_energy_production_today - daily_yield_battery_accounted
        battery_left_to_charge = battery_soc / config.BATTERY_GROSS_CAPACITY

        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=battery_charge_from_grid_factor,
            energy_still_to_be_produced=energy_still_to_be_produced,
            battery_left_to_charge=battery_left_to_charge
        )
        self.log(f'battery_charge_from_grid_factor is : {battery_charge_from_grid_factor}')
        self.log(f'energy_still_to_be_produced is : {energy_still_to_be_produced}')
        self.log(f'battery_left_to_charge is : {battery_left_to_charge}')
        self.log(f'setting battery_charge_from_generation_factor to : {factor}')
        self.set_state('sensor.battery_charge_from_generation_factor', state=factor)

    @staticmethod
    def get_factor(battery_charge_from_grid_factor, energy_still_to_be_produced, battery_left_to_charge):
        soc_factor = battery_left_to_charge / energy_still_to_be_produced
        return round((soc_factor * battery_charge_from_grid_factor) * config.THRESHOLD_FACTOR, 2)

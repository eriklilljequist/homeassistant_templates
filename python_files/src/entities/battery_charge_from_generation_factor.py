import hassapi
from src.utilities import config, utils
from datetime import datetime
import pytz


class BatteryChargeFromGenerationFactor(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.charge_from_grid_factor_change, 'sensor.battery_charge_from_grid_factor', constrain_presence='everyone')
        self.zone_se = pytz.timezone('Europe/Stockholm')
        self.run_every(self.from_schedule, datetime.now(tz=self.zone_se), 1 * 60)

    def from_schedule(self, kwargs):
        if config.RUN_ON_SCHEDULE:
            self.log('Executing on schedule!')
            self.execute()

    def charge_from_grid_factor_change(self, entity, attribute, old, new, kwargs):
        self.execute()

    def execute(self):
        daily_yield_battery_accounted = round(float(self.entities.sensor.daily_yield_battery_accounted.state))
        estimated_energy_production_today = utils.as_float(
            logger=self.log,
            string=self.entities.sensor.energy_production_today_2.state,
            or_else=1,
            not_less_than=1
        )
        battery_soc = float(self.entities.sensor.battery_state_of_capacity.state)
        battery_charge_from_grid_factor = float(self.entities.sensor.battery_charge_from_grid_factor.state)

        battery_left_to_charge = round(config.BATTERY_GROSS_CAPACITY - (config.BATTERY_GROSS_CAPACITY * battery_soc / 100), 2)

        factor = BatteryChargeFromGenerationFactor.get_factor(
            battery_charge_from_grid_factor=battery_charge_from_grid_factor,
            estimated_energy_production_today=estimated_energy_production_today,
            battery_left_to_charge=battery_left_to_charge,
            daily_yield_battery_accounted=daily_yield_battery_accounted
        )
        self.log(f'battery_charge_from_grid_factor is : {battery_charge_from_grid_factor}')
        self.log(f'battery_left_to_charge is : {battery_left_to_charge}')
        self.log(f'setting battery_charge_from_generation_factor to : {factor}')
        self.set_state('sensor.battery_charge_from_generation_factor', state=factor)

    @staticmethod
    def get_factor(battery_charge_from_grid_factor, estimated_energy_production_today, battery_left_to_charge, daily_yield_battery_accounted):
        energy_still_to_be_produced = round(max(estimated_energy_production_today - daily_yield_battery_accounted, 1), 2)
        still_to_produce_factor = max(estimated_energy_production_today / energy_still_to_be_produced, 1)
        soc_factor = (battery_left_to_charge * 2) / energy_still_to_be_produced  # Times 2 in order to have som margin
        return round(pow(soc_factor, 2) * pow(still_to_produce_factor, 2) * battery_charge_from_grid_factor, 2)

import hassapi
from datetime import datetime
import pytz
from src.utilities import config, utils


class BatteryGridChargeCutoffFactor(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.energy_production_today_change, "sensor.energy_production_today_2", constrain_presence="everyone")
        self.zone_se = pytz.timezone('Europe/Stockholm')
        self.run_every(self.from_schedule, datetime.now(tz=self.zone_se), 1 * 60)

    def from_schedule(self, kwargs):
        if config.RUN_ON_SCHEDULE:
            self.log('Executing on schedule!')
            self.execute()

    def energy_production_today_change(self, entity, attribute, old, new, kwargs):
        self.execute()

    def execute(self):
        estimated_energy_production_today = utils.as_float(
            logger=self.log,
            string=self.entities.sensor.energy_production_today_2.state,
            or_else=config.FORECAST_THRESHOLD,
            not_less_than=1
        )
        factor = BatteryGridChargeCutoffFactor.get_factor(estimated_energy_production_today)
        self.set_state('sensor.battery_grid_charge_cutoff_factor', state=factor)

    @staticmethod
    def get_factor(estimated_energy_production_today):
        return round(config.FORECAST_THRESHOLD / estimated_energy_production_today, 2)

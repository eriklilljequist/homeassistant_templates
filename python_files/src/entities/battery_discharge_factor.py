import hassapi
from datetime import datetime
import pytz
from src.utilities import config


class BatteryDischargeFactor(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.charge_from_grid_factor_change, "sensor.battery_charge_from_grid_factor", constrain_presence="everyone")
        self.zone_se = pytz.timezone('Europe/Stockholm')
        self.run_every(self.from_schedule, datetime.now(tz=self.zone_se), 1 * 60)

    def from_schedule(self, kwargs):
        if config.RUN_ON_SCHEDULE:
            self.log('Executing on schedule!')
            self.execute()

    def charge_from_grid_factor_change(self, entity, attribute, old, new, kwargs):
        self.execute()

    def execute(self):
        battery_charge_from_grid_factor = float(self.entities.sensor.battery_charge_from_grid_factor.state)
        price_threshold_factor = float(self.entities.sensor.price_threshold_factor.state)
        factor = BatteryDischargeFactor.get_factor(battery_charge_from_grid_factor, price_threshold_factor)
        self.set_state('sensor.battery_discharge_factor', state=factor)

    @staticmethod
    def get_factor(battery_charge_from_grid_factor, price_threshold_factor):
        return round((1 / battery_charge_from_grid_factor) * price_threshold_factor, 2)

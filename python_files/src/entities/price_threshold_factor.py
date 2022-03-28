import hassapi
from datetime import datetime
from src.utilities import config


class PriceThresholdFactor(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.nordpool_price_change, 'sensor.nordpool_kwh_se3_sek_2_10_025', constrain_presence='everyone')
        self.run_every(self.from_schedule, datetime.now(), 1 * 60)

    def from_schedule(self, kwargs):
        # if config.RUN_ON_SCHEDULE:
        #     self.log('Executing on schedule!')
        self.execute()

    def nordpool_price_change(self, entity, attribute, old, new, kwargs):
        self.execute()

    def execute(self):
        price_current = self.entities.sensor.nordpool_kwh_se3_sek_2_10_025.attributes.current_price
        factor = PriceThresholdFactor.get_factor(price_current)
        self.log(f'price_threshold_factor calculuated to {factor}')
        self.set_state('sensor.price_threshold_factor', state=factor)

    @staticmethod
    def get_factor(price_current):
        return round(price_current / config.THRESHOLD_FACTOR, 2)

import hassapi
from datetime import datetime
import pytz
from src.utilities import config


class BatteryChargeFromGridFactor(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.nordpool_price_change, 'sensor.nordpool_kwh_se3_sek_2_10_025', constrain_presence='everyone')
        self.zone_se = pytz.timezone('Europe/Stockholm')
        self.run_every(self.from_schedule, datetime.now(tz=self.zone_se), 1 * 60)

    def from_schedule(self, kwargs):
        if config.RUN_ON_SCHEDULE:
            self.log('Executing on schedule!')
            self.execute()

    def nordpool_price_change(self, entity, attribute, old, new, kwargs):
        self.execute()

    def execute(self):
        nordpool_sensor = self.entities.sensor.nordpool_kwh_se3_sek_2_10_025
        hour_current = datetime.now(tz=self.zone_se).hour
        price_current = nordpool_sensor.attributes.current_price
        prices_all = BatteryChargeFromGridFactor.get_sanitized_list(nordpool_sensor.attributes.today + nordpool_sensor.attributes.tomorrow)
        factor = BatteryChargeFromGridFactor.get_factor(
            price_current=price_current,
            prices_all=prices_all,
            hour_current=hour_current
        )
        self.set_state('sensor.battery_charge_from_grid_factor', state=factor)

    @staticmethod
    def get_factor(price_current, prices_all, hour_current):
        prices_future = prices_all[hour_current:hour_current + 12]
        price_average_future = BatteryChargeFromGridFactor.get_average(prices_future)
        price_average_factor = price_average_future / price_current
        factor = price_average_factor / config.THRESHOLD_FACTOR
        return round(factor, 3)

    @staticmethod
    def get_sanitized_list(lst):
        return list(filter(lambda x: type(x) == float, lst))

    @staticmethod
    def get_average(lst):
        return sum(lst) / len(lst)

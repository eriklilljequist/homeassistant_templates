import hassapi
from datetime import datetime
import pytz
from src.utilities import config


class BatteryChargeFromGridFactor(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.nordpool_price_change, 'sensor.nordpool_kwh_se3_sek_2_10_025', constrain_presence='everyone')

    def nordpool_price_change(self, entity, attribute, old, new, kwargs):
        self.execute()

    def execute(self):
        nordpool_sensor = self.entities.sensor.nordpool_kwh_se3_sek_2_10_025
        zone_se = pytz.timezone('Europe/Stockholm')
        hour_current = datetime.now(tz=zone_se).hour
        price_current = nordpool_sensor.attributes.current_price
        factor = BatteryChargeFromGridFactor.get_factor(
            price_current=price_current,
            prices_all=nordpool_sensor.attributes.today + nordpool_sensor.attributes.tomorrow,
            hour_current=hour_current
        )
        self.set_state('sensor.battery_charge_from_grid_factor', state=factor)

    @staticmethod
    def get_factor(price_current, prices_all, hour_current):
        period = 6
        prices_current = prices_all[hour_current:hour_current + period]
        prices_future = prices_all[hour_current + period:hour_current + period * 2]
        price_average_current = BatteryChargeFromGridFactor.get_average(prices_current)
        price_average_future = BatteryChargeFromGridFactor.get_average(prices_future)

        return round(BatteryChargeFromGridFactor.calculate_factor(
            price_current=price_current,
            price_average_current=price_average_current,
            price_average_future=price_average_future), 3)

    @staticmethod
    def calculate_factor(price_current, price_average_current, price_average_future):
        average_factor_future = price_average_future / price_current
        average_factor_current = price_average_current / price_current
        return (average_factor_future + average_factor_current) / 2 / config.THRESHOLD_FACTOR

    @staticmethod
    def get_average(lst):
        return sum(lst) / len(lst)

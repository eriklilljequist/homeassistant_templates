import hassapi
from datetime import datetime


class BatteryChargeFromGridFactor(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.nordpool_price_change, "sensor.nordpool_kwh_se3_sek_2_10_025", constrain_presence="everyone")
        self.run_every(self.from_schedule, datetime.now(), 60)

    def from_schedule(self, kwargs):
        self.execute()

    def nordpool_price_change(self, entity, attribute, old, new, kwargs):
        self.execute()

    def execute(self):
        nordpool_sensor = self.entities.sensor.nordpool_kwh_se3_sek_2_10_025
        hour_current = datetime.now().hour
        price_current = nordpool_sensor.attributes.current_price
        factor = BatteryChargeFromGridFactor.get_allow_factor(
            price_current=price_current,
            prices_all=nordpool_sensor.attributes.today + nordpool_sensor.attributes.tomorrow,
            hour_current=hour_current
        )
        self.log(f'Current hour is: {hour_current}')
        self.log(f'Current price is: {price_current}')
        self.log(f'Factor is: {factor}')

        self.set_state("sensor.battery_charge_from_grid_factor", state=factor)
        self.set_value("number.grid_charge_maximum_power", value=BatteryChargeFromGridFactor.get_max_grid_charging_power(factor))
        self.set_value("number.maximum_discharging_power", value=BatteryChargeFromGridFactor.get_max_discharging_power(factor))

    @staticmethod
    def get_max_grid_charging_power(factor):
        return round(min(int(1500 * factor), 3000), 3)

    @staticmethod
    def get_max_discharging_power(factor):
        return round(min(int(1500 / factor), 3000), 3)

    @staticmethod
    def get_allow_factor(price_current, prices_all, hour_current):
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
        threshold_factor = 1.8  # the bigger value the longer it will take until charge from grid reaches 1
        average_factor_future = price_average_future / price_current
        average_factor_current = price_average_current / price_current
        return average_factor_future * average_factor_current / threshold_factor

    @staticmethod
    def get_average(lst):
        return sum(lst) / len(lst)

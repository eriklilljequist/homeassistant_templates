import hassapi
import datetime


class AllowChargeFromGrid(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.nordpool_price_change, "sensor.nordpool_kwh_se3_sek_2_10_025", constrain_presence="everyone")
        self.nordpool_price_change()

    def nordpool_price_change(self, *_):
        nordpool_sensor = self.entities.sensor.nordpool_kwh_se3_sek_2_10_025
        factor = AllowChargeFromGrid.get_allow_factor(
            price_current=nordpool_sensor.attributes.current_price,
            prices_all=nordpool_sensor.attributes.today + nordpool_sensor.attributes.tomorrow,
            hour_current=datetime.datetime.now().hour
        )
        self.set_state("sensor.battery_allow_charge_from_grid_2", state=factor)
        self.set_value("number.grid_charge_maximum_power", value=AllowChargeFromGrid.get_max_grid_charging_power(factor))
        self.set_value("number.maximum_discharging_power", value=AllowChargeFromGrid.get_max_discharging_power(factor))

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
        price_average_current = AllowChargeFromGrid.get_average(prices_current)
        price_average_future = AllowChargeFromGrid.get_average(prices_future)

        return round(AllowChargeFromGrid.calculate_factor(
            price_current=price_current,
            price_average_current=price_average_current,
            price_average_future=price_average_future), 3)

    @staticmethod
    def calculate_factor(price_current, price_average_current, price_average_future):
        threshold_factor = 1.8  # the bigger value the longer it will take until charge fromgrid reaches 1
        average_factor_future = price_average_future / price_current
        average_factor_current = price_average_current / price_current
        return average_factor_future * average_factor_current / threshold_factor

    @staticmethod
    def get_average(lst):
        return sum(lst) / len(lst)

import hassapi
import datetime


class AllowChargeFromGrid(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.nordpool_price_change, "sensor.nordpool_kwh_se3_sek_2_10_025", constrain_presence="everyone")

    def nordpool_price_change(self, entity, attribute, old, new, kwargs):
        factor = AllowChargeFromGrid.get_allow_factor(
            current_price=entity.attributes.current_price,
            all_prices=entity.attributes.today + entity.attributes.tomorrow,
            current_hour=datetime.datetime.now().hour
        )
        self.set_state("sensor.battery_allow_charge_from_grid_2", state=factor)
        self.set_state("number.maximum_discharging_power", state=AllowChargeFromGrid.get_max_grid_charging_power(factor))

    @staticmethod
    def get_max_grid_charging_power(factor):
        return min(int(2000 * factor), 3000)

    @staticmethod
    def get_allow_factor(price_current, prices_all, current_hour):
        period = 6
        prices_current = prices_all[current_hour:current_hour + period]
        prices_future = prices_all[current_hour + period:current_hour + period * 2]
        price_average_current = AllowChargeFromGrid.get_average(prices_current)
        price_average_future = AllowChargeFromGrid.get_average(prices_future)

        return AllowChargeFromGrid.calculate_factor(
            price_current=price_current,
            price_average_current=price_average_current,
            price_average_future=price_average_future)

    @staticmethod
    def calculate_factor(price_current, price_average_current, price_average_future):
        threshold_factor = 1.8  # the bigger value the longer it will take until charge fromgrid reaches 1
        average_factor_future = price_average_future / price_current
        average_factor_current = price_average_current / price_current
        return average_factor_future * average_factor_current / threshold_factor

    @staticmethod
    def get_average(lst):
        return sum(lst) / len(lst)

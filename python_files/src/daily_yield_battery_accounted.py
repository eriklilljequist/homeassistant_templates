import hassapi
# from datetime import datetime


class DailyYieldBatteryAccounted(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.daily_yield_changed, "sensor.daily_yield", constrain_presence="everyone")
        # self.run_every(self.from_schedule, datetime.now(), 1 * 60)

    def from_schedule(self, kwargs):
        self.execute()

    def daily_yield_changed(self, entity, attribute, old, new, kwargs):
        self.execute()

    def execute(self):
        daily_yield = float(self.entities.sensor.daily_yield.state)
        battery_day_charge = float(self.entities.sensor.battery_day_charge.state)
        battery_day_discharge = float(self.entities.sensor.battery_day_discharge.state)
        daily_yield_battery_accounted = daily_yield + battery_day_charge - battery_day_discharge
        self.log(f'daily_yield is {daily_yield}')
        self.log(f'daily_yield_battery_accounted is {daily_yield_battery_accounted}')
        self.set_state(entity_id='sensor.daily_yield_battery_accounted', state=daily_yield_battery_accounted)

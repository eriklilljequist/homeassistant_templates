import hassapi


class BatteryDischargeFactor(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.charge_from_grid_factor_change, "sensor.battery_charge_from_grid_factor", constrain_presence="everyone")

    def charge_from_grid_factor_change(self, entity, attribute, old, new, kwargs):
        self.execute()

    def execute(self):
        battery_charge_from_grid_factor = float(self.entities.sensor.battery_charge_from_grid_factor.state)
        factor = BatteryDischargeFactor.get_factor(battery_charge_from_grid_factor)
        self.set_state('sensor.battery_discharge_factor', state=factor)

    @staticmethod
    def get_factor(battery_charge_from_grid_factor):
        return round(1 / battery_charge_from_grid_factor, 2)

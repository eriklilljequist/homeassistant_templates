import hassapi


class HouseConsumption(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.active_power_change, "sensor.active_power", constrain_presence="everyone")

    def active_power_change(self, *_):
        house_consumption = self.entities.sensor.active_power - self.entities.sensor.grid_active_power
        self.set_state("sensor.house_consumption_2", state=house_consumption)

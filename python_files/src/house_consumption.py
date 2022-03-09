import hassapi


class HouseConsumption(hassapi.Hass):
    def initialize(self):
        self.listen_state(self.active_power_change, "sensor.active_power", constrain_presence="everyone")

    def active_power_change(self, entity, attribute, old, new, kwargs):
        active_power = int(self.entities.sensor.active_power.state)
        grid_active_power = int(self.entities.sensor.grid_active_power.state)
        self.set_state("sensor.house_consumption_2", state=active_power - grid_active_power)

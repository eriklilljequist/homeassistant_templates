# import hassapi
# from datetime import datetime


# class ExportRatherThanChargeFactor(hassapi.Hass):
#     def initialize(self):
#         self.listen_state(self.nordpool_price_change, "sensor.nordpool_kwh_se3_sek_2_10_025", constrain_presence="everyone")
#         self.run_every(self.from_schedule, datetime.now(), 1 * 60)

#     def from_schedule(self, kwargs):
#         self.execute()

#     def nordpool_price_change(self, entity, attribute, old, new, kwargs):
#         self.execute()

#     def execute(self):
#         self.log('START')
#         daily_yield_battery_accounted = round(float(self.entities.sensor.daily_yield_battery_accounted.state))

#         # estimated_energy_current_hour = float(self.entities.sensor.energy_current_hour_2.state)
#         # estimated_energy_next_hour = float(self.entities.sensor.energy_next_hour_2.state)
#         estimated_energy_production_today = float(self.entities.sensor.energy_production_today_2.state)
#         # estimated_energy_production_tomorrow = float(self.entities.sensor.energy_production_tomorrow_2.state)
#         # estimated_power_production_now = float(self.entities.sensor.power_production_now_2.state)

#         # current_active_power = int(self.entities.sensor.active_power.state)

#         battery_capacity = 10
#         battery_soc = float(self.entities.sensor.battery_state_of_capacity.state)
#         # battery_grid_charge_cutoff_soc = int(self.entities.number.grid_charge_cutoff_soc.state)
#         battery_left_to_charge = battery_soc / battery_capacity

#         battery_charge_from_grid_factor = float(self.entities.sensor.battery_charge_from_grid_factor.state)

#         # Factors
#         # current_power_is_close_to_estimate = abs(estimated_power_production_now - current_active_power) < 0.3
#         price_is_high = battery_charge_from_grid_factor < 0.8
#         energy_still_to_be_produced = estimated_energy_production_today - daily_yield_battery_accounted

#         # self.log(f'Value of daily_yield_battery_accounted is {daily_yield_battery_accounted}')
#         # self.log(f'Value of estimated_energy_production_today is {estimated_energy_production_today}')
#         # self.log(f'Value of estimated_power_production_now is {estimated_power_production_now}')
#         # self.log(f'Value of current_active_power is {current_active_power}')
#         # self.log(f'Value of battery_soc is {battery_soc}')
#         # self.log(f'Value of battery_left_to_charge is {battery_left_to_charge}')
#         # self.log(f'Value of battery_charge_from_grid_factor is {battery_charge_from_grid_factor}')
#         # self.log(f'Value of price_is_high is {price_is_high}')
#         # self.log(f'Value of energy_still_to_be_produced is {energy_still_to_be_produced}')

#         if price_is_high and energy_still_to_be_produced > battery_left_to_charge * 1.5:
#             self.log('switching OFF charge_from_generation since price is high and we will produce more energy!')
#             self.set_state('input_boolean.charge_from_generation', state=False)
#         else:
#             self.log('switching ON charge_from_generation since price either low or we wont produce enough more in order to charge!')
#             self.set_state('self.entities.input_boolean.charge_from_generation', state=True)
#         self.log(f'Charge from generation switch is {self.entities.input_boolean.charge_from_generation.state}')
#         self.log('END')

#     @staticmethod
#     def get_factor(battery_charge_from_grid_factor, energy_still_to_be_produced, battery_left_to_charge):
#         toggler = ExportRatherThanChargeFactor.get_toggler(battery_charge_from_grid_factor)
#         return round(toggler * (energy_still_to_be_produced / battery_left_to_charge) * 0.6, 2)

#     @staticmethod
#     def get_toggler(battery_charge_from_grid_factor):
#         return min(
#             round(1 / battery_charge_from_grid_factor, 2),
#             2
#         )

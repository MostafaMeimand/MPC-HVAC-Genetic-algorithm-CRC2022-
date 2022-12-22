from pyenergyplus.plugin import EnergyPlusPlugin
import csv

class HeatingSetPoint(EnergyPlusPlugin):

    def actuate(self, state, x):
        self.api.exchange.set_actuator_value(state, self.data['actuator_heating'], x)

    def on_begin_zone_timestep_before_set_current_weather(self, state) -> int:
        if self.api.exchange.warmup_flag(state):
            return 0
        self.api.exchange.tomorrow_weather_outdoor_dry_bulb_at_time(state, 3, 2)
        return 0

    def on_begin_timestep_before_predictor(self, state) -> int:
        if 'handles_done' not in self.data:
            self.data['actuator_heating'] = self.api.exchange.get_actuator_handle(
                state, "Schedule:Constant", "Schedule Value", "HTGSETP_SCH"
            )
            if self.data['actuator_heating'] == -1:
                self.api.runtime.issue_severe(state, "Could not get handle to heating setpoint schedule")
                return 1
            self.data['handles_done'] = True

        hour = self.api.exchange.hour(state)
        day_of_week = self.api.exchange.day_of_week(state)
        day_of_year = self.api.exchange.day_of_year(state)
        holiday = self.api.exchange.holiday_index(state)
        self.actuate(state, 15.6)
        return 0


class CoolingSetPoint(EnergyPlusPlugin):

    def actuate(self, state, x):
        self.api.exchange.set_actuator_value(state, self.data['actuator_cooling'], x)

    def on_begin_timestep_before_predictor(self, state) -> int:
        if 'handles_done' not in self.data:
            self.data['actuator_cooling'] = self.api.exchange.get_actuator_handle(
                state, "Schedule:Constant", "Schedule Value", "CLGSETP_SCH"
            )
            if self.data['actuator_cooling'] == -1:
                self.api.runtime.issue_severe(state, "Could not get handle to cooling setpoint schedule")
                return 1
            self.data['handles_done'] = True
        hour = self.api.exchange.hour(state)
        day_of_week = self.api.exchange.day_of_week(state)
        day_of_month = self.api.exchange.day_of_month(state)
        holiday = self.api.exchange.holiday_index(state)
        month = self.api.exchange.month(state)
        minutes = self.api.exchange.minutes(state)


        if 11 <= hour < 22 :
            self.actuate(state, 25)
        else:
            self.actuate(state, 24)
        return 0

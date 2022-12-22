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


        # Price = [18.58,18.82,18.86,18.83,18.85,18.83,18.84,18.88,18.89,18.92,18.9,18.83,18.53,18.51,18.49,18.16,18.56,18.7,18.89,18.85,19.32,19.81,20.02,20.2,20.41,20.54,21.06,22.08,23.13,23.48,23.17,
        # 21.87,21.13,19.75,18.8,18.13,18.26,18.02,17.84,17.87,17.74,17.47,16.92,16.57,16.33,16.25,15.66,15.1,14.73,14.34,13.85,13.19,12.97,12.61,12.04,1.32,8.36,10.9,0.91,0.01,1.71,1.44,8.14,11.64,11.93,
        # 12.4,12.95,13.89,15.49,16.3,16.34,16.64,16.58,16.51,16.21,15.9,15.56,14.93,14.34,14.45,14.3,14.29,14.53,14.64,14.7,15.34,15.29,15.38,14.58,15.3,15.38,15.56,15.04,14.13,13.79,13.48]

        Price = [17,17,17,17,17,17,17,17,17,17,17,17,
17,17,17,17,
17,17,17,17,
17,17,17,17,
17,17,17,17,
17,17,17,17,
17,17,17,17,
17,17,17,17,
17,17,17,17,
17,17,19,19,
19,19,19,19,
19,19,19,19,
19,19,19,19,19,19,
19,19,19,19,
19,19,19,19,
19,19,19,19,
19,19,19,19,
19,19,19,19,
19,19,19,19,
19,19,19,19,
19,19,19,19,
19,19 ]

        # test this idea for a week!


        t = minutes + hour * 60
        t = int(t/15) # is a number between 1 to 96!

        # for writing a variable
        self.value = self.api.exchange.get_global_handle(state, "Variable")
        self.api.exchange.set_global_value(state, self.value, Price[t-1]) 

        if (Price[t-1] > 18):
                self.actuate(state, 23)
        else:
                self.actuate(state, 23)      
        return 0

        # if hour < 8:
        #     self.actuate(state, 23.89)
        # elif 8 <= hour < 17 :
        #     self.actuate(state, 25.56)
        # elif 17 <= hour < 22 :
        #     self.actuate(state, 22.77)
        # elif hour >= 22:
        #     self.actuate(state, 23.88)
        # return 0
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import os

from tkinter import *
from tkinter import ttk

class FuzzyProject:
    def __init__(self):
        self.masterWindow = Tk()
        self.drink_volume_string = StringVar();
        self.room_temperature_string = StringVar();
        self.freezer_intensity_string = StringVar()
        self.result_string = StringVar()


        self.frame = Frame(self.masterWindow)
        self.frame.pack()
        self.drink_volume_label = ttk.Label(self.masterWindow, text="Please type drink volume in ml [100;3000]:")
        self.drink_volume_entry = ttk.Entry(self.masterWindow, textvariable=self.drink_volume_string)
        self.room_temperature_label = ttk.Label(self.masterWindow, text="Please type room temperature in °C [15;35]:")
        self.room_temperature_entry = ttk.Entry(self.masterWindow, textvariable=self.room_temperature_string)
        self.freezer_intensity_label = ttk.Label(self.masterWindow,
                                            text="Please type freezer inensity in % as decimal fraction [0.1;1.0]:")
        self.freezer_intensity_entry = ttk.Entry(self.masterWindow, textvariable=self.freezer_intensity_string)
        self.button = Button(self.masterWindow, text="done", command=self.validate_and_go)
        self.result_is_label = ttk.Label(self.masterWindow, textvariable=self.result_string)

        self.drink_volume_label.pack()
        self.drink_volume_entry.pack()
        self.room_temperature_label.pack()
        self.room_temperature_entry.pack()
        self.freezer_intensity_label.pack()
        self.freezer_intensity_entry.pack()
        self.result_is_label.pack()
        self.button.pack()


        # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        self.drink_volume = ctrl.Antecedent(np.arange(100, 3001, 1), 'drink_volume')  # objetosc napoju
        self.room_temperature = ctrl.Antecedent(np.arange(15, 36, 1),
                                           'outside_temperature')  # temperatura otoczenia, zakladam ze napoj jest na poczatku w temperaturze otoczenia
        self.freezer_intensity = ctrl.Antecedent(np.arange(0.1, 1.01, 0.01),
                                            'freezer_intensity')  # minimalna intensywnosc chlodzenia dla potrzebnej temperatury to 10%
        self.cooling_time = ctrl.Consequent(np.arange(15, 360, 1), 'cooling_time')  # czas chlodzenia w minutach

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        # drink_volume.automf(5)
        self.drink_volume['tiny'] = fuzz.trimf(self.drink_volume.universe, [100, 100, 500])
        self.drink_volume['small'] = fuzz.trimf(self.drink_volume.universe, [100, 500, 1250])
        self.drink_volume['average'] = fuzz.trimf(self.drink_volume.universe, [500, 1250, 2250])
        self.drink_volume['large'] = fuzz.trimf(self.drink_volume.universe, [1250, 2250, 3000])
        self.drink_volume['enormous'] = fuzz.trimf(self.drink_volume.universe, [2250, 3000, 3000])

        # outside_temperature.automf(5)
        self.room_temperature['freezing'] = fuzz.trimf(self.room_temperature.universe, [15, 15, 18])
        self.room_temperature['cold'] = fuzz.trimf(self.room_temperature.universe, [15, 18, 23])
        self.room_temperature['convenient'] = fuzz.trimf(self.room_temperature.universe, [18, 23, 29])
        self.room_temperature['hot'] = fuzz.trimf(self.room_temperature.universe, [23, 29, 35])
        self.room_temperature['sweltering'] = fuzz.trimf(self.room_temperature.universe, [29, 35, 35])
        self.freezer_intensity.automf(5)

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        self.cooling_time['brief'] = fuzz.trimf(self.cooling_time.universe, [15, 15, 60])
        self.cooling_time['short'] = fuzz.trimf(self.cooling_time.universe, [15, 60, 120])
        self.cooling_time['average'] = fuzz.trimf(self.cooling_time.universe, [60, 120, 180])
        self.cooling_time['long'] = fuzz.trimf(self.cooling_time.universe, [120, 180, 360])
        self.cooling_time['very long'] = fuzz.trimf(self.cooling_time.universe, [180, 360, 360])

        # You can see how these look with .view()
        self.room_temperature.view()
        self.drink_volume.view()
        self.freezer_intensity.view()
        self.cooling_time.view()

        self.rule1 = ctrl.Rule(
            self.drink_volume['tiny'] & self.room_temperature['freezing'] & self.freezer_intensity['good'],
            self.cooling_time['brief'])
        self.rule2 = ctrl.Rule(
            self.drink_volume['small'] & self.room_temperature['cold'] & self.freezer_intensity['decent'],
            self.cooling_time['short'])
        self.rule3 = ctrl.Rule(
            self.drink_volume['average'] & self.room_temperature['convenient'] & self.freezer_intensity['average'],
            self.cooling_time['average'])
        self.rule4 = ctrl.Rule(
            self.drink_volume['large'] & self.room_temperature['hot'] & self.freezer_intensity['mediocre'],
            self.cooling_time['long'])
        self.rule5 = ctrl.Rule(
            self.drink_volume['enormous'] & self.room_temperature['sweltering'] & self.freezer_intensity['poor'],
            self.cooling_time['very long'])

        self.rule6 = ctrl.Rule(
            self.drink_volume['tiny'] | self.room_temperature['freezing'] | self.freezer_intensity['good'],
            self.cooling_time['brief'])
        self.rule7 = ctrl.Rule(
            self.drink_volume['small'] | self.room_temperature['cold'] | self.freezer_intensity['decent'],
            self.cooling_time['short'])
        self.rule8 = ctrl.Rule(
            self.drink_volume['average'] | self.room_temperature['convenient'] & self.freezer_intensity['average'],
            self.cooling_time['average'])
        self.rule9 = ctrl.Rule(
            self.drink_volume['large'] | self.room_temperature['hot'] | self.freezer_intensity['mediocre'],
            self.cooling_time['long'])
        self.rule10 = ctrl.Rule(
            self.drink_volume['enormous'] | self.room_temperature['sweltering'] | self.freezer_intensity['poor'],
            self.cooling_time['very long'])

        self.rule11 = ctrl.Rule(self.drink_volume['tiny'] & self.freezer_intensity['poor'],
                                self.cooling_time['average'])
        self.rule12 = ctrl.Rule(self.drink_volume['tiny'] & self.freezer_intensity['mediocre'],
                                self.cooling_time['short'])
        self.rule13 = ctrl.Rule(self.drink_volume['tiny'] & self.freezer_intensity['average'],
                                self.cooling_time['short'])
        self.rule14 = ctrl.Rule(self.drink_volume['tiny'] & self.freezer_intensity['decent'],
                                self.cooling_time['brief'])
        self.rule15 = ctrl.Rule(self.drink_volume['tiny'] & self.freezer_intensity['good'],
                                self.cooling_time['brief'])
        self.rule16 = ctrl.Rule(self.drink_volume['small'] & self.freezer_intensity['poor'],
                                self.cooling_time['average'])
        self.rule17 = ctrl.Rule(self.drink_volume['small'] & self.freezer_intensity['mediocre'],
                                self.cooling_time['average'])
        self.rule18 = ctrl.Rule(self.drink_volume['small'] & self.freezer_intensity['average'],
                                self.cooling_time['short'])
        self.rule19 = ctrl.Rule(self.drink_volume['small'] & self.freezer_intensity['decent'],
                                self.cooling_time['short'])
        self.rule20 = ctrl.Rule(self.drink_volume['small'] & self.freezer_intensity['good'],
                                self.cooling_time['brief'])
        self.rule21 = ctrl.Rule(self.drink_volume['average'] & self.freezer_intensity['poor'],
                                self.cooling_time['long'])
        self.rule22 = ctrl.Rule(self.drink_volume['average'] & self.freezer_intensity['mediocre'],
                                self.cooling_time['average'])
        self.rule23 = ctrl.Rule(self.drink_volume['average'] & self.freezer_intensity['average'],
                                self.cooling_time['average'])
        self.rule24 = ctrl.Rule(self.drink_volume['average'] & self.freezer_intensity['decent'],
                                self.cooling_time['short'])
        self.rule25 = ctrl.Rule(self.drink_volume['average'] & self.freezer_intensity['good'],
                                self.cooling_time['short'])
        self.rule26 = ctrl.Rule(self.drink_volume['large'] & self.freezer_intensity['poor'],
                                self.cooling_time['long'])
        self.rule27 = ctrl.Rule(self.drink_volume['large'] & self.freezer_intensity['mediocre'],
                                self.cooling_time['long'])
        self.rule28 = ctrl.Rule(self.drink_volume['large'] & self.freezer_intensity['average'],
                                self.cooling_time['average'])
        self.rule29 = ctrl.Rule(self.drink_volume['large'] & self.freezer_intensity['decent'],
                                self.cooling_time['average'])
        self.rule30 = ctrl.Rule(self.drink_volume['large'] & self.freezer_intensity['good'],
                                self.cooling_time['short'])
        self.rule31 = ctrl.Rule(self.drink_volume['enormous'] & self.freezer_intensity['poor'],
                                self.cooling_time['very long'])
        self.rule32 = ctrl.Rule(self.drink_volume['enormous'] & self.freezer_intensity['mediocre'],
                                self.cooling_time['long'])
        self.rule33 = ctrl.Rule(self.drink_volume['enormous'] & self.freezer_intensity['average'],
                                self.cooling_time['long'])
        self.rule34 = ctrl.Rule(self.drink_volume['enormous'] & self.freezer_intensity['decent'],
                                self.cooling_time['average'])
        self.rule35 = ctrl.Rule(self.drink_volume['enormous'] & self.freezer_intensity['good'],
                                self.cooling_time['average'])

        self.rule36 = ctrl.Rule(self.drink_volume['tiny'] & self.room_temperature['freezing'],
                                self.cooling_time['brief'])
        self.rule37 = ctrl.Rule(self.drink_volume['tiny'] & self.room_temperature['cold'],
                                self.cooling_time['brief'])
        self.rule38 = ctrl.Rule(self.drink_volume['tiny'] & self.room_temperature['convenient'],
                                self.cooling_time['brief'])
        self.rule39 = ctrl.Rule(self.drink_volume['tiny'] & self.room_temperature['hot'],
                                self.cooling_time['short'])
        self.rule40 = ctrl.Rule(self.drink_volume['tiny'] & self.room_temperature['sweltering'],
                                self.cooling_time['short'])
        self.rule41 = ctrl.Rule(self.drink_volume['small'] & self.room_temperature['freezing'],
                                self.cooling_time['brief'])
        self.rule42 = ctrl.Rule(self.drink_volume['small'] & self.room_temperature['cold'],
                                self.cooling_time['brief'])
        self.rule43 = ctrl.Rule(self.drink_volume['small'] & self.room_temperature['convenient'],
                                self.cooling_time['short'])
        self.rule44 = ctrl.Rule(self.drink_volume['small'] & self.room_temperature['hot'],
                                self.cooling_time['short'])
        self.rule45 = ctrl.Rule(self.drink_volume['small'] & self.room_temperature['sweltering'],
                                self.cooling_time['short'])
        self.rule46 = ctrl.Rule(self.drink_volume['average'] & self.room_temperature['freezing'],
                                self.cooling_time['short'])
        self.rule47 = ctrl.Rule(self.drink_volume['average'] & self.room_temperature['cold'],
                                self.cooling_time['average'])
        self.rule48 = ctrl.Rule(self.drink_volume['average'] & self.room_temperature['convenient'],
                                self.cooling_time['average'])
        self.rule49 = ctrl.Rule(self.drink_volume['average'] & self.room_temperature['hot'],
                                self.cooling_time['long'])
        self.rule50 = ctrl.Rule(self.drink_volume['average'] & self.room_temperature['sweltering'],
                                self.cooling_time['very long'])
        self.rule51 = ctrl.Rule(self.drink_volume['large'] & self.room_temperature['freezing'],
                                self.cooling_time['average'])
        self.rule52 = ctrl.Rule(self.drink_volume['large'] & self.room_temperature['cold'],
                                self.cooling_time['long'])
        self.rule53 = ctrl.Rule(self.drink_volume['large'] & self.room_temperature['convenient'],
                                self.cooling_time['long'])
        self.rule54 = ctrl.Rule(self.drink_volume['large'] & self.room_temperature['hot'],
                                self.cooling_time['very long'])
        self.rule55 = ctrl.Rule(self.drink_volume['large'] & self.room_temperature['sweltering'],
                                self.cooling_time['very long'])
        self.rule56 = ctrl.Rule(self.drink_volume['enormous'] & self.room_temperature['freezing'],
                                self.cooling_time['long'])
        self.rule57 = ctrl.Rule(self.drink_volume['enormous'] & self.room_temperature['cold'],
                                self.cooling_time['long'])
        self.rule58 = ctrl.Rule(self.drink_volume['enormous'] & self.room_temperature['convenient'],
                                self.cooling_time['very long'])
        self.rule59 = ctrl.Rule(self.drink_volume['enormous'] & self.room_temperature['hot'],
                                self.cooling_time['very long'])
        self.rule60 = ctrl.Rule(self.drink_volume['enormous'] & self.room_temperature['sweltering'],
                                self.cooling_time['very long'])

        self.time_ctrl = ctrl.ControlSystem(
            [self.rule1, self.rule2, self.rule3, self.rule4, self.rule5, self.rule6, self.rule7, self.rule8, self.rule9,
             self.rule10, self.rule11, self.rule12,
             self.rule13, self.rule14, self.rule15, self.rule16, self.rule17, self.rule18, self.rule19, self.rule20,
             self.rule21, self.rule22, self.rule23, self.rule24,
             self.rule25, self.rule26, self.rule27, self.rule28, self.rule29, self.rule30, self.rule31, self.rule32,
             self.rule33, self.rule34, self.rule35, self.rule36,
             self.rule37, self.rule38, self.rule39, self.rule40, self.rule41, self.rule42, self.rule43, self.rule44,
             self.rule45, self.rule46, self.rule47, self.rule48,
             self.rule49, self.rule50, self.rule51, self.rule52, self.rule53, self.rule54, self.rule55, self.rule56,
             self.rule57, self.rule58, self.rule59, self.rule60])

        self.time = ctrl.ControlSystemSimulation(self.time_ctrl)

        self.masterWindow.mainloop()

        # cooling_time.view(sim=time)

        # os.system("pause")

    def getInputAndcheckIfValueInRange(min, max, input_name):
        input_ok = False
        while input_ok == False:
            print("Please insert " + str(input_name) + " value between: [" + str(min) + "," + str(max) + "]")
            value = input()
            try:
                tmp = float(value)
                if (tmp >= min) and (tmp <= max):
                    input_ok = True
                    return tmp
                    break
                else:
                    print("The given value is out of range")
            except ValueError:
                print("The given value is not a number")

    def validate_input(self, min, max, input):
        try:
            tmp = float(input)
            if (tmp >= min) and (tmp <= max):
                return True
            else:
                False
        except ValueError:
            False

    def validate_and_go(self):
        if self.validate_input(100,3000,self.drink_volume_string.get()):
            pass
        else:
            self.result_string.set("Drink volume value is incorrect")
            return
        if self.validate_input(15,35,self.room_temperature_string.get()):
            pass
        else:
            self.result_string.set("Room temperature value is incorrect")
            return
        if self.validate_input(0.1,1.0, self.freezer_intensity_string.get()):
            pass
        else:
            self.result_string.set("Freezer intensity value is incorrect")
            return
        self.run_fuzzy()



    # Chlodzenie napojow fuzzy w lodowce

    # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
    # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
    # time.input['drink_volume'] = getInputAndcheckIfValueInRange(100, 3000, "drink volume")
    # time.input['outside_temperature'] = getInputAndcheckIfValueInRange(15, 36, "outside temperature")
    # time.input['freezer_intensity'] = getInputAndcheckIfValueInRange(0.1, 1.0, "freezer intensity")

    # Crunch the numbers
    # time.compute()

    # print(time.output['cooling_time'])

    def run_fuzzy(self):
        self.time.input['drink_volume'] = float(self.drink_volume_string.get())
        self.time.input['outside_temperature'] = float(self.room_temperature_string.get())
        self.time.input['freezer_intensity'] = float(self.freezer_intensity_string.get())
        self.time.compute()
        self.result_string.set("Expected cooling time is: "+str(self.time.output['cooling_time']) + "minutes")




fuzzy_project = FuzzyProject()
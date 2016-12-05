import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import os

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

# Chlodzenie napojow fuzzy w lodowce

# masterWindow = t


# New Antecedent/Consequent objects hold universe variables and membership
# functions
drink_volume = ctrl.Antecedent(np.arange(100, 3001, 1), 'drink_volume') # objetosc napoju
room_temperature = ctrl.Antecedent(np.arange(15, 36, 1), 'outside_temperature') # temperatura otoczenia, zakladam ze napoj jest na poczatku w temperaturze otoczenia
freezer_intensity = ctrl.Antecedent(np.arange(0.1, 1.01, 0.01), 'freezer_intensity') # minimalna intensywnosc chlodzenia dla potrzebnej temperatury to 10%
cooling_time = ctrl.Consequent(np.arange(15, 360, 1), 'cooling_time') # czas chlodzenia w minutach

# Auto-membership function population is possible with .automf(3, 5, or 7)
# drink_volume.automf(5)
drink_volume['tiny'] = fuzz.trimf(drink_volume.universe, [100, 100, 500])
drink_volume['small'] = fuzz.trimf(drink_volume.universe, [100, 500, 1250])
drink_volume['average'] = fuzz.trimf(drink_volume.universe, [500, 1250, 2250])
drink_volume['large'] = fuzz.trimf(drink_volume.universe, [1250, 2250, 3000])
drink_volume['enormous'] = fuzz.trimf(drink_volume.universe, [2250, 3000, 3000])

# outside_temperature.automf(5)
room_temperature['freezing'] = fuzz.trimf(room_temperature.universe, [15, 15, 18])
room_temperature['cold'] = fuzz.trimf(room_temperature.universe, [15, 18, 23])
room_temperature['convenient'] = fuzz.trimf(room_temperature.universe, [18, 23, 29])
room_temperature['hot'] = fuzz.trimf(room_temperature.universe, [23, 29, 35])
room_temperature['sweltering'] = fuzz.trimf(room_temperature.universe, [29, 35, 35])
freezer_intensity.automf(5)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
cooling_time['brief'] = fuzz.trimf(cooling_time.universe, [15, 15, 60])
cooling_time['short'] = fuzz.trimf(cooling_time.universe, [15, 60, 120])
cooling_time['average'] = fuzz.trimf(cooling_time.universe, [60, 120, 180])
cooling_time['long'] = fuzz.trimf(cooling_time.universe, [120, 180, 360])
cooling_time['very long'] = fuzz.trimf(cooling_time.universe, [180, 360, 360])


# You can see how these look with .view()
room_temperature.view()
drink_volume.view()
freezer_intensity.view()
cooling_time.view()

rule1 = ctrl.Rule(drink_volume['tiny'] & room_temperature['freezing'] & freezer_intensity['good'], cooling_time['brief'])
rule2 = ctrl.Rule(drink_volume['small'] & room_temperature['cold'] & freezer_intensity['decent'], cooling_time['short'])
rule3 = ctrl.Rule(drink_volume['average'] & room_temperature['convenient'] & freezer_intensity['average'], cooling_time['average'])
rule4 = ctrl.Rule(drink_volume['large'] & room_temperature['hot'] & freezer_intensity['mediocre'], cooling_time['long'])
rule5 = ctrl.Rule(drink_volume['enormous'] & room_temperature['sweltering'] & freezer_intensity['poor'], cooling_time['very long'])

rule6 = ctrl.Rule(drink_volume['tiny'] | room_temperature['freezing'] | freezer_intensity['good'], cooling_time['brief'])
rule7 = ctrl.Rule(drink_volume['small'] | room_temperature['cold'] | freezer_intensity['decent'], cooling_time['short'])
rule8 = ctrl.Rule(drink_volume['average'] | room_temperature['convenient'] & freezer_intensity['average'], cooling_time['average'])
rule9 = ctrl.Rule(drink_volume['large'] | room_temperature['hot'] | freezer_intensity['mediocre'], cooling_time['long'])
rule10 = ctrl.Rule(drink_volume['enormous'] | room_temperature['sweltering'] | freezer_intensity['poor'], cooling_time['very long'])

rule11 = ctrl.Rule(drink_volume['tiny'] & freezer_intensity['poor'], cooling_time['average'])
rule12 = ctrl.Rule(drink_volume['tiny'] & freezer_intensity['mediocre'], cooling_time['short'])
rule13 = ctrl.Rule(drink_volume['tiny'] & freezer_intensity['average'], cooling_time['short'])
rule14 = ctrl.Rule(drink_volume['tiny'] & freezer_intensity['decent'], cooling_time['brief'])
rule15 = ctrl.Rule(drink_volume['tiny'] & freezer_intensity['good'], cooling_time['brief'])
rule16 = ctrl.Rule(drink_volume['small'] & freezer_intensity['poor'], cooling_time['average'])
rule17 = ctrl.Rule(drink_volume['small'] & freezer_intensity['mediocre'], cooling_time['average'])
rule18 = ctrl.Rule(drink_volume['small'] & freezer_intensity['average'], cooling_time['short'])
rule19 = ctrl.Rule(drink_volume['small'] & freezer_intensity['decent'], cooling_time['short'])
rule20 = ctrl.Rule(drink_volume['small'] & freezer_intensity['good'], cooling_time['brief'])
rule21 = ctrl.Rule(drink_volume['average'] & freezer_intensity['poor'], cooling_time['long'])
rule22 = ctrl.Rule(drink_volume['average'] & freezer_intensity['mediocre'], cooling_time['average'])
rule23 = ctrl.Rule(drink_volume['average'] & freezer_intensity['average'], cooling_time['average'])
rule24 = ctrl.Rule(drink_volume['average'] & freezer_intensity['decent'], cooling_time['short'])
rule25 = ctrl.Rule(drink_volume['average'] & freezer_intensity['good'], cooling_time['short'])
rule26 = ctrl.Rule(drink_volume['large'] & freezer_intensity['poor'], cooling_time['long'])
rule27 = ctrl.Rule(drink_volume['large'] & freezer_intensity['mediocre'], cooling_time['long'])
rule28 = ctrl.Rule(drink_volume['large'] & freezer_intensity['average'], cooling_time['average'])
rule29 = ctrl.Rule(drink_volume['large'] & freezer_intensity['decent'], cooling_time['average'])
rule30 = ctrl.Rule(drink_volume['large'] & freezer_intensity['good'], cooling_time['short'])
rule31 = ctrl.Rule(drink_volume['enormous'] & freezer_intensity['poor'], cooling_time['very long'])
rule32 = ctrl.Rule(drink_volume['enormous'] & freezer_intensity['mediocre'], cooling_time['long'])
rule33 = ctrl.Rule(drink_volume['enormous'] & freezer_intensity['average'], cooling_time['long'])
rule34 = ctrl.Rule(drink_volume['enormous'] & freezer_intensity['decent'], cooling_time['average'])
rule35 = ctrl.Rule(drink_volume['enormous'] & freezer_intensity['good'], cooling_time['average'])

rule36 = ctrl.Rule(drink_volume['tiny'] & room_temperature['freezing'], cooling_time['brief'])
rule37 = ctrl.Rule(drink_volume['tiny'] & room_temperature['cold'], cooling_time['brief'])
rule38 = ctrl.Rule(drink_volume['tiny'] & room_temperature['convenient'], cooling_time['brief'])
rule39 = ctrl.Rule(drink_volume['tiny'] & room_temperature['hot'], cooling_time['short'])
rule40 = ctrl.Rule(drink_volume['tiny'] & room_temperature['sweltering'], cooling_time['short'])
rule41 = ctrl.Rule(drink_volume['small'] & room_temperature['freezing'], cooling_time['brief'])
rule42 = ctrl.Rule(drink_volume['small'] & room_temperature['cold'], cooling_time['brief'])
rule43 = ctrl.Rule(drink_volume['small'] & room_temperature['convenient'], cooling_time['short'])
rule44 = ctrl.Rule(drink_volume['small'] & room_temperature['hot'], cooling_time['short'])
rule45 = ctrl.Rule(drink_volume['small'] & room_temperature['sweltering'], cooling_time['short'])
rule46 = ctrl.Rule(drink_volume['average'] & room_temperature['freezing'], cooling_time['short'])
rule47 = ctrl.Rule(drink_volume['average'] & room_temperature['cold'], cooling_time['average'])
rule48 = ctrl.Rule(drink_volume['average'] & room_temperature['convenient'], cooling_time['average'])
rule49 = ctrl.Rule(drink_volume['average'] & room_temperature['hot'], cooling_time['long'])
rule50 = ctrl.Rule(drink_volume['average'] & room_temperature['sweltering'], cooling_time['very long'])
rule51 = ctrl.Rule(drink_volume['large'] & room_temperature['freezing'], cooling_time['average'])
rule52 = ctrl.Rule(drink_volume['large'] & room_temperature['cold'], cooling_time['long'])
rule53 = ctrl.Rule(drink_volume['large'] & room_temperature['convenient'], cooling_time['long'])
rule54 = ctrl.Rule(drink_volume['large'] & room_temperature['hot'], cooling_time['very long'])
rule55 = ctrl.Rule(drink_volume['large'] & room_temperature['sweltering'], cooling_time['very long'])
rule56 = ctrl.Rule(drink_volume['enormous'] & room_temperature['freezing'], cooling_time['long'])
rule57 = ctrl.Rule(drink_volume['enormous'] & room_temperature['cold'], cooling_time['long'])
rule58 = ctrl.Rule(drink_volume['enormous'] & room_temperature['convenient'], cooling_time['very long'])
rule59 = ctrl.Rule(drink_volume['enormous'] & room_temperature['hot'], cooling_time['very long'])
rule60 = ctrl.Rule(drink_volume['enormous'] & room_temperature['sweltering'], cooling_time['very long'])

time_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule12, rule12,
                                rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24,
                                rule25, rule26, rule27, rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36,
                                rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48,
                                rule49, rule50, rule51, rule52, rule53, rule54, rule55, rule56, rule57, rule58, rule59, rule60])

time = ctrl.ControlSystemSimulation(time_ctrl)

# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
time.input['drink_volume'] = getInputAndcheckIfValueInRange(100, 3000, "drink volume")
time.input['outside_temperature'] = getInputAndcheckIfValueInRange(15, 36, "outside temperature")
time.input['freezer_intensity'] = getInputAndcheckIfValueInRange(0.1, 1.0, "freezer intensity")

# Crunch the numbers
time.compute()

print(time.output['cooling_time'])
cooling_time.view(sim=time)


os.system("pause")



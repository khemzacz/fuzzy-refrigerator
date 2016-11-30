import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import threading
import os
import time

def getInputAndcheckIfValueInRange(min, max, input_name):
    input_ok = False
    while input_ok == False:
        print("Please insert " + str(input_name) + " value between: [" + str(min) + "," + str(max) + "]")
        value = input()
        try:
            tmp = float(value)
            if (tmp > min) and (tmp < max):
                input_ok = True
                return tmp
                break
            else:
                print("The given value is out of range")
        except ValueError:
            print("The given value is not a number")

# Chlodzenie napojow fuzzy w lodowce

# New Antecedent/Consequent objects hold universe variables and membership
# functions
drink_volume = ctrl.Antecedent(np.arange(100, 3001, 1), 'drink_volume') # objetosc napoju
outside_temperature = ctrl.Antecedent(np.arange(15, 36, 1), 'outside_temperature') # temperatura otoczenia, zakladam ze napoj jest na poczatku w temperaturze otoczenia
freezer_intensity = ctrl.Antecedent(np.arange(0.1, 1.0, 0.01), 'freezer_intensity') # minimalna intensywnosc chlodzenia dla potrzebnej temperatury to 10%
cooling_time = ctrl.Consequent(np.arange(15, 360, 1), 'cooling_time') # czas chlodzenia w minutach

# Auto-membership function population is possible with .automf(3, 5, or 7)
drink_volume.automf(5)
outside_temperature.automf(5)
freezer_intensity.automf(5)


# Custom membership functions can be built interactively with a familiar,
# Pythonic API
cooling_time['very short'] = fuzz.trimf(cooling_time.universe, [15, 15, 60])
cooling_time['short'] = fuzz.trimf(cooling_time.universe, [15, 60, 120])
cooling_time['medium'] = fuzz.trimf(cooling_time.universe, [60, 120, 180])
cooling_time['long'] = fuzz.trimf(cooling_time.universe, [120, 180, 240])
cooling_time['very_long'] = fuzz.trimf(cooling_time.universe, [180, 360, 360])


# You can see how these look with .view()
outside_temperature['average'].view()
drink_volume.view()

freezer_intensity.view()

rule1 = ctrl.Rule(drink_volume['poor'] | outside_temperature['poor'] | freezer_intensity['good'], cooling_time['very short'])
rule2 = ctrl.Rule(drink_volume['mediocre'] | outside_temperature['mediocre'] | freezer_intensity['decent'], cooling_time['short'])
rule3 = ctrl.Rule(drink_volume['average'], cooling_time['medium'])
rule4 = ctrl.Rule(drink_volume['decent'] | outside_temperature['decent'] | freezer_intensity['mediocre'], cooling_time['long'])
rule5 = ctrl.Rule(drink_volume['good'] | outside_temperature['good'] | freezer_intensity['poor'], cooling_time['very_long'])

# rule1.view()

time_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])

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



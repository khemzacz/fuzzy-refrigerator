import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Generate universe variables
#   * Quality and service on subjective ranges [0, 10]
#   * Tip has a range of [0, 25] in units of percentage points
# Temperature inside the fridge is 2 celsius, minimum cooling time is 3 minutes, which should cool 3 liters of drink
# Restrictions: Required temperature can't be lower than starting temperature
x_in_temp = np.arange(2, 36, 1)
x_volume = np.arange(100, 3001, 1)
x_time = np.arange(5, 361, 1)

# Generate fuzzy membership functions
in_temp_very_low = fuzz.trapmf(x_in_temp, [2, 2, 5, 10])
in_temp_low = fuzz.trimf(x_in_temp, [5, 10, 16])
in_temp_med = fuzz.trimf(x_in_temp, [10, 16, 22])
in_temp_high = fuzz.trimf(x_in_temp, [16, 22, 30])
in_temp_very_high = fuzz.trapmf(x_in_temp, [22, 30, 36, 36])

volume_very_low = fuzz.trapmf(x_volume, [100, 100, 200, 600])
volume_low = fuzz.trimf(x_volume, [200, 600, 1000])
volume_med = fuzz.trimf(x_volume, [600, 1000, 1500])
volume_big = fuzz.trimf(x_volume, [1000, 1500, 2000])
volume_enormous = fuzz.trapmf(x_volume, [1500, 2000, 3000, 3000])

time_short = fuzz.trapmf(x_time, [5, 5, 60, 120])
time_med = fuzz.trimf(x_time, [60, 120, 180])
time_long = fuzz.trimf(x_time, [120, 180, 240])
time_very_long = fuzz.trapmf(x_time, [180, 240, 360, 360])

# Visualize these universes and membership functions
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(x_in_temp, in_temp_very_low, 'b', linewidth=1.5, label='Very cold')
ax0.plot(x_in_temp, in_temp_low, 'g', linewidth=1.5, label='Cold')
ax0.plot(x_in_temp, in_temp_med, 'y', linewidth=1.5, label='Medium')
ax0.plot(x_in_temp, in_temp_high, 'm', linewidth=1.5, label='"Hot"')
ax0.plot(x_in_temp, in_temp_very_high, 'r', linewidth=1.5, label='"Very Hot"')
ax0.set_title('Drink\'s temperature [°C]')
ax0.legend()

ax1.plot(x_volume, volume_very_low, 'b', linewidth=1.5, label='Very small')
ax1.plot(x_volume, volume_low, 'g', linewidth=1.5, label='Small')
ax1.plot(x_volume, volume_med, 'y', linewidth=1.5, label='Medium')
ax1.plot(x_volume, volume_big, 'm', linewidth=1.5, label='Large')
ax1.plot(x_volume, volume_enormous, 'r', linewidth=1.5, label='Very large')
ax1.set_title('Drink\'s volume [ml]')
ax1.legend()

ax2.plot(x_time, time_short, 'b', linewidth=1.5, label='Short')
ax2.plot(x_time, time_med, 'g', linewidth=1.5, label='Medium')
ax2.plot(x_time, time_long, 'y', linewidth=1.5, label='Long')
ax2.plot(x_time, time_very_long, 'r', linewidth=1.5, label='Very long')
ax2.set_title('Time needed to cool a drink [min]')
ax2.legend()

# Turn off top/right axes
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()

plt.show()

inp1_val = 0; inp2_val = 0;
val_ok = False
while val_ok == False:
    inp1_val = input("Please insert the temperature of inserted drink[between 2°C and 35°C]:")
    try:
        inp1_val = float(inp1_val)
        if (inp1_val < 2.0) or (inp1_val > 35.0):
            print("Value is incorrect. Temperature should vary between 2°C and 35°C")
        else:
            val_ok = True
    except ValueError:
        print("Value is incorrect. Temperature should vary between 2°C and 35°C[use number without \"35°C\"]")

val_ok = False

while val_ok == False:
    inp2_val = input("Please insert the volume of inserted drink[between 100ml and 3000ml]:")
    try:
        inp2_val = float(inp2_val)
        if (inp2_val < 100.0) or (inp2_val > 3000.0):
            print("Value is incorrect. Volume should vary between 100ml and 3000ml")
        else:
            val_ok = True
    except ValueError:
        print("Value is incorrect. Volume should vary between 100ml and 3000ml[use number without \"ml\"]")

val_ok = False

print("Input values are: "+str(inp1_val)+"°C for starting temperature and "+str(inp2_val)+"ml for drink volume")




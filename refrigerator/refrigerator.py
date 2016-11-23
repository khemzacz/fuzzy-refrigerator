import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


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

# We need the activation of our fuzzy membership functions at these values.
# The exact values 6.5 and 9.8 do not exist on our universes...
# This is what fuzz.interp_membership exists for!
in_temp_level_vlo = fuzz.interp_membership(x_in_temp, in_temp_very_low, inp1_val)
in_temp_level_lo = fuzz.interp_membership(x_in_temp, in_temp_low, inp1_val)
in_temp_level_med = fuzz.interp_membership(x_in_temp, in_temp_med, inp1_val)
in_temp_level_hi = fuzz.interp_membership(x_in_temp, in_temp_high, inp1_val)
in_temp_level_vhi = fuzz.interp_membership(x_in_temp, in_temp_very_high, inp1_val)

volume_level_vlo = fuzz.interp_membership(x_volume, volume_very_low, inp2_val)
volume_level_lo = fuzz.interp_membership(x_volume, volume_low, inp2_val)
volume_level_med = fuzz.interp_membership(x_volume, volume_med, inp2_val)
volume_level_hi = fuzz.interp_membership(x_volume, volume_big, inp2_val)
volume_level_vhi = fuzz.interp_membership(x_volume, volume_enormous, inp2_val)

# Now we take our rules and apply them. Rule 1 concerns bad food OR service.
# The OR operator means we take the maximum of these two.
rule1 = np.fmin(in_temp_level_vlo, volume_level_vlo)
rule2 = np.fmin(in_temp_level_vlo, volume_level_lo)
rule3 = np.fmin(in_temp_level_vlo, volume_level_med)
rule4 = np.fmin(in_temp_level_vlo, volume_level_hi)
rule5 = np.fmin(in_temp_level_vlo, volume_level_vhi)
rule6 = np.fmin(in_temp_level_lo, volume_level_vlo)
rule7 = np.fmin(in_temp_level_lo, volume_level_lo)
rule8 = np.fmin(in_temp_level_lo, volume_level_med)
rule9 = np.fmin(in_temp_level_lo, volume_level_hi)
rule10 = np.fmin(in_temp_level_lo, volume_level_vhi)
rule11 = np.fmin(in_temp_level_med, volume_level_vlo)
rule12 = np.fmin(in_temp_level_med, volume_level_lo)
rule13 = np.fmin(in_temp_level_med, volume_level_med)
rule14 = np.fmin(in_temp_level_med, volume_level_hi)
rule15 = np.fmin(in_temp_level_med, volume_level_vhi)
rule16 = np.fmin(in_temp_level_hi, volume_level_vlo)
rule17 = np.fmin(in_temp_level_hi, volume_level_lo)
rule18 = np.fmin(in_temp_level_hi, volume_level_med)
rule19 = np.fmin(in_temp_level_hi, volume_level_hi)
rule20 = np.fmin(in_temp_level_hi, volume_level_vhi)
rule21 = np.fmin(in_temp_level_vhi, volume_level_vlo)
rule22 = np.fmin(in_temp_level_vhi, volume_level_lo)
rule23 = np.fmin(in_temp_level_vhi, volume_level_med)
rule24 = np.fmin(in_temp_level_vhi, volume_level_hi)
rule25 = np.fmin(in_temp_level_vhi, volume_level_vhi)

# Now we apply this by clipping the top off the corresponding output
# membership function with `np.fmin`
w, h = 25, 2
time_activation = [[0 for x in range(h)] for y in range(w)]

time_activation[0][0] = np.fmin(rule1, time_short); time_activation[0][1] = time_short
time_activation[1][0] = np.fmin(rule2, time_short); time_activation[1][1] = time_short
time_activation[2][0] = np.fmin(rule3, time_short); time_activation[2][1] = time_short
time_activation[3][0] = np.fmin(rule4, time_med); time_activation[3][1] = time_med
time_activation[4][0] = np.fmin(rule5, time_med); time_activation[4][1] = time_med
time_activation[5][0] = np.fmin(rule6, time_short); time_activation[5][1] = time_short
time_activation[6][0] = np.fmin(rule7, time_short); time_activation[6][1] = time_short
time_activation[7][0] = np.fmin(rule8, time_med); time_activation[7][1] = time_med
time_activation[8][0] = np.fmin(rule9, time_med); time_activation[8][1] = time_med
time_activation[9][0] = np.fmin(rule10, time_long); time_activation[9][1] = time_long
time_activation[10][0] = np.fmin(rule11, time_short); time_activation[10][1] = time_short
time_activation[11][0] = np.fmin(rule12, time_med); time_activation[11][1] = time_med
time_activation[12][0] = np.fmin(rule13, time_med); time_activation[12][1] = time_med
time_activation[13][0] = np.fmin(rule14, time_long); time_activation[13][1] = time_long
time_activation[14][0] = np.fmin(rule15, time_long); time_activation[14][1] = time_long
time_activation[15][0] = np.fmin(rule16, time_med); time_activation[15][1] = time_med
time_activation[16][0] = np.fmin(rule17, time_med); time_activation[16][1] = time_med
time_activation[17][0] = np.fmin(rule18, time_long); time_activation[17][1] = time_long
time_activation[18][0] = np.fmin(rule19, time_long); time_activation[18][1] = time_long
time_activation[19][0] = np.fmin(rule20, time_very_long); time_activation[19][1] = time_very_long
time_activation[20][0] = np.fmin(rule21, time_med); time_activation[20][1] = time_med
time_activation[21][0] = np.fmin(rule22, time_long); time_activation[21][1] = time_long
time_activation[22][0] = np.fmin(rule23, time_long); time_activation[22][1] = time_long
time_activation[23][0] = np.fmin(rule24, time_very_long); time_activation[23][1] = time_very_long
time_activation[24][0] = np.fmin(rule25, time_very_long); time_activation[24][1] = time_very_long


time0 = np.zeros_like(x_time)

# Visualize this
fig, ax0 = plt.subplots(figsize=(8, 4))

color_stack = ['y', 'm', 'c', 'r', 'g', 'b', 'g', 'r', 'c', 'm', 'y']

i = 0
while i < 25:
    ax0.fill_between(x_time, time0, time_activation[i][0], facecolor='b', alpha=0.7)
    ax0.plot(x_time, time_activation[i][1], 'b', linewidth=0.5, linestyle='--', )
    i=i+1

#
# ax0.fill_between(x_time, time0, time_activation[1][0], facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_short, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_2, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_short, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_3, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_short, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_4, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_med, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_5, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_med, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_6, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_short, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_7, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_short, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_8, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_med, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_9, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_med, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_10, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_long, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_11, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_short, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_12, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_med, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_13, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_med, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_14, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_long, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_15, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_long, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_16, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_med, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_17, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_med, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_18, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_long, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_19, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_long, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_20, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_very_long, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_21, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_med, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_22, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_long, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_23, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_long, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_24, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_very_long, 'b', linewidth=0.5, linestyle='--', )
# ax0.fill_between(x_time, time0, time_activation_25, facecolor='b', alpha=0.7)
# ax0.plot(x_time, time_very_long, 'b', linewidth=0.5, linestyle='--', )



ax0.set_title('Output membership activity')

# Turn off top/right axes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()

plt.show()


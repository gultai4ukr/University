from matplotlib import pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


TEMPERATURE_MIN = 20
TEMPERATURE_MAX = 200
TEMPERATURE_OPTIMAL = 80

temperature = ctrl.Antecedent(
    np.arange(TEMPERATURE_MIN, TEMPERATURE_MAX + 1, 1),
    'temperature'
)
temperature['cold'] = fuzz.trimf(
    temperature.universe,
    [TEMPERATURE_MIN, TEMPERATURE_MIN, TEMPERATURE_OPTIMAL]
)
temperature['comfortable'] = fuzz.trimf(
    temperature.universe,
    [TEMPERATURE_MIN, TEMPERATURE_OPTIMAL, TEMPERATURE_MAX]
)
temperature['hot'] = fuzz.trimf(
    temperature.universe,
    [TEMPERATURE_OPTIMAL, TEMPERATURE_MAX, TEMPERATURE_MAX]
)
temperature.view()

wave_mode = ctrl.Consequent([0, 0.5, 1], 'wave_mode')
wave_mode['off'] = [1, 0, 0]
wave_mode['half_power'] = [0, 1, 0]
wave_mode['on'] = [0, 0, 1]
wave_mode.view()

rules = [
    ctrl.Rule(temperature['cold'], wave_mode['on']),
    ctrl.Rule(temperature['comfortable'], wave_mode['half_power']),
    ctrl.Rule(temperature['hot'], wave_mode['off'])
]
# rules[0].view()
# rules[1].view()
# rules[2].view()

sauna_controller = ctrl.ControlSystem(rules)
sauna_simulation = ctrl.ControlSystemSimulation(sauna_controller)
plt.show()

print("*"*10 + " Sauna simulation started... For finishing type 'f'. " + "*"*10)
while 1:
    t = input("Specify current temperature: ")
    if t == 'f':
        break
    sauna_simulation.input['temperature'] = float(t)
    sauna_simulation.compute()
    fuzzy_mode = sauna_simulation.output['wave_mode']
    print("\tFuzzy mode value - {}".format(fuzzy_mode))
    mode = [None, 0]
    for label, term in wave_mode.terms.items():
        ratio = term.membership_value[sauna_simulation]
        print("\tMode '{}' matched on {:.2f}%".format(label, ratio * 100))
        if ratio > mode[1]:
            mode = [label, ratio]
    print("\tSo, wave should work in mode - '{}'".format(mode[0]))
    wave_mode.view(sim=sauna_simulation)
    plt.show()

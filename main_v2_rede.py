from datetime import datetime, timedelta
from pyomo.environ import *
import pandas as pd
import json

############ EV and EVCS variables ################
with open('dataset/ev.json') as file:
    EV = json.load(file)

with open('dataset/evcs.json') as file:
    EVCS = json.load(file)
    
with open('dataset/scenarios.json') as file:
    SCENARIOS = json.load(file)

with open('dataset/cost.json') as file:
    COST = json.load(file)


DELTA = 60 # minutes
T_novo = []
t = datetime.strptime('00:00', "%H:%M")
while t < datetime.strptime('23:59', "%H:%M"):
    T_novo.append(t.strftime("%H:%M"))
    t += timedelta(minutes=DELTA)


data = {'set_of_time': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'], 
        'set_of_nodes': ['1', '2', '3', '4', '5'], 
        'set_of_lines': [['1', '2'], ['2', '3'], ['3', '4'], ['4', '5']], 
        'set_of_photovoltaic_systems': ['1'], 
        'set_of_energy_storage_systems': ['1'], 
        # 'set_of_electric_vehicles': ['1'], 
        'set_of_thermal_generator': ['1'], 
        'set_of_outage': [], 
        # 'set_of_scenarios': ['1', '2', '3', '4', '5', '6', '7', '8', '9'], 
        # 'coefficient_demand_scen': [1.0, 1.0, 1.0, 0.8, 0.8, 0.8, 0.6, 0.6, 0.6], 
        # 'coefficient_pv_scen': [1.0, 0.8, 0.6, 1.0, 0.8, 0.6, 1.0, 0.8, 0.6], 
        # 'probability_of_scen': [0.1111111111111111, 0.1111111111111111, 0.1111111111111111, 0.1111111111111111, 0.1111111111111111, 0.1111111111111111, 0.1111111111111111, 0.1111111111111111, 0.1111111111111111], 
        'set_of_scenarios': ['1'], 
        'probability_of_scen': [1.0], 
        'coefficient_demand_scen': [1.0], 
        'coefficient_pv_scen': [1.0], 
        
        'type_of_bus': [1, 0, 0, 2, 0,], 
        'resistance_raa': [0.4138, 0.4138, 0.4138, 0.4138],#, 0.4138], 0.4138], 
        'resistance_rbb': [0.4138, 0.4138, 0.4138, 0.4138],#, 0.4138], 0.4138], 
        'resistance_rcc': [0.4138, 0.4138, 0.4138, 0.4138],#, 0.4138], 0.4138], 
        'resistance_rab': [0.0523, 0.0523, 0.0523, 0.0523],#, 0.0523], 0.0523], 
        'resistance_rac': [0.0523, 0.0523, 0.0523, 0.0523],#, 0.0523], 0.0523], 
        'resistance_rbc': [0.0523, 0.0523, 0.0523, 0.0523],#, 0.0523], 0.0523], 
        'reactance_xaa':  [0.8258, 0.8258, 0.8258, 0.8258],#, 0.8258], 0.8258], 
        'reactance_xbb':  [0.8258, 0.8258, 0.8258, 0.8258],#, 0.8258], 0.8258], 
        'reactance_xcc':  [0.8258, 0.8258, 0.8258, 0.8258],#, 0.8258], 0.8258], 
        'reactance_xab':  [0.4765, 0.4765, 0.4765, 0.4765],#, 0.4765], 0.4765], 
        'reactance_xac':  [0.4765, 0.4765, 0.4765, 0.4765],#, 0.4765], 0.4765], 
        'reactance_xbc':  [0.4765, 0.4765, 0.4765, 0.4765],#, 0.4765], 0.4765], 
        'nominal_voltage': 11.9, 
        'maximum_current_of_lines': [999.0, 999.0, 999.0, 999.0],#, 999.0], 
        'maximum_power_PCC': [1000.0, 0, 0, 0, 0],#, 0, 0], 
        'variation_of_time': 1, 
        'cost_of_the_energy': [0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.167, 0.167, 0.254, 0.254, 0.254, 0.167, 0.167, 0.116, 0.116], 
        'cost_of_load_curtailment': [500.0, 500.0, 500.0, 500.0, 0],#, 500.0, 500.0], 
        'nominal_active_load_phase_a': [1, 1, 123.66666666666667, 1, 1],#, 1, 1], 
        'nominal_active_load_phase_b': [1, 1, 123.66666666666667, 1, 1],#, 1, 1], 
        'nominal_active_load_phase_c': [1, 1, 123.66666666666667, 1, 1],#, 1, 1], 
        'nominal_reactive_load_phase_a': [1, 1, 1.0, 1, 1],#, 1, 1], 
        'nominal_reactive_load_phase_b': [1, 1, 1.0, 1, 1],#, 1, 1], 
        'nominal_reactive_load_phase_c': [1, 1, 1.0, 1, 1],#, 1, 1], 
        'profile_active_load_phase_a': [[0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.34, 0.36, 0.36, 0.37, 0.36, 0.33, 0.37, 0.52, 0.69, 0.73, 0.81, 0.82, 0.85, 1.0, 0.94, 0.91, 0.75, 0.92, 0.96, 0.89, 0.77, 0.52, 0.39, 0.36], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]], 
        'profile_active_load_phase_b': [[0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.34, 0.36, 0.36, 0.37, 0.36, 0.33, 0.37, 0.52, 0.69, 0.73, 0.81, 0.82, 0.85, 1.0, 0.94, 0.91, 0.75, 0.92, 0.96, 0.89, 0.77, 0.52, 0.39, 0.36], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]], 
        'profile_active_load_phase_c': [[0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.34, 0.36, 0.36, 0.37, 0.36, 0.33, 0.37, 0.52, 0.69, 0.73, 0.81, 0.82, 0.85, 1.0, 0.94, 0.91, 0.75, 0.92, 0.96, 0.89, 0.77, 0.52, 0.39, 0.36], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]], 
        'profile_reactive_load_phase_a': [[0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.29, 0.31, 0.31, 0.31, 0.3, 0.26, 0.3, 0.43, 0.64, 0.66, 0.73, 0.76, 0.74, 0.82, 0.77, 0.73, 0.66, 0.92, 1.0, 0.93, 0.75, 0.45, 0.35, 0.32], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]], 
        'profile_reactive_load_phase_b': [[0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.29, 0.31, 0.31, 0.31, 0.3, 0.26, 0.3, 0.43, 0.64, 0.66, 0.73, 0.76, 0.74, 0.82, 0.77, 0.73, 0.66, 0.92, 1.0, 0.93, 0.75, 0.45, 0.35, 0.32], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]], 
        'profile_reactive_load_phase_c': [[0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.29, 0.31, 0.31, 0.31, 0.3, 0.26, 0.3, 0.43, 0.64, 0.66, 0.73, 0.76, 0.74, 0.82, 0.77, 0.73, 0.66, 0.92, 1.0, 0.93, 0.75, 0.45, 0.35, 0.32], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]], 
        'photovoltaic_generation_phase_a': [0, 0, 0, 0, 245.33333333333334],#, 0, 0], 
        'photovoltaic_generation_phase_b': [0, 0, 0, 0, 245.33333333333334],#, 0, 0], 
        'photovoltaic_generation_phase_c': [0, 0, 0, 0, 245.33333333333334],#, 0, 0], 
        'profile_photovoltaic_generation': [[0, 0, 0, 0, 0.009, 0.073, 0.234, 0.449, 0.636, 0.768, 0.835, 0.841, 0.791, 0.685, 0.529, 0.333, 0.138, 0.024, 0, 0, 0, 0, 0, 0]], 
        'location_of_thermal_generation': {'1': [], '2': ['1'], '3': [], '4': [], '5': [], '6': [], '7': []}, 
        'minimum_active_power_thermal_generation': [0.0], 
        'maximum_active_power_thermal_generation': [106.05], 
        'minimum_reactive_power_thermal_generation': [-106.08203193755294], 
        'maximum_reactive_power_thermal_generation': [106.08203193755294], 
        'cost_thermal_generation': [30.0], 
        'location_of_energy_storage_system': {'1': [], '2': [], '3': [], '4': ['1'], '5': [], '6': [], '7': []}, 
        'initial_energy_of_the_ess': [372.29999999999995], 
        'minimum_energy_capacity_ess': [255.0], 
        'maximum_energy_capacity_ess': [1211.25], 
        'maximum_power_ess': [1275.0], 
        'ess_efficiency': [0.9], 
        'number_discrete_blocks_piecewise_linearization': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'], 
        # 'location_of_ev': {'1': [], '2': [], '3': [], '4': [], '5': [], '6': ['1'], '7': []}, 
        # 'initial_energy_of_the_ev_1': [64.8], 
        # 'minimum_energy_capacity_ev_1': [0.0], 
        # 'maximum_energy_capacity_ev_1': [324.0], 
        # 'maximum_power_ev_1': [80.0], 
        # 'ev_efficiency': [0.95], 
        # 't_arrival_1': [1], 
        # 't_departure_1': [7], 
        # 'initial_energy_of_the_ev_2': [21.6], 
        # 'minimum_energy_capacity_ev_2': [0.0], 
        # 'maximum_energy_capacity_ev_2': [108.0], 
        # 'maximum_power_ev_2': [11.0], 
        # 't_arrival_2': [8], 
        # 't_departure_2': [16]
        }

## **Sets:**

T = T_novo
N = data['set_of_nodes']
L = [tuple(x) for x in data["set_of_lines"]]
B = data['set_of_energy_storage_systems']
GD = data['set_of_thermal_generator']
# EV = data['set_of_electric_vehicles']
Y = data['number_discrete_blocks_piecewise_linearization']
O = data["set_of_outage"]
S = data['set_of_scenarios']


## **Parameters:**

### Parameter data preparation

Prob = {}
for index in range(len(data["probability_of_scen"])):
	Prob[S[index]] = data["probability_of_scen"][index]
sd = {}
for index in range(len(data["coefficient_demand_scen"])):
	sd[S[index]] = data["coefficient_demand_scen"][index]
spv = {}
for index in range(len(data["coefficient_pv_scen"])):
	spv[S[index]] = data["coefficient_pv_scen"][index]


Tb = {}
for index in range(len(data["type_of_bus"])):
	Tb[N[index]] = data["type_of_bus"][index]
Raa = {}
for index in range(len(data["resistance_raa"])):
	Raa[L[index]] = data["resistance_raa"][index]
Rbb = {}
for index in range(len(data["resistance_rbb"])):
	Rbb[L[index]] = data["resistance_rbb"][index]
Rcc = {}
for index in range(len(data["resistance_rcc"])):
	Rcc[L[index]] = data["resistance_rcc"][index]
Rab = {}
for index in range(len(data["resistance_rab"])):
	Rab[L[index]] = data["resistance_rab"][index]
Rbc = {}
for index in range(len(data["resistance_rbc"])):
	Rbc[L[index]] = data["resistance_rbc"][index]
Rac = {}
for index in range(len(data["resistance_rac"])):
	Rac[L[index]] = data["resistance_rac"][index]
Xaa = {}
for index in range(len(data["reactance_xaa"])):
	Xaa[L[index]] = data["reactance_xaa"][index]
Xbb = {}
for index in range(len(data["reactance_xbb"])):
	Xbb[L[index]] = data["reactance_xbb"][index]
Xcc = {}
for index in range(len(data["reactance_xcc"])):
	Xcc[L[index]] = data["reactance_xcc"][index]
Xab = {}
for index in range(len(data["reactance_xab"])):
	Xab[L[index]] = data["reactance_xab"][index]
	Xbc = {}
for index in range(len(data["reactance_xbc"])):
	Xbc[L[index]] = data["reactance_xbc"][index]
Xac = {}
for index in range(len(data["reactance_xac"])):
	Xac[L[index]] = data["reactance_xac"][index]

Vnom = data["nominal_voltage"]  # 11.9kV
Vmax = Vnom * 1.05 # kV
Vmin = Vnom * 0.95 # kV
out_time = 2

Imax = {}
for index in range(len(data["maximum_current_of_lines"])):
	Imax[L[index]] = data["maximum_current_of_lines"][index]

Smax = {}
for index in range(len(data["maximum_power_PCC"])):
	Smax[N[index]] = data["maximum_power_PCC"][index]

delta_t = data["variation_of_time"]

cEDS = {}
for index in range(len(data["cost_of_the_energy"])):
	cEDS[T[index]] = data["cost_of_the_energy"][index]

alpha_c = {}
for index in range(len(data['cost_of_load_curtailment'])):
	alpha_c[N[index]] = data['cost_of_load_curtailment'][index]

PDa_0 = {}
for index in range(len(data["nominal_active_load_phase_a"])):
	PDa_0[N[index]] = data["nominal_active_load_phase_a"][index]
PDb_0 = {}
for index in range(len(data["nominal_active_load_phase_b"])):
	PDb_0[N[index]] = data["nominal_active_load_phase_b"][index]
PDc_0 = {}
for index in range(len(data["nominal_active_load_phase_c"])):
	PDc_0[N[index]] = data["nominal_active_load_phase_c"][index]
QDa_0 = {}
for index in range(len(data["nominal_reactive_load_phase_a"])):
	QDa_0[N[index]] = data["nominal_reactive_load_phase_a"][index]
QDb_0 = {}
for index in range(len(data["nominal_reactive_load_phase_b"])):
	QDb_0[N[index]] = data["nominal_reactive_load_phase_b"][index]
QDc_0 = {}
for index in range(len(data["nominal_reactive_load_phase_c"])):
	QDc_0[N[index]] = data["nominal_reactive_load_phase_c"][index]
fm_pa = {}
for x in range(len(data["set_of_nodes"])):
	fm_pa[N[x]] = {}
	for index in range(len(data["set_of_time"])):
		fm_pa[N[x]][T[index]] = data["profile_active_load_phase_a"][x][index]
fm_pb = {}
for x in range(len(data["set_of_nodes"])):
	fm_pb[N[x]] = {}
	for index in range(len(data["set_of_time"])):
		fm_pb[N[x]][T[index]] = data["profile_active_load_phase_b"][x][index]
fm_pc = {}
for x in range(len(data["set_of_nodes"])):
	fm_pc[N[x]] = {}
	for index in range(len(data["set_of_time"])):
		fm_pc[N[x]][T[index]] = data["profile_active_load_phase_c"][x][index]
fm_qa = {}
for x in range(len(data["set_of_nodes"])):
	fm_qa[N[x]] = {}
	for index in range(len(data["set_of_time"])):
		fm_qa[N[x]][T[index]] = data["profile_reactive_load_phase_a"][x][index]
fm_qb = {}
for x in range(len(data["set_of_nodes"])):
	fm_qb[N[x]] = {}
	for index in range(len(data["set_of_time"])):
		fm_qb[N[x]][T[index]] = data["profile_reactive_load_phase_b"][x][index]
fm_qc = {}
for x in range(len(data["set_of_nodes"])):
	fm_qc[N[x]] = {}
	for index in range(len(data["set_of_time"])):
		fm_qc[N[x]][T[index]] = data["profile_reactive_load_phase_c"][x][index]
		

PVa_0 = {}
for index in range(len(data["photovoltaic_generation_phase_a"])):
	PVa_0[N[index]] = data["photovoltaic_generation_phase_a"][index]
PVb_0 = {}
for index in range(len(data["photovoltaic_generation_phase_b"])):
	PVb_0[N[index]] = data["photovoltaic_generation_phase_b"][index]
PVc_0 = {}
for index in range(len(data["photovoltaic_generation_phase_c"])):
	PVc_0[N[index]] = data["photovoltaic_generation_phase_c"][index]
fpv ={}
for index in range(len(data["profile_photovoltaic_generation"][0])):
	fpv[T[index]] = data["profile_photovoltaic_generation"][0][index]

# Location of GD, BESS, EV

dict_nos_gd = data["location_of_thermal_generation"]
PG_min = {}
PG_max = {}
QG_min = {}
QG_max = {}
cost_PG = {}
for index in range(len(data["set_of_thermal_generator"])):
	PG_min[GD[index]] = data["minimum_active_power_thermal_generation"][index]
	PG_max[GD[index]] = data["maximum_active_power_thermal_generation"][index]
	QG_min[GD[index]] = data["minimum_reactive_power_thermal_generation"][index]
	QG_max[GD[index]] = data["maximum_reactive_power_thermal_generation"][index]
	cost_PG[GD[index]] = data["cost_thermal_generation"][index]

dict_nos_bs = data["location_of_energy_storage_system"]
PBmax = {}
EBi = {}
EBmin = {}
EBmax = {}
eta_b = {}
for index in range(len(data["set_of_energy_storage_systems"])):
	PBmax[B[index]] = data["maximum_power_ess"][index]
	EBi[B[index]] = data["initial_energy_of_the_ess"][index]
	EBmin[B[index]] = data["minimum_energy_capacity_ess"][index]
	EBmax[B[index]] = data["maximum_energy_capacity_ess"][index]
	eta_b[B[index]] = data["ess_efficiency"][index]
	




from math import acos, atan, cos, sin, sqrt	
# Function to calculate Parameters

PDa = {}
PDb = {}
PDc = {}
QDa = {}
QDb = {}
QDc = {}
# Transforms the demands in variate values in the time
List_NT = []
for i in N:
	for t in T:
		List_NT += [[i, t]]
for (i,t) in List_NT:
	PDa[(i,t)] = ' '
	PDb[(i,t)] = ' '
	PDc[(i,t)] = ' '
	QDa[(i,t)] = ' '
	QDa[(i,t)] = ' '
	QDa[(i,t)] = ' '

for (i,t) in List_NT:
	PDa[(i,t)] = fm_pa[i][t] * PDa_0[i] 
	PDb[(i,t)] = fm_pb[i][t] * PDb_0[i] 
	PDc[(i,t)] = fm_pc[i][t] * PDc_0[i]
	QDa[(i,t)] = fm_qa[i][t] * QDa_0[i]
	QDb[(i,t)] = fm_qb[i][t] * QDb_0[i]
	QDc[(i,t)] = fm_qc[i][t] * QDc_0[i]
PVa = {}
PVb = {}
PVc = {}
for (i,t) in List_NT:
	PVa[(i,t)] = ' '
	PVb[(i,t)] = ' '
	PVc[(i,t)] = ' '
# Transforms the PV generation in variate values in the time
for (i,t) in List_NT:
	PVa[(i,t)] = fpv[t] * PVa_0[i]
	PVb[(i,t)] = fpv[t] * PVb_0[i]
	PVc[(i,t)] = fpv[t] * PVc_0[i]
for (i,j) in L:
	Raa[(i,j)] = Raa[(i,j)]/1000
	Rbb[(i,j)] = Rbb[(i,j)]/1000
	Rcc[(i,j)] = Rcc[(i,j)]/1000
	Rab[(i,j)] = Rab[(i,j)]/1000
	Rac[(i,j)] = Rac[(i,j)]/1000
	Rbc[(i,j)] = Rbc[(i,j)]/1000
	Xaa[(i,j)] = Xaa[(i,j)]/1000
	Xbb[(i,j)] = Xbb[(i,j)]/1000
	Xcc[(i,j)] = Xcc[(i,j)]/1000
	Xab[(i,j)] = Xab[(i,j)]/1000
	Xac[(i,j)] = Xac[(i,j)]/1000
	Xbc[(i,j)] = Xbc[(i,j)]/1000
# Calculats the impedance magnitude and angle in the lines
Thaa = {}
Zaa =  {}
Thbb = {}
Zbb =  {}
Thcc = {}
Zcc =  {}
Thab = {}
Zab =  {}
Thac = {}
Zac =  {}
Thbc = {}
Zbc =  {}
for (i,j) in L:
	Zaa[(i,j)] = ' '
	Zbb[(i,j)] = ' '
	Zcc[(i,j)] = ' '
	Zab[(i,j)] = ' '
	Zac[(i,j)] = ' '
	Zbc[(i,j)] = ' '
	Thaa[(i,j)] = ' '
	Thbb[(i,j)] = ' '
	Thcc[(i,j)] = ' '
	Thab[(i,j)] = ' '
	Thac[(i,j)] = ' '
	Thbc[(i,j)] = ' '
for (i,j) in L:
	Thaa[(i,j)] = atan(Xaa[(i,j)] / Raa[(i,j)])
	Zaa[(i,j)] = sqrt(Raa[(i,j)]**2 + Xaa[(i,j)]**2)
	Thbb[(i,j)] = atan(Xbb[(i,j)] / Rbb[(i,j)])
	Zbb[(i,j)] = sqrt(Rbb[(i,j)]**2 + Xbb[(i,j)]**2)
	Thcc[(i,j)] = atan(Xcc[(i,j)] / Rcc[(i,j)])
	Zcc[(i,j)] = sqrt(Rcc[(i,j)]**2 + Xcc[(i,j)]**2)
	Thab[(i,j)] = 0
	Zab[(i,j)] = sqrt(Rab[(i,j)]**2 + Xab[(i,j)]**2)
	Thac[(i,j)] = 0
	Zac[(i,j)] = sqrt(Rac[(i,j)]**2 + Xac[(i,j)]**2)
	Thbc[(i,j)] = 0
	Zbc[(i,j)] = sqrt(Rbc[(i,j)]**2 + Xbc[(i,j)]**2)
# Defines the angles of the phases
Tha0 = {}
Thb0 = {}
Thc0 = {}
for i in N:
	Tha0[i] = 0
	Thb0[i] = -2.0944
	Thc0[i] = 2.0944
# Calculation of Transformed Impedance Components
Raa_p = {}
Xaa_p = {}
Rbb_p = {}
Xbb_p = {}
Rcc_p = {}
Xcc_p = {}
Rab_p = {}
Xab_p = {}
Rac_p = {}
Xac_p = {}
Rbc_p = {}
Xbc_p = {}
Rba_p = {}
Xba_p = {}
Rca_p = {}
Xca_p = {}
Rcb_p = {}
Xcb_p = {}

for (i,j) in L:
	Raa_p[(i,j)] = ' '
	Xaa_p[(i,j)] = ' '
	Rbb_p[(i,j)] = ' '
	Xbb_p[(i,j)] = ' '
	Rcc_p[(i,j)] = ' '
	Xcc_p[(i,j)] = ' '
	Rab_p[(i,j)] = ' '
	Xab_p[(i,j)] = ' '
	Rac_p[(i,j)] = ' '
	Xac_p[(i,j)] = ' '
	Rbc_p[(i,j)] = ' '
	Xbc_p[(i,j)] = ' '
	Rba_p[(i,j)] = ' '
	Xba_p[(i,j)] = ' '
	Rca_p[(i,j)] = ' '
	Xca_p[(i,j)] = ' '
	Rcb_p[(i,j)] = ' '
	Xcb_p[(i,j)] = ' '
for (i,j) in L:
	Raa_p[(i,j)] = Zaa[(i,j)] * cos(Thaa[(i,j)] + Tha0[i] - Tha0[i])
	Xaa_p[(i,j)] = Zaa[(i,j)] * sin(Thaa[(i,j)] + Tha0[i] - Tha0[i])
	Rbb_p[(i,j)] = Zbb[(i,j)] * cos(Thbb[(i,j)] + Thb0[i] - Thb0[i])
	Xbb_p[(i,j)] = Zbb[(i,j)] * sin(Thbb[(i,j)] + Thb0[i] - Thb0[i])
	Rcc_p[(i,j)] = Zcc[(i,j)] * cos(Thcc[(i,j)] + Thc0[i] - Thc0[i])
	Xcc_p[(i,j)] = Zcc[(i,j)] * sin(Thcc[(i,j)] + Thc0[i] - Thc0[i])
	Rab_p[(i,j)] = Zab[(i,j)] * cos(Thab[(i,j)] + Thb0[i] - Tha0[i])
	Xab_p[(i,j)] = Zab[(i,j)] * sin(Thab[(i,j)] + Thb0[i] - Tha0[i])
	Rac_p[(i,j)] = Zac[(i,j)] * cos(Thac[(i,j)] + Thc0[i] - Tha0[i])
	Xac_p[(i,j)] = Zac[(i,j)] * sin(Thac[(i,j)] + Thc0[i] - Tha0[i])
	Rbc_p[(i,j)] = Zbc[(i,j)] * cos(Thbc[(i,j)] + Thc0[i] - Thb0[i])
	Xbc_p[(i,j)] = Zbc[(i,j)] * sin(Thbc[(i,j)] + Thc0[i] - Thb0[i])
	Rba_p[(i,j)] = Zab[(i,j)] * cos(Thab[(i,j)] + Tha0[i] - Thb0[i])
	Xba_p[(i,j)] = Zab[(i,j)] * sin(Thab[(i,j)] + Tha0[i] - Thb0[i])
	Rca_p[(i,j)] = Zac[(i,j)] * cos(Thac[(i,j)] + Tha0[i] - Thc0[i])
	Xca_p[(i,j)] = Zac[(i,j)] * sin(Thac[(i,j)] + Tha0[i] - Thc0[i])
	Rcb_p[(i,j)] = Zbc[(i,j)] * cos(Thbc[(i,j)] + Thb0[i] - Thc0[i])
	Xcb_p[(i,j)] = Zbc[(i,j)] * sin(Thbc[(i,j)] + Thb0[i] - Thc0[i])		

# ### Power flow direction

List_NL = []
for a in N:
	for (i,j) in L:
		List_NL += [[a,i,j]]
df = {}
for (a,i,j) in List_NL:
	df[(a,i,j)] = ' '
for a in N:
	for (i,j) in L:
		if int(a) == int(i):
			df[(a,i,j)] = -1
		elif int(a) == int(j):
			df[(a,i,j)] = 1
		else:
			df[(a,i,j)] = 0

p = {} # dperdas
for (a,i,j) in List_NL:
		p[(a,i,j)] = ' '
for i in N:
		for (a,j) in L:
			if int(i) == int(a):
				p[(i,a,j)] = 1
			else:
				p[(i,a,j)] = 0

# ### Define linearization blocks

S_Dp_max = {}
S_ms = {}

for (i,j) in L:
    S_Dp_max[i,j] = (Vnom * Imax[i,j]) / len(Y)
    for y in Y:
        S_ms[i,j,y] = ((2*int(y)) - 1) *  S_Dp_max[i,j] 


Spcc_Dp_max = {}
Spcc_ms = {}

for i in N:
    Spcc_Dp_max[i] = (Smax[i]) / len(Y)
    for y in Y:
        Spcc_ms[i,y] = ((2*int(y)) - 1) *  Spcc_Dp_max[i] 
        

# ### Creating lists

List_LTS = []
for (i,j) in L:
	for t in T:
		for s in S:
			List_LTS += [[i, j, t, s]]
List_NTS = []
for i in N:
	for t in T:
		for s in S:
		    List_NTS += [[i, t, s]]
List_GDTS = []
for i in GD:
	for t in T:
		for s in S:
		    List_GDTS += [[i, t, s]]
List_BT = []
for i in B:
	for t in T:
		List_BT += [[i, t]]
  

          
List_LTSY = []
for (i,j) in L:
	for t in T:
		for s in S:
		    for y in Y:
			    List_LTSY += [[i, j, t, s, y]]

List_NTSY = []
for i in N:
	for t in T:
		for s in S:
		    for y in Y:
			    List_NTSY += [[i, t, s, y]]

# list's contingences
List_LTOS = []
for (i,j) in L:
	for t in T:
		for c in O:
			for s in S:
			    List_LTOS += [[i, j, t, c, s]]
List_NTOS = []
for i in N:
	for t in T:
		for c in O:
			for s in S:
			    List_NTOS += [[i, t, c, s]]
List_GDTOS = []
for i in GD:
	for t in T:
		for c in O:
			for s in S:
			    List_GDTOS += [[i, t, c, s]]
List_NTOSY = []
for i in N:
	for t in T:
		for c in O:
			for s in S:
			    for y in Y:
				    List_NTOSY += [[i, t, c, s, y]]
List_LTOSY = []
for (i,j) in L:
	for t in T:
		for c in O:
			for s in S:
			    for y in Y:
				    List_LTOSY += [[i, j, t, c, s, y]]
        

### Start the complete model ###
model_cs = ConcreteModel("Modelo_coldstar_EMS_PYOMO")

# Declare variables
model_cs.Pa = Var(L, T, S, within = Reals)
model_cs.Pb = Var(L, T, S, within = Reals)
model_cs.Pc = Var(L, T, S, within = Reals)
model_cs.Qa = Var(L, T, S, within = Reals)
model_cs.Qb = Var(L, T, S, within = Reals)
model_cs.Qc = Var(L, T, S, within = Reals)
model_cs.Va = Var(N, T, S, within = Reals)
model_cs.Vb = Var(N, T, S, within = Reals)
model_cs.Vc = Var(N, T, S, within = Reals)

model_cs.Ppcc_a = Var(N, T, S, within = Reals)
model_cs.Ppcc_b = Var(N, T, S, within = Reals)
model_cs.Ppcc_c = Var(N, T, S, within = Reals)
model_cs.Qpcc_a = Var(N, T, S, within = Reals)
model_cs.Qpcc_b = Var(N, T, S, within = Reals)
model_cs.Qpcc_c = Var(N, T, S, within = Reals)
model_cs.Ppcc = Var(N, T, S, within = Reals)
model_cs.Qpcc = Var(N, T, S, within = Reals)

model_cs.PGa = Var(GD, T, S, within = NonNegativeReals)
model_cs.PGb = Var(GD, T, S, within = NonNegativeReals)
model_cs.PGc = Var(GD, T, S, within = NonNegativeReals)
model_cs.QGa = Var(GD, T, S, within = NonNegativeReals)
model_cs.QGb = Var(GD, T, S, within = NonNegativeReals)
model_cs.QGc = Var(GD, T, S, within = NonNegativeReals)
model_cs.PG =  Var(GD, T, S, within = NonNegativeReals)
model_cs.QG =  Var(GD, T, S, within = NonNegativeReals)

# Variables for contingences

model_cs.Pa_out = Var(L, T, O, S, within = Reals)
model_cs.Pb_out = Var(L, T, O, S, within = Reals)
model_cs.Pc_out = Var(L, T, O, S, within = Reals)
model_cs.Qa_out = Var(L, T, O, S, within = Reals)
model_cs.Qb_out = Var(L, T, O, S, within = Reals)
model_cs.Qc_out = Var(L, T, O, S, within = Reals)
model_cs.Va_out = Var(N, T, O, S, within = Reals)
model_cs.Vb_out = Var(N, T, O, S, within = Reals)
model_cs.Vc_out = Var(N, T, O, S, within = Reals)

model_cs.Ppcc_a_out = Var(N, T, O, S, within = Reals)
model_cs.Ppcc_b_out = Var(N, T, O, S, within = Reals)
model_cs.Ppcc_c_out = Var(N, T, O, S, within = Reals)
model_cs.Qpcc_a_out = Var(N, T, O, S, within = Reals)
model_cs.Qpcc_b_out = Var(N, T, O, S, within = Reals)
model_cs.Qpcc_c_out = Var(N, T, O, S, within = Reals)
model_cs.Ppcc_out = Var(N, T, O, S, within = Reals)
model_cs.Qpcc_out = Var(N, T, O, S, within = Reals)

model_cs.PGa_out = Var(GD, T, O, S, within = NonNegativeReals)
model_cs.PGb_out = Var(GD, T, O, S, within = NonNegativeReals)
model_cs.PGc_out = Var(GD, T, O, S, within = NonNegativeReals)
model_cs.QGa_out = Var(GD, T, O, S, within = NonNegativeReals)
model_cs.QGb_out = Var(GD, T, O, S, within = NonNegativeReals)
model_cs.QGc_out = Var(GD, T, O, S, within = NonNegativeReals)
model_cs.PG_out =  Var(GD, T, O, S, within = NonNegativeReals)
model_cs.QG_out =  Var(GD, T, O, S, within = NonNegativeReals)

model_cs.xd = Var(N, T, O, S, domain = Reals, bounds = (0, 1))	

# Objective function
if len(O) >= 1 :
    cost_operation_contingency_cs = (sum(Prob[s]*(0.01/len(O) * (sum(cEDS[t] * delta_t * (model_cs.Ppcc_a_out[i, t, o, s] + model_cs.Ppcc_b_out[i, t, o, s] + model_cs.Ppcc_c_out[i, t, o, s]) for (i, t, o, s) in List_NTOS) + 
                                    sum([cost_PG[i] * delta_t * model_cs.PG_out[i,t,o, s] for (i,t,o,s) in List_GDTOS]) + 
                                    sum([delta_t * alpha_c[i] * sd[s] * (PDa[(i,t)]+PDb[(i,t)]+PDc[(i,t)]) * (1-model_cs.xd[i,t,o,s]) for (i,t,o,s) in List_NTOS]))) + 
                                    (0.99 * sum(cEDS[t] * delta_t * (model_cs.Ppcc_a[i, t,s] + model_cs.Ppcc_b[i, t,s] + model_cs.Ppcc_c[i, t,s]) for (i, t,s) in List_NTS) + 
                                    sum(cost_PG[i] * delta_t * model_cs.PG[i, t,s] for (i, t,s) in List_GDTS)) for s in S))
else :
    cost_operation_contingency_cs = (sum(Prob[s]*(0.01/1000000 * (sum(cEDS[t] * delta_t * (model_cs.Ppcc_a_out[i, t, o, s] + model_cs.Ppcc_b_out[i, t, o, s] + model_cs.Ppcc_c_out[i, t, o, s]) for (i, t, o, s) in List_NTOS) + 
                                    sum([delta_t * alpha_c[i] * sd[s] * (PDa[(i,t)]+PDb[(i,t)]+PDc[(i,t)]) * (1-model_cs.xd[i,t,o,s]) for (i,t,o,s) in List_NTOS]))) +
                                    (0.99 * sum(cEDS[t] * delta_t * (model_cs.Ppcc_a[i, t,s] + model_cs.Ppcc_b[i, t,s] + model_cs.Ppcc_c[i, t,s]) for (i, t,s) in List_NTS)) for s in S))

model_cs.objective_function_cs = Objective(expr=cost_operation_contingency_cs)

# Constraints without contingences---------------------------------------------------------------- 

#ACTIVE POWER BALANCE WITHOUT CONTINGENCES
def active_power_balance_rule_a(model_cs, i,t, s):
    return (
        sum(model_cs.Pa[a, j, t, s]*df[(i,a,j)] for (a,j) in L) +
        model_cs.Ppcc_a[i, t, s] + sum(model_cs.PGa[a, t, s] for a in dict_nos_gd[i]) - PDa[(i,t)]*sd[s] == 0) 
model_cs.active_power_balance_a = Constraint(List_NTS, rule=active_power_balance_rule_a)

def active_power_balance_rule_b(model_cs, i,t, s):
    return (
        sum(model_cs.Pb[a, j, t, s]*df[(i,a,j)] for (a,j) in L) +
        model_cs.Ppcc_b[i, t, s] + sum(model_cs.PGb[a, t, s] for a in dict_nos_gd[i]) -
        PDb[(i,t)]*sd[s] == 0)
model_cs.active_power_balance_b = Constraint(List_NTS, rule=active_power_balance_rule_b)

def active_power_balance_rule_c(model_cs, i,t, s):
    return (
        sum(model_cs.Pc[a, j, t, s]*df[(i,a,j)] for (a,j) in L) +
        model_cs.Ppcc_c[i, t, s] + sum(model_cs.PGc[a, t, s] for a in dict_nos_gd[i]) -
        PDc[(i,t)]*sd[s] == 0)
model_cs.active_power_balance_c = Constraint(List_NTS, rule=active_power_balance_rule_c)

#REACTIVE POWER BALANCE
def reactive_power_balance_rule_a(model_cs, i,t, s):
    return (
        sum(model_cs.Qa[a, j, t, s]*df[(i,a,j)] for (a,j) in L) +
        model_cs.Qpcc_a[i, t, s] + sum(model_cs.QGa[a, t, s] for a in dict_nos_gd[i]) -
        QDa[(i,t)]*sd[s] == 0)
model_cs.reactive_power_balance_a = Constraint(List_NTS, rule=reactive_power_balance_rule_a)

def reactive_power_balance_rule_b(model_cs, i,t, s):
    return (
        sum(model_cs.Qb[a, j, t, s]*df[(i,a,j)] for (a,j) in L) +
        model_cs.Qpcc_b[i, t, s] + sum(model_cs.QGb[a, t, s] for a in dict_nos_gd[i])-
        QDb[(i,t)]*sd[s] == 0)
model_cs.reactive_power_balance_b = Constraint(List_NTS, rule=reactive_power_balance_rule_b)

def reactive_power_balance_rule_c(model_cs, i,t, s):
    return (
        sum(model_cs.Qc[a, j, t, s]*df[(i,a,j)] for (a,j) in L) +
        model_cs.Qpcc_c[i, t, s]+ sum(model_cs.QGc[a, t, s] for a in dict_nos_gd[i]) -
        QDc[(i,t)]*sd[s] == 0)
model_cs.reactive_power_balance_c = Constraint(List_NTS, rule=reactive_power_balance_rule_c)

# GENSET CONSTRAINTS
def genset_power_rule(model_cs, i,t, s):
    return(model_cs.PGa[i, t, s] + model_cs.PGb[i, t, s] + model_cs.PGc[i, t, s] == model_cs.PG[i, t, s])
model_cs.genset_power_active = Constraint(List_GDTS, rule=genset_power_rule)

def genset_power_reactive_rule(model_cs, i,t, s):
    return(model_cs.QGa[i, t, s] + model_cs.QGb[i, t, s] + model_cs.QGc[i, t, s] == model_cs.QG[i, t, s])
model_cs.genset_power_reactive = Constraint(List_GDTS, rule=genset_power_reactive_rule)

def genset_power_active_limits_rule_1(model_cs, i,t, s):
    return(model_cs.PG[i, t, s] >= PG_min[i])
model_cs.genset_power_active_limits_1 = Constraint(List_GDTS, rule = genset_power_active_limits_rule_1)

def genset_power_active_limits_rule_2(model_cs, i,t, s):
    return(model_cs.PG[i, t, s] <= PG_max[i])
model_cs.genset_power_active_limits_2 = Constraint(List_GDTS, rule = genset_power_active_limits_rule_2)

def genset_power_reactive_limits_rule_1(model_cs, i,t, s):
    return(model_cs.QG[i, t, s] >= QG_min[i])
model_cs.genset_power_reactive_limits_1 = Constraint(List_GDTS, rule = genset_power_reactive_limits_rule_1)

def genset_power_reactive_limits_rule_2(model_cs, i,t, s):
    return(model_cs.QG[i, t, s] <= QG_max[i])
model_cs.genset_power_reactive_limits_2 = Constraint(List_GDTS, rule = genset_power_reactive_limits_rule_2)

def genset_operation_1_rule(model_cs, i,t, s):
    return(model_cs.PGa[i, t, s] == 0)
model_cs.genset_operation_1 = Constraint(List_GDTS, rule = genset_operation_1_rule)

def genset_operation_2_rule(model_cs, i,t, s):
    return(model_cs.PGb[i, t, s] == 0)
model_cs.genset_operation_2 = Constraint(List_GDTS, rule = genset_operation_2_rule)

def genset_operation_3_rule(model_cs, i,t, s):
    return(model_cs.PGc[i, t, s] == 0)
model_cs.genset_operation_3 = Constraint(List_GDTS, rule = genset_operation_3_rule)

def genset_operation_4_rule(model_cs, i,t, s):
    return(model_cs.QGa[i, t, s] == 0)
model_cs.genset_operation_4 = Constraint(List_GDTS, rule = genset_operation_4_rule)

def genset_operation_5_rule(model_cs, i,t, s):
    return(model_cs.QGb[i, t, s] == 0)
model_cs.genset_operation_5 = Constraint(List_GDTS, rule = genset_operation_5_rule)

def genset_operation_6_rule(model_cs, i,t, s):
    return(model_cs.QGc[i, t, s] == 0)
model_cs.genset_operation_6 = Constraint(List_GDTS, rule = genset_operation_6_rule)

#FIX VARIABLES

def fix_voltage_a_rule(model_cs,i,t,s):
    return(model_cs.Va[i,t,s] == Vnom)
model_cs.fix_voltage_a = Constraint(List_NTS, rule = fix_voltage_a_rule)

def fix_voltage_b_rule(model_cs,i,t,s):
    return(model_cs.Vb[i,t,s] == Vnom)
model_cs.fix_voltage_b = Constraint(List_NTS, rule = fix_voltage_b_rule)

def fix_voltage_c_rule(model_cs,i,t,s):
    return(model_cs.Vc[i,t,s] == Vnom)
model_cs.fix_voltage_c = Constraint(List_NTS, rule = fix_voltage_c_rule)

model_cs.fix_active_power = ConstraintList()
for i in Tb:
    for t in T:
        for s in S:
            if Tb[i] != 1:
                model_cs.fix_active_power.add(expr = model_cs.Ppcc_a[i,t,s] == 0)
                model_cs.fix_active_power.add(expr = model_cs.Ppcc_b[i,t,s] == 0)
                model_cs.fix_active_power.add(expr = model_cs.Ppcc_c[i,t,s] == 0)

model_cs.fix_reactive_power = ConstraintList()
for i in Tb:
    for t in T:
        for s in S:
            if Tb[i] != 1:
                model_cs.fix_reactive_power.add(expr=model_cs.Qpcc_a[i, t, s] == 0)
                model_cs.fix_reactive_power.add(expr=model_cs.Qpcc_b[i, t, s] == 0)
                model_cs.fix_reactive_power.add(expr=model_cs.Qpcc_c[i, t, s] == 0)

# ------------------------------------------------------------------------------
#------------- Operation with outage - COLD START ------------------------------
# ------------------------------------------------------------------------------
#
#ACTIVE POWER BALANCE

def active_power_balance_rule_a_out(model_cs, i, t, o, s):
    return (
        sum(model_cs.Pa_out[a, j, t, o, s] * df[(i, a, j)] for (a, j) in L) +
        sum(model_cs.PGa_out[a, t, o, s] for a in dict_nos_gd[i]) +
        model_cs.Ppcc_a_out[i, t, o, s] - PDa[(i, t)] * model_cs.xd[i, t, o, s] * sd[s] == 0
    )

model_cs.active_power_balance_a_out = Constraint(List_NTOS, rule=active_power_balance_rule_a_out)

def active_power_balance_rule_b_out(model_cs, i, t, o, s):
    return (
        sum(model_cs.Pb_out[a, j, t, o, s] * df[(i, a, j)] for (a, j) in L) +
        sum(model_cs.PGb_out[a, t, o, s] for a in dict_nos_gd[i]) +
        model_cs.Ppcc_b_out[i, t, o, s] -
        PDb[(i, t)] * model_cs.xd[i, t, o, s] * sd[s] == 0
    )

model_cs.active_power_balance_b_out = Constraint(List_NTOS, rule=active_power_balance_rule_b_out)

def active_power_balance_rule_c_out(model_cs, i, t, o, s):
    return (
        sum(model_cs.Pc_out[a, j, t, o, s] * df[(i, a, j)] for (a, j) in L) +
        sum(model_cs.PGc_out[a, t, o, s] for a in dict_nos_gd[i]) +
        model_cs.Ppcc_c_out[i, t, o, s] -
        PDc[(i, t)] * model_cs.xd[i, t, o, s] * sd[s] == 0
    )

model_cs.active_power_balance_c_out = Constraint(List_NTOS, rule=active_power_balance_rule_c_out)

#REACTIVE POWER BALANCE

def reactive_power_balance_rule_a_out(model_cs, i, t, o, s):
    return (
        sum(model_cs.Qa_out[a, j, t, o, s] * df[(i, a, j)] for (a, j) in L) +
        sum(model_cs.QGa_out[a, t, o, s] for a in dict_nos_gd[i]) +
        model_cs.Qpcc_a_out[i, t, o, s] -
        QDa[(i, t)] * model_cs.xd[i, t, o, s] * sd[s] == 0
    )

model_cs.reactive_power_balance_a_out = Constraint(List_NTOS, rule=reactive_power_balance_rule_a_out)

def reactive_power_balance_rule_b_out(model_cs, i, t, o, s):
    return (
        sum(model_cs.Qb_out[a, j, t, o, s] * df[(i, a, j)] for (a, j) in L) +
        sum(model_cs.QGb_out[a, t, o, s] for a in dict_nos_gd[i]) +
        model_cs.Qpcc_b_out[i, t, o, s] -
        QDb[(i, t)] * model_cs.xd[i, t, o, s] * sd[s] == 0
    )

model_cs.reactive_power_balance_b_out = Constraint(List_NTOS, rule=reactive_power_balance_rule_b_out)

def reactive_power_balance_rule_c_out(model_cs, i, t, o, s):
    return (
        sum(model_cs.Qc_out[a, j, t, o, s] * df[(i, a, j)] for (a, j) in L) +
        sum(model_cs.QGc_out[a, t, o, s] for a in dict_nos_gd[i]) +
        model_cs.Qpcc_c_out[i, t, o, s] -
        QDc[(i, t)] * model_cs.xd[i, t, o, s] * sd[s] == 0
    )

model_cs.reactive_power_balance_c_out = Constraint(List_NTOS, rule=reactive_power_balance_rule_c_out)

#GENSET OPERATION CONSTRAINS

def genset_power_rule_out(model_cs, i, t, o, s):
    return (model_cs.PGa_out[i, t, o, s] + model_cs.PGb_out[i, t, o, s] + model_cs.PGc_out[i, t, o, s] == model_cs.PG_out[i, t, o, s])

model_cs.genset_power_active_out = Constraint(List_GDTOS, rule=genset_power_rule_out)

def genset_power_reactive_rule_out(model_cs, i, t, o, s):
    return (model_cs.QGa_out[i, t, o, s] + model_cs.QGb_out[i, t, o, s] + model_cs.QGc_out[i, t, o, s] == model_cs.QG_out[i, t, o, s])

model_cs.genset_power_reactive_out = Constraint(List_GDTOS, rule=genset_power_reactive_rule_out)

def genset_power_active_limits_rule_out_1(model_cs, i, t, o, s):
    return (model_cs.PG_out[i, t, o, s] >= PG_min[i])

model_cs.genset_power_active_limits_1_out = Constraint(List_GDTOS, rule=genset_power_active_limits_rule_out_1)

def genset_power_active_limits_rule_out_2(model_cs, i, t, o, s):
    return (model_cs.PG_out[i, t, o, s] <= PG_max[i])

model_cs.genset_power_active_limits_2_out = Constraint(List_GDTOS, rule=genset_power_active_limits_rule_out_2)

def genset_power_reactive_limits_rule_out_1(model_cs, i, t, o, s):
    return (model_cs.QG_out[i, t, o, s] >= QG_min[i])

model_cs.genset_power_reactive_limits_1_out = Constraint(List_GDTOS, rule=genset_power_reactive_limits_rule_out_1)

def genset_power_reactive_limits_rule_out_2(model_cs, i, t, o, s):
    return (model_cs.QG_out[i, t, o, s] <= QG_max[i])

model_cs.genset_power_reactive_limits_2_out = Constraint(List_GDTOS, rule=genset_power_reactive_limits_rule_out_2)

# FIX VARIABLES: ISLANDED OPERATION

model_cs.islanded_operation = ConstraintList()
for i in N:
    for t in T:
        for o in O:
            for s in S:
                if datetime.strptime(t, '%H:%M:%S') >= datetime.strptime(o, '%H:%M:%S') and datetime.strptime(t, '%H:%M:%S') < datetime.strptime(o, '%H:%M:%S') + timedelta(hours=out_time):    
                    model_cs.islanded_operation.add(expr=model_cs.Ppcc_a_out[i, t, o, s] == 0)
                    model_cs.islanded_operation.add(expr=model_cs.Ppcc_b_out[i, t, o, s] == 0)
                    model_cs.islanded_operation.add(expr=model_cs.Ppcc_c_out[i, t, o, s] == 0)
                    model_cs.islanded_operation.add(expr=model_cs.Qpcc_a_out[i, t, o, s] == 0)
                    model_cs.islanded_operation.add(expr=model_cs.Qpcc_b_out[i, t, o, s] == 0)
                    model_cs.islanded_operation.add(expr=model_cs.Qpcc_c_out[i, t, o, s] == 0)

def fix_voltage_a_rule_out(model_cs, i, t, o, s):
    return (model_cs.Va_out[i, t, o, s] == Vnom)

model_cs.fix_voltage_a_out = Constraint(List_NTOS, rule=fix_voltage_a_rule_out)

def fix_voltage_b_rule_out(model_cs, i, t, o, s):
    return (model_cs.Vb_out[i, t, o, s] == Vnom)

model_cs.fix_voltage_b_out = Constraint(List_NTOS, rule=fix_voltage_b_rule_out)

def fix_voltage_c_rule_out(model_cs, i, t, o, s):
    return (model_cs.Vc_out[i, t, o, s] == Vnom)

model_cs.fix_voltage_c_out = Constraint(List_NTOS, rule=fix_voltage_c_rule_out)

model_cs.fix_active_power_out = ConstraintList()
for i in Tb:
    for t in T:
        for o in O:
            for s in S:
                if Tb[i] != 1:
                    model_cs.fix_active_power_out.add(expr=model_cs.Ppcc_a_out[i, t, o, s] == 0)
                    model_cs.fix_active_power_out.add(expr=model_cs.Ppcc_b_out[i, t, o, s] == 0)
                    model_cs.fix_active_power_out.add(expr=model_cs.Ppcc_c_out[i, t, o, s] == 0)

model_cs.fix_reactive_power_out = ConstraintList()
for i in Tb:
    for t in T:
        for o in O:
            for s in S:
                if Tb[i] != 1:
                    model_cs.fix_reactive_power_out.add(expr=model_cs.Qpcc_a_out[i, t, o, s] == 0)
                    model_cs.fix_reactive_power_out.add(expr=model_cs.Qpcc_b_out[i, t, o, s] == 0)
                    model_cs.fix_reactive_power_out.add(expr=model_cs.Qpcc_c_out[i, t, o, s] == 0)


# Resultado_cs = SolverFactory('cbc', executable='C:/Solvers/cbc.exe').solve(model_cs)
Resultado_cs = SolverFactory('gurobi').solve(model_cs)
print("Solver Status CS:", Resultado_cs.solver.status)
print("Termination Condition CS:", Resultado_cs.solver.termination_condition)


Pa_0 = model_cs.Pa.get_values()
Pb_0 = model_cs.Pb.get_values()
Pc_0 = model_cs.Pc.get_values()
Qa_0 = model_cs.Qa.get_values()
Qb_0 = model_cs.Qb.get_values()
Qc_0 = model_cs.Qc.get_values()
Va_0 = model_cs.Va.get_values()
Vb_0 = model_cs.Vb.get_values()
Vc_0 = model_cs.Vc.get_values()

Pa_0_out = model_cs.Pa_out.get_values()
Pb_0_out = model_cs.Pb_out.get_values()
Pc_0_out = model_cs.Pc_out.get_values()
Qa_0_out = model_cs.Qa_out.get_values()
Qb_0_out = model_cs.Qb_out.get_values()
Qc_0_out = model_cs.Qc_out.get_values()
Va_0_out = model_cs.Va_out.get_values()
Vb_0_out = model_cs.Vb_out.get_values()
Vc_0_out = model_cs.Vc_out.get_values()

############################################################################
###############################  PARTE 2 ###################################
############################################################################




C = list()
for evcs in EVCS.keys():
    dc = [connector for connector in EVCS[evcs]['connector'].keys() if EVCS[evcs]['connector'][connector]['current'] == 'DC']
    ac = [connector for connector in EVCS[evcs]['connector'].keys() if EVCS[evcs]['connector'][connector]['current'] == 'AC']
    # Ωc_dc[evcs] = dc
    # Ωc_ac[evcs] = ac
    for connector in EVCS[evcs]['connector'].keys():
        C.append((evcs, connector))

E = list(EV.keys())

dict_nos_evcs = dict()
for i in N:
    dict_nos_evcs[i] = [evcs for evcs in EVCS.keys() if i in EVCS[evcs]['node']]
        

model = ConcreteModel("Modelo_EMS_PYOMO")


model.Pa = Var(L, T, S,within = Reals)
model.Pb = Var(L, T, S,within = Reals)
model.Pc = Var(L, T, S,within = Reals)
model.Qa = Var(L, T, S,within = Reals)
model.Qb = Var(L, T, S,within = Reals)
model.Qc = Var(L, T, S,within = Reals)
model.Va = Var(N, T, S,within = Reals)
model.Vb = Var(N, T, S,within = Reals)
model.Vc = Var(N, T, S,within = Reals)

model.Plss_a = Var(L, T, S,within = Reals)
model.Plss_b = Var(L, T, S,within = Reals)
model.Plss_c = Var(L, T, S,within = Reals)
model.Qlss_a = Var(L, T, S,within = Reals)
model.Qlss_b = Var(L, T, S,within = Reals)
model.Qlss_c = Var(L, T, S,within = Reals)

model.Ppcc_a = Var(N, T, S,within = Reals)
model.Ppcc_b = Var(N, T, S,within = Reals)
model.Ppcc_c = Var(N, T, S,within = Reals)
model.Qpcc_a = Var(N, T, S,within = Reals)
model.Qpcc_b = Var(N, T, S,within = Reals)
model.Qpcc_c = Var(N, T, S,within = Reals)

model.Ppcc = Var(N, T, S,within = Reals)
model.Qpcc = Var(N, T, S,within = Reals)

model.Ppcc_a_po = Var(N, T, S,within = NonNegativeReals)
model.Ppcc_b_po = Var(N, T, S,within = NonNegativeReals)
model.Ppcc_c_po = Var(N, T, S,within = NonNegativeReals)
model.Ppcc_a_ne = Var(N, T, S,within = NonNegativeReals)
model.Ppcc_b_ne = Var(N, T, S,within = NonNegativeReals)
model.Ppcc_c_ne = Var(N, T, S,within = NonNegativeReals)

model.PGa = Var(GD, T, S,within = NonNegativeReals)
model.PGb = Var(GD, T, S,within = NonNegativeReals)
model.PGc = Var(GD, T, S,within = NonNegativeReals)
model.QGa = Var(GD, T, S,within = NonNegativeReals)
model.QGb = Var(GD, T, S,within = NonNegativeReals)
model.QGc = Var(GD, T, S,within = NonNegativeReals)
model.PG =  Var(GD, T, S,within = NonNegativeReals)
model.QG =  Var(GD, T, S,within = NonNegativeReals)

model.EB = Var(B, T, within = Reals)
model.PB = Var(B, T, within = Reals)
model.b_ch =     Var(B, T, within=Binary)
model.b_dis =    Var(B, T, within=Binary)
model.PB_ch =    Var(B, T, within = Reals)
model.PB_dis =   Var(B, T, within = Reals)
model.PB_ch_a =  Var(B, T, within = Reals)
model.PB_ch_b =  Var(B, T, within = Reals)
model.PB_ch_c =  Var(B, T, within = Reals)
model.PB_dis_a = Var(B, T, within = Reals)
model.PB_dis_b = Var(B, T, within = Reals)
model.PB_dis_c = Var(B, T, within = Reals)

# Power flow linearization variables
model.Pa_sqr = Var(L, T, S, within = Reals)
model.Pb_sqr = Var(L, T, S, within = Reals)
model.Pc_sqr = Var(L, T, S, within = Reals)
model.Qa_sqr = Var(L, T, S, within = Reals)
model.Qb_sqr = Var(L, T, S, within = Reals)
model.Qc_sqr = Var(L, T, S, within = Reals)

model.Pa_p = Var(L, T, S, within = NonNegativeReals)
model.Pa_n = Var(L, T, S, within = NonNegativeReals)
model.Pb_p = Var(L, T, S, within = NonNegativeReals)
model.Pb_n = Var(L, T, S, within = NonNegativeReals)
model.Pc_p = Var(L, T, S, within = NonNegativeReals)
model.Pc_n = Var(L, T, S, within = NonNegativeReals)
model.Qa_p = Var(L, T, S, within = NonNegativeReals)
model.Qa_n = Var(L, T, S, within = NonNegativeReals)
model.Qb_p = Var(L, T, S, within = NonNegativeReals)
model.Qb_n = Var(L, T, S, within = NonNegativeReals)
model.Qc_p = Var(L, T, S, within = NonNegativeReals)
model.Qc_n = Var(L, T, S, within = NonNegativeReals)

model.Pa_Dp = Var(L, T, S, Y, within = NonNegativeReals)
model.Pb_Dp = Var(L, T, S, Y, within = NonNegativeReals)
model.Pc_Dp = Var(L, T, S, Y, within = NonNegativeReals)
model.Qa_Dp = Var(L, T, S, Y, within = NonNegativeReals)
model.Qb_Dp = Var(L, T, S, Y, within = NonNegativeReals)
model.Qc_Dp = Var(L, T, S, Y, within = NonNegativeReals)

# Linearization of PCC
model.Ppcc_sqr = Var(N, T, S, within = NonNegativeReals)
model.Qpcc_sqr = Var(N, T, S, within = NonNegativeReals)
model.Ppcc_p = Var(N, T, S, within = NonNegativeReals)
model.Ppcc_n = Var(N, T, S, within = NonNegativeReals)
model.Qpcc_n = Var(N, T, S, within = NonNegativeReals)
model.Qpcc_p = Var(N, T, S, within = NonNegativeReals)
model.Ppcc_Dp = Var(N, T, S, Y,within =  NonNegativeReals)
model.Qpcc_Dp = Var(N, T, S, Y, within = NonNegativeReals)



# Voltage linearization variables
model.Va_sqr = Var(N, T, S, within = NonNegativeReals, bounds = (Vmin**2, Vmax**2))
model.Vb_sqr = Var(N, T, S, within = NonNegativeReals, bounds = (Vmin**2, Vmax**2))
model.Vc_sqr = Var(N, T, S, within = NonNegativeReals, bounds = (Vmin**2, Vmax**2))

## ------ Variables for contingences --------------
model.Pa_out =     Var(L, T, O, S, within = Reals)
model.Pb_out =     Var(L, T, O, S, within = Reals)
model.Pc_out =     Var(L, T, O, S, within = Reals)
model.Qa_out =     Var(L, T, O, S, within = Reals)
model.Qb_out =     Var(L, T, O, S, within = Reals)
model.Qc_out =     Var(L, T, O, S, within = Reals)

model.Va_out =     Var(N, T, O, S, within = Reals)
model.Vb_out =     Var(N, T, O, S, within = Reals)
model.Vc_out =     Var(N, T, O, S, within = Reals)

model.Plss_a_out = Var(L, T, O, S, within = Reals)
model.Plss_b_out = Var(L, T, O, S, within = Reals)
model.Plss_c_out = Var(L, T, O, S, within = Reals)
model.Qlss_a_out = Var(L, T, O, S, within = Reals)
model.Qlss_b_out = Var(L, T, O, S, within = Reals)
model.Qlss_c_out = Var(L, T, O, S, within = Reals)

model.Ppcc_a_out = Var(N, T, O, S, within = Reals)
model.Ppcc_b_out = Var(N, T, O, S, within = Reals)
model.Ppcc_c_out = Var(N, T, O, S, within = Reals)
model.Qpcc_a_out = Var(N, T, O, S, within = Reals)
model.Qpcc_b_out = Var(N, T, O, S, within = Reals)
model.Qpcc_c_out = Var(N, T, O, S, within = Reals)
model.Ppcc_out =   Var(N, T, O, S, within = Reals)
model.Qpcc_out =   Var(N, T, O, S, within = Reals)

model.Ppcc_a_out_po = Var(N, T, O, S, within = NonNegativeReals)
model.Ppcc_b_out_po = Var(N, T, O, S, within = NonNegativeReals)
model.Ppcc_c_out_po = Var(N, T, O, S, within = NonNegativeReals)
model.Ppcc_a_out_ne = Var(N, T, O, S, within = NonNegativeReals)
model.Ppcc_b_out_ne = Var(N, T, O, S, within = NonNegativeReals)
model.Ppcc_c_out_ne = Var(N, T, O, S, within = NonNegativeReals)

model.PGa_out = Var(GD, T, O, S, within = NonNegativeReals)
model.PGb_out = Var(GD, T, O, S, within = NonNegativeReals)
model.PGc_out = Var(GD, T, O, S, within = NonNegativeReals)
model.QGa_out = Var(GD, T, O, S, within = NonNegativeReals)
model.QGb_out = Var(GD, T, O, S, within = NonNegativeReals)
model.QGc_out = Var(GD, T, O, S, within = NonNegativeReals)
model.PG_out =  Var(GD, T, O, S, within = NonNegativeReals)
model.QG_out =  Var(GD, T, O, S, within = NonNegativeReals)
model.oG_out =  Var(GD, T, O, S, domain = Binary)

# Power flow linearization variables with contingences
model.Pa_sqr_out = Var(L, T, O, S, within = Reals)
model.Pb_sqr_out = Var(L, T, O, S, within = Reals)
model.Pc_sqr_out = Var(L, T, O, S, within = Reals)
model.Qa_sqr_out = Var(L, T, O, S, within = Reals)
model.Qb_sqr_out = Var(L, T, O, S, within = Reals)
model.Qc_sqr_out = Var(L, T, O, S, within = Reals)

model.Pa_p_out = Var(L, T, O, S, within = NonNegativeReals)
model.Pa_n_out = Var(L, T, O, S, within = NonNegativeReals)
model.Pb_p_out = Var(L, T, O, S, within = NonNegativeReals)
model.Pb_n_out = Var(L, T, O, S, within = NonNegativeReals)
model.Pc_p_out = Var(L, T, O, S, within = NonNegativeReals)
model.Pc_n_out = Var(L, T, O, S, within = NonNegativeReals)
model.Qa_p_out = Var(L, T, O, S, within = NonNegativeReals)
model.Qa_n_out = Var(L, T, O, S, within = NonNegativeReals)
model.Qb_p_out = Var(L, T, O, S, within = NonNegativeReals)
model.Qb_n_out = Var(L, T, O, S, within = NonNegativeReals)
model.Qc_p_out = Var(L, T, O, S, within = NonNegativeReals)
model.Qc_n_out = Var(L, T, O, S, within = NonNegativeReals)

# Variáveis com Dp deveriam ser maiores ou iguais a zerO, mas ao inserir como NonNegativeReals o problema da infactível
model.Pa_Dp_out = Var(L, T, O, S, Y, within = NonNegativeReals)
model.Pb_Dp_out = Var(L, T, O, S, Y, within = NonNegativeReals)
model.Pc_Dp_out = Var(L, T, O, S, Y, within = NonNegativeReals)
model.Qa_Dp_out = Var(L, T, O, S, Y, within = NonNegativeReals)
model.Qb_Dp_out = Var(L, T, O, S, Y, within = NonNegativeReals)
model.Qc_Dp_out = Var(L, T, O, S, Y, within = NonNegativeReals)

# Linearization of PCC
model.Ppcc_sqr_out = Var(N, T, O, S, within = NonNegativeReals)
model.Qpcc_sqr_out = Var(N, T, O, S, within = NonNegativeReals)
model.Ppcc_p_out = Var(N, T, O, S, within = NonNegativeReals)
model.Ppcc_n_out = Var(N, T, O, S, within = NonNegativeReals)
model.Qpcc_n_out = Var(N, T, O, S, within = NonNegativeReals)
model.Qpcc_p_out = Var(N, T, O, S, within = NonNegativeReals)
model.Ppcc_Dp_out = Var(N, T, O, S, Y, within = NonNegativeReals)
model.Qpcc_Dp_out = Var(N, T, O, S, Y, within = NonNegativeReals)


# Voltage linearization variables

model.Va_sqr_out = Var(N, T, O, S, within = NonNegativeReals, bounds = (Vmin**2, Vmax**2))
model.Vb_sqr_out = Var(N, T, O, S, within = NonNegativeReals, bounds = (Vmin**2, Vmax**2))
model.Vc_sqr_out = Var(N, T, O, S, within = NonNegativeReals, bounds = (Vmin**2, Vmax**2))

model.xd =  Var(N, T, O, S,  domain = Binary)
model.xpv = Var(N, T, O, S, bounds = (0, 1))




    #### EV test
model.EEV       = Var(T, E, domain=NonNegativeReals)
model.PEV       = Var(T, E, domain=Reals)
model.PEV_c     = Var(T, E, domain=NonNegativeReals)
model.PEV_d     = Var(T, E, domain=NonNegativeReals)
model.PEV_c_lin = Var(T, E, C, domain=NonNegativeReals)
model.PEV_d_lin = Var(T, E, C, domain=NonNegativeReals)



model.gEV_c     = Var(T, E, domain=Binary)
model.gEV_d     = Var(T, E, domain=Binary)
model.aEV       = Var(T, E, C, domain=Binary)

model.PEVCS_a   = Var(T, C, domain=Reals)
model.PEVCS_b   = Var(T, C, domain=Reals)
model.PEVCS_c   = Var(T, C, domain=Reals)
model.PEVCS     = Var(T, C, domain=Reals)
    


################# ev constraints ##################
# def ev_energy_rule(model, t, e):
#     if t 

def alpha_ev_rule(model, t, e):
    ta = datetime.strptime(EV[e]["arrival"], '%H:%M')
    td = datetime.strptime(EV[e]["departure"], '%H:%M')
    to = datetime.strptime(t, '%H:%M')
    if to >= ta and to <= td:
        return sum(model.aEV[t, e, x, y] for x,y in C) <= 1
    else:
        return sum(model.aEV[t, e, x, y] for x,y in C) == 0
model.alpha_ev = Constraint(T, E, rule=alpha_ev_rule)

def alpha_charger_rule(model, t, x, y):
    return sum(model.aEV[t, e, x, y] for e in E) <= 1
model.alpha_charger = Constraint(T, C, rule=alpha_charger_rule)

def ev_charging_power_alpha_rule(model, t, e):
    return model.PEV_c[t, e] <= sum(EVCS[x]["connector"][y]["Pmaxc"] * model.aEV[t, e, x, y] for x,y in C)
model.ev_charging_power_alpha = Constraint(T, E, rule=ev_charging_power_alpha_rule)

def ev_discharging_power_alpha_rule(model, t, e):
    return model.PEV_d[t, e] <= sum(EVCS[x]["connector"][y]["Pmaxd"] * model.aEV[t, e, x, y] for x,y in C)
model.ev_discharging_power_alpha = Constraint(T, E, rule=ev_discharging_power_alpha_rule)

def ev_charging_power_rule(model, t, e):
    return model.PEV_c[t, e] <= model.gEV_c[t, e] * EV[e]["Pmaxc"]
model.ev_charging_power = Constraint(T, E, rule=ev_charging_power_rule)

def ev_discharging_power_rule(model, t, e):
    return model.PEV_d[t, e] <= model.gEV_d[t, e] * EV[e]["Pmaxd"]
model.ev_discharging_power = Constraint(T, E, rule=ev_discharging_power_rule)

def gamma_ev_charging_rule(model, t, e):
    return model.gEV_c[t, e] + model.gEV_d[t, e] <= 1
model.gamma_ev_charging = Constraint(T, E, rule=gamma_ev_charging_rule)

def ev_energy_rule(model, t, e):
    if t == T[1]:
        return model.EEV[t, e] == EV[e]["SoCini"] * EV[e]['Emax'] + model.PEV[t, e] * delta_t
    else:
        t0 = (datetime.strptime(t, '%H:%M') - timedelta(hours=delta_t)).strftime('%H:%M')
        return model.EEV[t, e] == model.EEV[t0, e] + model.PEV[t, e] * delta_t
model.ev_energy = Constraint(T, E, rule=ev_energy_rule)

def ev_total_power_rule(model, t, e):
    return model.PEV[t, e] == sum(model.PEV_c_lin * EVCS[x]["connector"][y]["efficiency"] for x, y in C) - \
        sum(model.PEV_d_lin / (EVCS[x]["connector"][y]["efficiency"]) for x, y in C)

# EV charging linearization
def ev_charging_power_linearization_rule_1(model, t, e, x, y):
    return model.PEV_c_lin[t, e, x, y] <= model.PEV_c[t, e]
model.ev_charging_power_linearization_1 = Constraint(T, E, C, rule=ev_charging_power_linearization_rule_1)

def ev_charging_power_linearization_rule_2(model, t, e, x, y):
    return model.PEV_c_lin[t, e, x, y] <= EVCS[x]["connector"][y]["Pmaxc"] * model.aEV[t, e, x, y]
model.ev_charging_power_linearization_2 = Constraint(T, E, C, rule=ev_charging_power_linearization_rule_2)

def ev_charging_power_linearization_rule_3(model, t, e, x, y):
    return model.PEV_c_lin[t, e, x, y] >= model.PEV_c[t, e] - EVCS[x]["connector"][y]["Pmaxc"] * (1 - model.aEV[t, e, x, y])
model.ev_charging_power_linearization_3 = Constraint(T, E, C, rule=ev_charging_power_linearization_rule_3)

# EV discharging linearization
def ev_discharging_power_linearization_rule_1(model, t, e, x, y):
    return model.PEV_d_lin[t, e, x, y] <= model.PEV_d[t, e]
model.ev_discharging_power_linearization_1 = Constraint(T, E, C, rule=ev_discharging_power_linearization_rule_1)

def ev_discharging_power_linearization_rule_2(model, t, e, x, y):
    return model.PEV_d_lin[t, e, x, y] <= EVCS[x]["connector"][y]["Pmaxd"] * model.aEV[t, e, x, y]
model.ev_discharging_power_linearization_2 = Constraint(T, E, C, rule=ev_discharging_power_linearization_rule_2)

def ev_discharging_power_linearization_rule_3(model, t, e, x, y):
    return model.PEV_d_lin[t, e, x, y] >= model.PEV_d[t, e] - EVCS[x]["connector"][y]["Pmaxd"] * (1 - model.aEV[t, e, x, y])
model.ev_discharging_power_linearization_3 = Constraint(T, E, C, rule=ev_discharging_power_linearization_rule_3)

# alpha switch constraint
def ev_switch_rule(model, t, e, x, y):
    ta = datetime.strptime(EV[e]["arrival"], '%H:%M')
    td = datetime.strptime(EV[e]["departure"], '%H:%M')
    t2 = datetime.strptime(t, '%H:%M')
    t1 = t2 - timedelta(hours=delta_t)
    if t2 > ta and t2 <= td:
        return model.aEV[t2.strftime('%H:%M'), e, x, y] >= model.aEV[t1.strftime('%H:%M'), e, x, y]
    else:
        return Constraint.Skip
model.ev_switch = Constraint(T, E, C, rule=ev_switch_rule)

# EVCS power constraint
def evcs_power_rule(model, t, x, y):
    return model.PEVCS[t, x, y] == sum(model.PEV_c_lin[t, e, x, y] for e in E)
model.evcs_power = Constraint(T, C, rule=evcs_power_rule)

# EVCS phase power constraint
def evcs_phase_power_rule(model, t, x, y):
    if ["a"] == EVCS[x]["phases"]:
        return model.PEVCS_a[t, x, y] == model.PEVCS[t, x, y]
    elif ["b"] == EVCS[x]["phases"]:
        return model.PEVCS_b[t, x, y] == model.PEVCS[t, x, y]
    elif ["c"] == EVCS[x]["phases"]:
        return model.PEVCS_c[t, x, y] == model.PEVCS[t, x, y]
    elif ["a", "b"] == EVCS[x]["phases"]:
        return model.PEVCS_a[t, x, y] + model.PEVCS_b[t, x, y] == model.PEVCS[t, x, y]
    elif ["a", "c"] == EVCS[x]["phases"]:
        return model.PEVCS_a[t, x, y] + model.PEVCS_c[t, x, y] == model.PEVCS[t, x, y]
    elif ["b", "c"] == EVCS[x]["phases"]:
        return model.PEVCS_b[t, x, y] + model.PEVCS_c[t, x, y] == model.PEVCS[t, x, y]
    else:
        return model.PEVCS_a[t, x, y] + model.PEVCS_b[t, x, y] + model.PEVCS_c[t, x, y] == model.PEVCS[t, x, y]
model.evcs_phase_power = Constraint(T, C, rule=evcs_phase_power_rule)



def evcs_phase_balance_not_in_rule(model, t, x, y, p):
    if p == "a" and p not in EVCS[x]["phases"]:
        return model.PEVCS_a[t, x, y] == 0
    elif p == "b" and p not in EVCS[x]["phases"]:
        return model.PEVCS_b[t, x, y] == 0
    elif p == "c" and p not in EVCS[x]["phases"]:
        return model.PEVCS_c[t, x, y] == 0
    else:
        return Constraint.Skip
model.evcs_phase_balance_not_in = Constraint(T, C, ["a", "b", "c"], rule=evcs_phase_balance_not_in_rule)


def evcs_two_phases_balance_rule(model, t, x, y):
    if ["a", "b"] == EVCS[x]["phases"]:
        return model.PEVCS_a[t, x, y] == model.PEVCS_b[t, x, y]
    elif ["a", "c"] == EVCS[x]["phases"]:
        return model.PEVCS_a[t, x, y] == model.PEVCS_c[t, x, y]
    elif ["b", "c"] == EVCS[x]["phases"]:
        return model.PEVCS_b[t, x, y] == model.PEVCS_c[t, x, y]
    else:
        return Constraint.Skip
model.evcs_two_phases_balance = Constraint(T, C, rule=evcs_two_phases_balance_rule)

def evcs_three_phases_ab_balance_rule(model, t, x, y):
    if ["a", "b", "c"] == EVCS[x]["phases"]:
        return model.PEVCS_a[t, x, y] == model.PEVCS_b[t, x, y]
    else:
        return Constraint.Skip
model.evcs_three_phases_ab_balance = Constraint(T, C, rule=evcs_three_phases_ab_balance_rule)

def evcs_three_phases_ac_balance_rule(model, t, x, y):
    if ["a", "b", "c"] == EVCS[x]["phases"]:
        return model.PEVCS_a[t, x, y] == model.PEVCS_c[t, x, y]
    else:
        return Constraint.Skip
model.evcs_three_phases_ac_balance = Constraint(T, C, rule=evcs_three_phases_ac_balance_rule)

def evcs_three_phases_bc_balance_rule(model, t, x, y):
    if ["a", "b", "c"] == EVCS[x]["phases"]:
        return model.PEVCS_b[t, x, y] == model.PEVCS_c[t, x, y]
    else:
        return Constraint.Skip
model.evcs_three_phases_bc_balance = Constraint(T, C, rule=evcs_three_phases_bc_balance_rule)
        

def ev_departure_energy_rule(model, t, e):
    if t == EV[e]["departure"]:
        return model.EEV[t, e] == EV[e]["Emax"]
    elif t == EV[e]["arrival"]:
        return model.EEV[t, e] == EV[e]["SoCini"] * EV[e]["Emax"]
    else:
        return model.EEV[t, e] <= EV[e]["Emax"]
model.ev_departure_energy = Constraint(T, E, rule=ev_departure_energy_rule)

# Modelo Multi-objective e-constraint

if len(O) >= 1 :
    FO1 = (sum(Prob[s]*(0.01/len(O) * (sum(cEDS[t] * delta_t * (model.Ppcc_a_out_po[i, t, o, s] + model.Ppcc_b_out_po[i, t, o, s] + model.Ppcc_c_out_po[i, t, o, s]) for (i, t, o, s) in List_NTOS) + 
        sum([cost_PG[i] * delta_t * model.PG_out[i,t,o, s] for (i,t,o,s) in List_GDTOS]) + 
        sum([delta_t * alpha_c[i] * sd[s] * (PDa[('3',t)]+PDb[('3',t)]+PDc[('3',t)]) * (1-model.xd['3',t,o,s]) for (i,t,o,s) in List_NTOS]))) + 
        (0.99 * sum(cEDS[t] * delta_t * (model.Ppcc_a_po[i, t,s] + model.Ppcc_b_po[i, t,s] + model.Ppcc_c_po[i, t,s]) for (i, t,s) in List_NTS) + 
        sum(cost_PG[i] * delta_t * model.PG[i, t,s] for (i, t,s) in List_GDTS)) for s in S))
else :
    FO1 = (sum(Prob[s]*(0.01/1000000 * (sum(cEDS[t] * delta_t * (model.Ppcc_a_out_po[i, t, o, s] + model.Ppcc_b_out_po[i, t, o, s] + model.Ppcc_c_out_po[i, t, o, s]) for (i, t, o, s) in List_NTOS) + 
        sum([delta_t * alpha_c[i] * sd[s] * (PDa[(i,t)]+PDb[(i,t)]+PDc[(i,t)]) * (1-model.xd[i,t,o,s]) for (i,t,o,s) in List_NTOS]))) +
        (0.99 * sum(cEDS[t] * delta_t * (model.Ppcc_a_po[i, t,s] + model.Ppcc_b_po[i, t,s] + model.Ppcc_c_po[i, t,s]) for (i, t,s) in List_NTS)) for s in S))
model.objective_1 = Objective(expr=FO1)

# --------------------- Constraints --------------------------------------------
# --------------------- Without Contingences------------------------------------

#-----------------------New constraint-----------------------------------------

def active_power_positive_a_rule(model, i, t, s):
    return (model.Ppcc_a[i,t,s] - model.Ppcc_a_po[i,t,s] + model.Ppcc_a_ne[i,t,s] == 0)
model.active_power_positive_a = Constraint(List_NTS, rule=active_power_positive_a_rule)

def active_power_positive_b_rule(model, i, t, s):
    return (model.Ppcc_b[i,t,s] - model.Ppcc_b_po[i,t,s] + model.Ppcc_b_ne[i,t,s] == 0)
model.active_power_positive_b = Constraint(List_NTS, rule=active_power_positive_b_rule)

def active_power_positive_c_rule(model, i, t, s):
    return (model.Ppcc_c[i,t,s] - model.Ppcc_c_po[i,t,s] + model.Ppcc_c_ne[i,t,s] == 0)
model.active_power_positive_c = Constraint(List_NTS, rule=active_power_positive_c_rule)


# ---------------------- Active losses -----------------------------------------
def active_losses_a_rule(model, i, j, t, s):
    return (
        (1 / (Va_0[i, t, s] * Va_0[i, t, s])) * 
        (Raa_p[i, j] * model.Pa_sqr[i, j, t, s] + 
        Raa_p[i, j] * model.Qa_sqr[i, j, t, s] - 
        Xaa_p[i, j] * Pa_0[i, j, t, s] * model.Qa[i, j, t, s] + 
        Xaa_p[i, j] * Qa_0[i, j, t, s] * model.Pa[i, j, t, s]) +
        (1 / (Va_0[i, t, s] * Vb_0[i, t, s])) * 
        (Rab_p[i, j] * Pb_0[i, j, t, s] * model.Pa[i, j, t, s] + 
        Rab_p[i, j] * Qb_0[i, j, t, s] * model.Qa[i, j, t, s] - 
        Xab_p[i, j] * Pb_0[i, j, t, s] * model.Qa[i, j, t, s] + 
        Xab_p[i, j] * Qb_0[i, j, t, s] * model.Pa[i, j, t, s]) +
        (1 / (Va_0[i, t, s] * Vc_0[i, t, s])) * 
        (Rac_p[i, j] * Pc_0[i, j, t, s] * model.Pa[i, j, t, s] + 
        Rac_p[i, j] * Qc_0[i, j, t, s] * model.Qa[i, j, t, s] - 
        Xac_p[i, j] * Pc_0[i, j, t, s] * model.Qa[i, j, t, s] + 
        Xac_p[i, j] * Qc_0[i, j, t, s] * model.Pa[i, j, t, s]) == model.Plss_a[i, j, t, s]
        )
model.active_losses_a = Constraint(List_LTS, rule=active_losses_a_rule)

def active_losses_b_rule(model, i, j, t, s):
    return (
        (1 / (Vb_0[i, t, s] * Va_0[i, t, s])) * 
        (Rba_p[i, j] * Pa_0[i, j, t, s] * model.Pb[i, j, t, s] + 
        Rba_p[i, j] * Qa_0[i, j, t, s] * model.Qb[i, j, t, s] - 
        Xba_p[i, j] * Pa_0[i, j, t, s] * model.Qb[i, j, t, s] + 
        Xba_p[i, j] * Qa_0[i, j, t, s] * model.Pb[i, j, t, s]) +
        (1 / (Vb_0[i, t, s] * Vb_0[i, t, s])) * 
        (Rbb_p[i, j] * model.Pb_sqr[i, j, t, s]  + 
        Rbb_p[i, j] * model.Qb_sqr[i, j, t, s]  - 
        Xbb_p[i, j] * Pb_0[i, j, t, s] * model.Qb[i, j, t, s] + 
        Xbb_p[i, j] * Qb_0[i, j, t, s] * model.Pb[i, j, t, s]) +
        (1 / (Vb_0[i, t, s] * Vc_0[i, t, s])) * 
        (Rbc_p[i, j] * Pc_0[i, j, t, s] * model.Pb[i, j, t, s] + 
        Rbc_p[i, j] * Qc_0[i, j, t, s] * model.Qb[i, j, t, s] - 
        Xbc_p[i, j] * Pc_0[i, j, t, s] * model.Qb[i, j, t, s] + 
        Xbc_p[i, j] * Qc_0[i, j, t, s] * model.Pb[i, j, t, s]) == model.Plss_b[i, j, t, s])
model.active_losses_b = Constraint(List_LTS, rule=active_losses_b_rule)


def active_losses_c_rule(model, i, j, t, s):
    return (
        (1 / (Vc_0[i, t, s] * Va_0[i, t, s])) * 
        (Rca_p[i, j] * Pa_0[i, j, t, s] * model.Pc[i, j, t, s] + 
        Rca_p[i, j] * Qa_0[i, j, t, s] * model.Qc[i, j, t, s] - 
        Xca_p[i, j] * Pa_0[i, j, t, s] * model.Qc[i, j, t, s] + 
        Xca_p[i, j] * Qa_0[i, j, t, s] * model.Pc[i, j, t, s]) +
        (1 / (Vc_0[i, t, s] * Vb_0[i, t, s])) * 
        (Rcb_p[i, j] * Pb_0[i, j, t, s] * model.Pc[i, j, t, s] + 
        Rcb_p[i, j] * Qb_0[i, j, t, s] * model.Qc[i, j, t, s] - 
        Xcb_p[i, j] * Pb_0[i, j, t, s] * model.Qc[i, j, t, s] + 
        Xcb_p[i, j] * Qb_0[i, j, t, s] * model.Pc[i, j, t, s]) +
        (1 / (Vc_0[i, t, s] * Vc_0[i, t, s])) * 
        (Rcc_p[i, j] * model.Pc_sqr[i, j, t, s]  + 
        Rcc_p[i, j] * model.Qc_sqr[i, j, t, s]  - 
        Xcc_p[i, j] * Pc_0[i, j, t, s] * model.Qc[i, j, t, s] + 
        Xcc_p[i, j] * Qc_0[i, j, t, s] * model.Pc[i, j, t, s]) == model.Plss_c[i, j, t, s])
model.active_losses_c = Constraint(List_LTS, rule=active_losses_c_rule)    

# Reactive losses ----------------------------------------------------------------
def reactive_losses_a_rule(model, i, j, t, s):
    return (
        (1 / (Va_0[i, t, s] * Va_0[i, t, s])) * 
        (Raa_p[i, j] * Pa_0[i, j, t, s] * model.Qa[i, j, t, s] - 
        Raa_p[i, j] * Qa_0[i, j, t, s] * model.Pa[i, j, t, s] + 
        Xaa_p[i, j] * model.Pa_sqr[i, j, t, s]  + 
        Xaa_p[i, j] * model.Qa_sqr[i, j, t, s] ) +
        (1 / (Va_0[i, t, s] * Vb_0[i, t, s])) * 
        (Rab_p[i, j] * Pb_0[i, j, t, s] * model.Qa[i, j, t, s] - 
        Rab_p[i, j] * Qb_0[i, j, t, s] * model.Pa[i, j, t, s] + 
        Xab_p[i, j] * Pb_0[i, j, t, s] * model.Pa[i, j, t, s] + 
        Xab_p[i, j] * Qb_0[i, j, t, s] * model.Qa[i, j, t, s]) +
        (1 / (Va_0[i, t, s] * Vc_0[i, t, s])) * 
        (Rac_p[i, j] * Pc_0[i, j, t, s] * model.Qa[i, j, t, s] - 
        Rac_p[i, j] * Qc_0[i, j, t, s] * model.Pa[i, j, t, s] + 
        Xac_p[i, j] * Pc_0[i, j, t, s] * model.Pa[i, j, t, s] + 
        Xac_p[i, j] * Qc_0[i, j, t, s] * model.Qa[i, j, t, s]) == model.Qlss_a[i, j, t, s])
model.reactive_losses_a = Constraint(List_LTS, rule=reactive_losses_a_rule)

def reactive_losses_b_rule(model, i, j, t, s):
    return (
        (1 / (Vb_0[i, t, s] * Va_0[i, t, s])) * 
        (Rba_p[i, j] * Pa_0[i, j, t, s] * model.Qb[i, j, t, s] - 
        Rba_p[i, j] * Qa_0[i, j, t, s] * model.Pb[i, j, t, s] + 
        Xba_p[i, j] * Pa_0[i, j, t, s] * model.Pb[i, j, t, s] + 
        Xba_p[i, j] * Qa_0[i, j, t, s] * model.Qb[i, j, t, s]) +
        (1 / (Vb_0[i, t, s] * Vb_0[i, t, s])) * 
        (Rbb_p[i, j] * Pb_0[i, j, t, s] * model.Qb[i, j, t, s] - 
        Rbb_p[i, j] * Qb_0[i, j, t, s] * model.Pb[i, j, t, s] + 
        Xbb_p[i, j] * model.Pb_sqr[i, j, t, s]  + 
        Xbb_p[i, j] * model.Qb_sqr[i, j, t, s] ) +
        (1 / (Vb_0[i, t, s] * Vc_0[i, t, s])) * 
        (Rbc_p[i, j] * Pc_0[i, j, t, s] * model.Qb[i, j, t, s] - 
        Rbc_p[i, j] * Qc_0[i, j, t, s] * model.Pb[i, j, t, s] + 
        Xbc_p[i, j] * Pc_0[i, j, t, s] * model.Pb[i, j, t, s] + 
        Xbc_p[i, j] * Qc_0[i, j, t, s] * model.Qb[i, j, t, s]) == model.Qlss_b[i, j, t, s])

model.reactive_losses_b = Constraint(List_LTS, rule= reactive_losses_b_rule)

def reactive_losses_c_rule(model, i, j, t, s):
    return (
        (1 / (Vc_0[i, t, s] * Va_0[i, t, s])) * 
        (Rca_p[i, j] * Pa_0[i, j, t, s] * model.Qc[i, j, t, s] - 
        Rca_p[i, j] * Qa_0[i, j, t, s] * model.Pc[i, j, t, s] + 
        Xca_p[i, j] * Pa_0[i, j, t, s] * model.Pc[i, j, t, s] + 
        Xca_p[i, j] * Qa_0[i, j, t, s] * model.Qc[i, j, t, s]) +
        (1 / (Vc_0[i, t, s] * Vb_0[i, t, s])) * 
        (Rcb_p[i, j] * Pb_0[i, j, t, s] * model.Qc[i, j, t, s] - 
        Rcb_p[i, j] * Qb_0[i, j, t, s] * model.Pc[i, j, t, s] + 
        Xcb_p[i, j] * Pb_0[i, j, t, s] * model.Pc[i, j, t, s] + 
        Xcb_p[i, j] * Qb_0[i, j, t, s] * model.Qc[i, j, t, s]) +
        (1 / (Vc_0[i, t, s] * Vc_0[i, t, s])) * 
        (Rcc_p[i, j] * Pc_0[i, j, t, s] * model.Qc[i, j, t, s] - 
        Rcc_p[i, j] * Qc_0[i, j, t, s] * model.Pc[i, j, t, s] + 
        Xcc_p[i, j] * model.Pc_sqr[i, j, t, s]  + 
        Xcc_p[i, j] * model.Qc_sqr[i, j, t, s] ) == model.Qlss_c[i, j, t, s])

model.reactive_losses_c = Constraint(List_LTS, rule= reactive_losses_c_rule)

# Active Power Flow with EV -------------------------------------------------------------
def active_power_balance_rule_a(model, i, t, s):
    return (
        sum(model.Pa[a, j, t, s]*df[(i,a,j)] for (a,j) in L) -
        sum(model.Plss_a[a, j, t, s]*p[(i,a,j)] for (a,j) in L) +
        model.Ppcc_a[i, t, s] +
        sum(model.PGa[a, t, s] for a in dict_nos_gd[i]) +
        sum(model.PB_dis_a[a, t] for a in dict_nos_bs[i]) -
        sum(model.PB_ch_a[a, t] for a in dict_nos_bs[i]) -
        
        
        sum(model.PEVCS_a[t, (x,y)] for (x,y) in C if EVCS[x]["node"] == i and 'a' in EVCS[x]["phases"]) -
        
        
        PDa[(i,t)]*sd[s] + PVa[(i,t)]*spv[s] == 0
    )

model.active_power_balance_a = Constraint(List_NTS, rule=active_power_balance_rule_a)

def active_power_balance_rule_b(model, i, t, s):
    return (
        sum(model.Pb[a, j, t, s]*df[(i,a,j)] for (a,j) in L) -
        sum(model.Plss_b[a, j, t, s]*p[(i,a,j)] for (a,j) in L) +
        model.Ppcc_b[i, t, s] +
        sum(model.PGb[a, t, s] for a in dict_nos_gd[i]) +
        sum(model.PB_dis_b[a, t] for a in dict_nos_bs[i]) -
        sum(model.PB_ch_b[a, t] for a in dict_nos_bs[i]) -
        sum(model.PEVCS_b[t, (x,y)] for (x,y) in C if EVCS[x]["node"] == i and 'b' in EVCS[x]["phases"]) -
        PDb[(i,t)]*sd[s] + PVb[(i,t)]*spv[s] == 0)

model.active_power_balance_b = Constraint(List_NTS, rule=active_power_balance_rule_b)

def active_power_balance_rule_c(model, i, t, s):
    return (
        sum(model.Pc[a, j, t, s]*df[(i,a,j)] for (a,j) in L) -
        sum(model.Plss_c[a, j, t, s]*p[(i,a,j)] for (a,j) in L) +
        model.Ppcc_c[i, t, s] +
        sum(model.PGc[a, t, s] for a in dict_nos_gd[i]) +
        sum(model.PB_dis_c[a, t] for a in dict_nos_bs[i]) -
        sum(model.PB_ch_c[a, t] for a in dict_nos_bs[i]) -
        sum(model.PEVCS_c[t, (x,y)] for (x,y) in C if EVCS[x]["node"] == i and 'c' in EVCS[x]["phases"]) -
        PDc[(i,t)]*sd[s] + PVc[(i,t)]*spv[s] == 0)
model.active_power_balance_c = Constraint(List_NTS, rule=active_power_balance_rule_c)

# Reactive Power Flow ----------------------------------------------------------------
def reactive_power_balance_rule_a(model, i, t, s):
    return (
        sum(model.Qa[a, j, t, s]*df[(i,a,j)] for (a,j) in L) -
        sum(model.Qlss_a[a, j, t, s]*p[(i,a,j)] for (a,j) in L) +
        model.Qpcc_a[i, t, s] +
        sum(model.QGa[a, t, s] for a in dict_nos_gd[i]) -
        QDa[(i,t)]*sd[s] == 0)
model.reactive_power_balance_a = Constraint(List_NTS, rule=reactive_power_balance_rule_a)

def reactive_power_balance_rule_b(model, i, t, s):
    return (
        sum(model.Qb[a, j, t, s]*df[(i,a,j)] for (a,j) in L) -
        sum(model.Qlss_b[a, j, t, s]*p[(i,a,j)] for (a,j) in L) +
        model.Qpcc_b[i, t, s] +
        sum(model.QGb[a, t, s] for a in dict_nos_gd[i]) -
        QDb[(i,t)]*sd[s] == 0)
model.reactive_power_balance_b = Constraint(List_NTS, rule=reactive_power_balance_rule_b)

def reactive_power_balance_rule_c(model, i, t, s):
    return (
        sum(model.Qc[a, j, t, s]*df[(i,a,j)] for (a,j) in L) -
        sum(model.Qlss_c[a, j, t, s]*p[(i,a,j)] for (a,j) in L) +
        model.Qpcc_c[i, t, s] +
        sum(model.QGc[a, t, s] for a in dict_nos_gd[i]) -
        QDc[(i,t)]*sd[s] == 0)
model.reactive_power_balance_c = Constraint(List_NTS, rule=reactive_power_balance_rule_c)

# Voltage Droop in the Lines ----------------------------------------------------------------
def voltage_droop_rule_a(model, i, j, t, s):
    return((2*(Raa_p[i,j]*model.Pa[i, j, t, s] + Xaa_p[i,j]*model.Qa[i, j, t, s])) + 
        (2*(Rab_p[i,j]*model.Pb[i, j, t, s] + Xab_p[i,j]*model.Qb[i, j, t, s])) + 
        (2*(Rac_p[i,j]*model.Pc[i, j, t, s] + Xac_p[i,j]*model.Qc[i, j, t, s])) -
        (1/Va_0[i, t, s]**2) * ((Raa_p[i,j]**2 + Xaa_p[i,j]**2) * (model.Pa_sqr[i, j, t, s] + model.Qa_sqr[i, j, t, s])) ==
        model.Va_sqr[i, t, s] - model.Va_sqr[j, t, s])
model.voltage_droop_a = Constraint(List_LTS, rule=voltage_droop_rule_a)

def voltage_droop_rule_b(model, i, j, t, s):
    return((2*(Rba_p[i,j]*model.Pa[i, j, t, s] + Xba_p[i,j]*model.Qa[i, j, t, s])) + 
        (2*(Rbb_p[i,j]*model.Pb[i, j, t, s] + Xbb_p[i,j]*model.Qb[i, j, t, s])) + 
        (2*(Rbc_p[i,j]*model.Pc[i, j, t, s] + Xbc_p[i,j]*model.Qc[i, j, t, s])) -
        (1/Vb_0[i, t, s]**2) * ((Rbb_p[i,j]**2 + Xbb_p[i,j]**2) * (model.Pb_sqr[i, j, t, s] + model.Qb_sqr[i, j, t, s])) ==
        model.Vb_sqr[i, t, s] - model.Vb_sqr[j, t, s])
model.voltage_droop_b = Constraint(List_LTS, rule=voltage_droop_rule_b)

def voltage_droop_rule_c(model, i, j, t, s):
    return((2*(Rca_p[i,j]*model.Pa[i, j, t, s] + Xca_p[i,j]*model.Qa[i, j, t, s])) + 
        (2*(Rcb_p[i,j]*model.Pb[i, j, t, s] + Xcb_p[i,j]*model.Qb[i, j, t, s])) + 
        (2*(Rcc_p[i,j]*model.Pc[i, j, t, s] + Xcc_p[i,j]*model.Qc[i, j, t, s])) -
        (1/Vc_0[i, t, s]**2) * ((Rcc_p[i,j]**2 + Xcc_p[i,j]**2) * (model.Pc_sqr[i, j, t, s] + model.Qc_sqr[i, j, t, s])) ==
        model.Vc_sqr[i, t, s] - model.Vc_sqr[j, t, s])
model.voltage_droop_c = Constraint(List_LTS, rule= voltage_droop_rule_c)

# Constrain Current Limits -------------------------------------------------------------
def current_limits_rule_a(model, i, j, t, s):
    return((model.Pa_sqr[i, j, t, s] + model.Qa_sqr[i, j, t, s]) <= Imax[i,j]**2 * (model.Va_sqr[i, t, s]))
model.current_limits_a = Constraint(List_LTS, rule=current_limits_rule_a)

def current_limits_rule_b(model, i, j, t, s):
    return((model.Pb_sqr[i, j, t, s] + model.Qb_sqr[i, j, t, s]) <= Imax[i,j]**2 * (model.Vb_sqr[i, t, s]))
model.current_limits_b = Constraint(List_LTS, rule=current_limits_rule_b)

def current_limits_rule_c(model, i, j, t, s):
    return((model.Pc_sqr[i, j, t, s] + model.Qc_sqr[i, j, t, s]) <= Imax[i,j]**2 * (model.Vc_sqr[i, t, s]))
model.current_limits_c = Constraint(List_LTS, rule=current_limits_rule_c)

# Active power linearization constraints
def pa_calculation_rule(model, i, j, t, s):
    return( model.Pa_sqr[i, j, t, s] - sum(S_ms[i,j,y] * model.Pa_Dp[i, j, t, s, y] for y in Y) == 0)
model.Pa_calculation = Constraint(List_LTS, rule=pa_calculation_rule)

def pb_calculation_rule(model, i, j, t, s):
    return( model.Pb_sqr[i, j, t, s] - sum(S_ms[i,j,y] * model.Pb_Dp[i, j, t, s, y] for y in Y) == 0)
model.Pb_calculation = Constraint(List_LTS, rule=pb_calculation_rule)

def pc_calculation_rule(model, i, j, t, s):
    return( model.Pc_sqr[i, j, t, s] - sum(S_ms[i,j,y] * model.Pc_Dp[i, j, t, s, y] for y in Y) == 0)
model.Pc_calculation = Constraint(List_LTS, rule=pc_calculation_rule)

# Reactive power linearization constraints
def qa_calculation_rule(model, i, j, t, s):
    return( model.Qa_sqr[i, j, t, s] - sum(S_ms[i,j,y] * model.Qa_Dp[i, j, t, s, y] for y in Y) == 0)
model.Qa_calculation = Constraint(List_LTS, rule=qa_calculation_rule)

def qb_calculation_rule(model, i, j, t, s):
    return( model.Qb_sqr[i, j, t, s] - sum(S_ms[i,j,y] * model.Qb_Dp[i, j, t, s, y] for y in Y) == 0)
model.Qb_calculation = Constraint(List_LTS, rule=qb_calculation_rule)

def qc_calculation_rule(model, i, j, t, s):
    return( model.Qc_sqr[i, j, t, s] - sum(S_ms[i,j,y] * model.Qc_Dp[i, j, t, s, y] for y in Y) == 0)
model.Qc_calculation = Constraint(List_LTS, rule=qc_calculation_rule)

# Linearizations variables
def pa_p_rule(model, i, j, t, s):
    return( model.Pa_p[i, j, t, s] - model.Pa_n[i, j, t, s] - model.Pa[i, j, t, s] == 0)
model.Pa_p_constraint = Constraint(List_LTS, rule=pa_p_rule)

def pb_p_rule(model, i, j, t, s):
    return( model.Pb_p[i, j, t, s] - model.Pb_n[i, j, t, s] - model.Pb[i, j, t, s] == 0)
model.Pb_p_constraint = Constraint(List_LTS, rule=pb_p_rule)

def pc_p_rule(model, i, j, t, s):
    return( model.Pc_p[i, j, t, s] - model.Pc_n[i, j, t, s] - model.Pc[i, j, t, s] == 0)
model.Pc_p_constraint = Constraint(List_LTS, rule=pc_p_rule)

def qa_p_rule(model, i, j, t, s):
    return( model.Qa_p[i, j, t, s] - model.Qa_n[i, j, t, s] - model.Qa[i, j, t, s] == 0)
model.Qa_p_constraint = Constraint(List_LTS, rule=qa_p_rule)

def qb_p_rule(model, i, j, t, s):
    return( model.Qb_p[i, j, t, s] - model.Qb_n[i, j, t, s] - model.Qb[i, j, t, s] == 0)
model.Qb_p_constraint = Constraint(List_LTS, rule=qb_p_rule)

def qc_p_rule(model, i, j, t, s):
    return( model.Qc_p[i, j, t, s] - model.Qc_n[i, j, t, s] - model.Qc[i, j, t, s] == 0)
model.Qc_p_constraint = Constraint(List_LTS, rule=qc_p_rule)

def pa_abs_rule(model, i, j, t, s):
    return( model.Pa_p[i, j, t, s] + model.Pa_n[i, j, t, s] - sum(model.Pa_Dp[i, j, t, s, y] for y in Y) == 0)
model.pa_abs = Constraint(List_LTS, rule=pa_abs_rule)

def pb_abs_rule(model, i, j, t, s):
    return( model.Pb_p[i, j, t, s] + model.Pb_n[i, j, t, s] - sum(model.Pb_Dp[i, j, t, s, y] for y in Y) == 0)
model.pb_abs = Constraint(List_LTS, rule=pb_abs_rule)

def pc_abs_rule(model, i, j, t, s):
    return( model.Pc_p[i, j, t, s] + model.Pc_n[i, j, t, s] - sum(model.Pc_Dp[i, j, t, s, y] for y in Y) == 0)
model.pc_abs = Constraint(List_LTS, rule=pc_abs_rule)

def qa_abs_rule(model, i, j, t, s):
    return( model.Qa_p[i, j, t, s] + model.Qa_n[i, j, t, s] - sum(model.Qa_Dp[i, j, t, s, y] for y in Y) == 0)
model.qa_abs = Constraint(List_LTS, rule=qa_abs_rule)

def qb_abs_rule(model, i, j, t, s):
    return( model.Qb_p[i, j, t, s] + model.Qb_n[i, j, t, s] - sum(model.Qb_Dp[i, j, t, s, y] for y in Y) == 0)
model.qb_abs = Constraint(List_LTS, rule=qb_abs_rule)

def qc_abs_rule(model, i, j, t, s):
    return( model.Qc_p[i, j, t, s] + model.Qc_n[i, j, t, s] - sum(model.Qc_Dp[i, j, t, s, y] for y in Y) == 0)
model.qc_abs = Constraint(List_LTS, rule=qc_abs_rule)

def pa_limits_rule(model, i, j, t, s, y):
    return( model.Pa_Dp[i, j, t, s, y] <= S_Dp_max[i,j])
model.pa_limits = Constraint(List_LTSY, rule=pa_limits_rule)

def pb_limits_rule(model, i, j, t, s, y):
    return( model.Pb_Dp[i, j, t, s, y] <= S_Dp_max[i,j])
model.pb_limits = Constraint(List_LTSY, rule=pb_limits_rule)

def pc_limits_rule(model, i, j, t, s, y):
    return( model.Pc_Dp[i, j, t, s, y] <= S_Dp_max[i,j])
model.pc_limits = Constraint(List_LTSY, rule=pc_limits_rule)

def qa_limits_rule(model, i, j, t, s, y):
    return( model.Qa_Dp[i, j, t, s, y] <= S_Dp_max[i,j])
model.qa_limits = Constraint(List_LTSY, rule=qa_limits_rule)

def qb_limits_rule(model, i, j, t, s, y):
    return( model.Qb_Dp[i, j, t, s, y] <= S_Dp_max[i,j])
model.qb_limits = Constraint(List_LTSY, rule=qb_limits_rule)

def qc_limits_rule(model, i, j, t, s, y):
    return( model.Qc_Dp[i, j, t, s, y] <= S_Dp_max[i,j])
model.qc_limits = Constraint(List_LTSY, rule=qc_limits_rule)

# PCC constraints ---------------------------------------------------------
def ative_power_pcc_rule(model, i, t, s):
    return(model.Ppcc[i, t, s] - model.Ppcc_a[i, t, s] - model.Ppcc_b[i, t, s] - model.Ppcc_c[i, t, s] == 0)
model.ative_power_pcc = Constraint(List_NTS, rule=ative_power_pcc_rule)

def reative_power_pcc_rule(model, i, t, s):
    return(model.Qpcc[i, t, s] - model.Qpcc_a[i, t, s] - model.Qpcc_b[i, t, s] - model.Qpcc_c[i, t, s] == 0)
model.reative_power_pcc = Constraint(List_NTS, rule=reative_power_pcc_rule)

# Apparent power --------------------------------------------------
def apparent_power_pcc_rule(model, i, t, s):
    return(model.Ppcc_sqr[i, t, s] + model.Qpcc_sqr[i, t, s] <= Smax[i]**2)
model.apparent_power_pcc = Constraint(List_NTS, rule=apparent_power_pcc_rule)

# PCC piecewise linearization constraints ------------------------------
def ppcc_calculation_rule(model, i, t, s):
    return( model.Ppcc_sqr[i, t, s] - sum(Spcc_ms[i,y] * model.Ppcc_Dp[i, t, s, y] for y in Y) == 0)
model.Ppcc_calculation = Constraint(List_NTS, rule=ppcc_calculation_rule)

def Qpcc_calculation_rule(model, i, t, s):
    return( model.Qpcc_sqr[i, t, s] - sum(Spcc_ms[i,y] * model.Qpcc_Dp[i, t, s, y] for y in Y) == 0)
model.Qpcc_calculation = Constraint(List_NTS, rule=Qpcc_calculation_rule)

def ppcc_p_rule(model, i, t, s):
    return( model.Ppcc_p[i, t, s] - model.Ppcc_n[i, t, s] - model.Ppcc[i, t, s] == 0)
model.Ppcc_p_constraint = Constraint(List_NTS, rule=ppcc_p_rule)

def qpcc_p_rule(model, i, t, s):
    return( model.Qpcc_p[i, t, s] - model.Qpcc_n[i, t, s] - model.Qpcc[i, t, s] == 0)
model.Qpcc_p_constraint = Constraint(List_NTS, rule=qpcc_p_rule)

def ppcc_abs_rule(model, i, t, s):
    return( model.Ppcc_p[i, t, s] + model.Ppcc_n[i, t, s] - sum(model.Ppcc_Dp[i, t, s, y] for y in Y) == 0)
model.ppcc_abs = Constraint(List_NTS, rule=ppcc_abs_rule)

def qpcc_abs_rule(model, i, t, s):
    return( model.Qpcc_p[i, t, s] + model.Qpcc_n[i, t, s] - sum(model.Qpcc_Dp[i, t, s, y] for y in Y) == 0)
model.qpcc_abs = Constraint(List_NTS, rule=qpcc_abs_rule)

# PCC limits --------------------------------------------------------
def ppcc_limits_rule(model, i, t, s, y):
    return( model.Ppcc_Dp[i, t, s, y] <= Spcc_Dp_max[i])
model.ppcc_limits = Constraint(List_NTSY, rule=ppcc_limits_rule)

def qpcc_limits_rule(model, i, t, s, y):
    return( model.Qpcc_Dp[i, t, s, y] <= Spcc_Dp_max[i])
model.qpcc_limits = Constraint(List_NTSY, rule=qpcc_limits_rule)        

# Genset ----------------------------------------------------------------
def genset_power_rule(model, i, t, s):
    return(model.PGa[i, t, s] + model.PGb[i, t, s] + model.PGc[i, t, s] == model.PG[i, t, s])
model.genset_power_active = Constraint(List_GDTS, rule=genset_power_rule)

def genset_power_reactive_rule(model, i, t, s):
    return(model.QGa[i, t, s] + model.QGb[i, t, s] + model.QGc[i, t, s] == model.QG[i, t, s])
model.genset_power_reactive = Constraint(List_GDTS, rule=genset_power_reactive_rule)

def genset_power_active_limits_rule_1(model, i, t, s):
    return(model.PG[i, t, s] >= PG_min[i])
model.genset_power_active_limits_1 = Constraint(List_GDTS, rule=genset_power_active_limits_rule_1)

def genset_power_active_limits_rule_2(model, i, t, s):
    return(model.PG[i, t, s] <= PG_max[i])
model.genset_power_active_limits_2 = Constraint(List_GDTS, rule=genset_power_active_limits_rule_2)

def genset_power_reactive_limits_rule_1(model, i, t, s):
    return(model.QG[i, t, s] >= QG_min[i])
model.genset_power_reactive_limits_1 = Constraint(List_GDTS, rule=genset_power_reactive_limits_rule_1)

def genset_power_reactive_limits_rule_2(model, i, t, s):
    return(model.QG[i, t, s] <= QG_max[i])
model.genset_power_reactive_limits_2 = Constraint(List_GDTS, rule=genset_power_reactive_limits_rule_2)

def genset_operation_1_rule_cm(model, i, t, s):
    return(model.PGa[i, t, s] == 0)
model.genset_operation_1_cm = Constraint(List_GDTS, rule=genset_operation_1_rule_cm)

def genset_operation_2_rule_cm(model, i, t, s):
    return(model.PGb[i, t, s] == 0)
model.genset_operation_2_cm = Constraint(List_GDTS, rule=genset_operation_2_rule_cm)

def genset_operation_3_rule_cm(model, i, t, s):
    return(model.PGc[i, t, s] == 0)
model.genset_operation_3_cm = Constraint(List_GDTS, rule=genset_operation_3_rule_cm)

def genset_operation_4_rule_cm(model, i, t, s):
    return(model.QGa[i, t, s] == 0)
model.genset_operation_4_cm = Constraint(List_GDTS, rule=genset_operation_4_rule_cm)

def genset_operation_5_rule_cm(model, i, t, s):
    return(model.QGb[i, t, s] == 0)
model.genset_operation_5_cm = Constraint(List_GDTS, rule=genset_operation_5_rule_cm)

def genset_operation_6_rule_cm(model, i, t, s):
    return(model.QGc[i, t, s] == 0)
model.genset_operation_6_cm = Constraint(List_GDTS, rule=genset_operation_6_rule_cm)

# Island Operation ----------------------------------------------------------------
model.islanded_operation = ConstraintList()
for i in N:
    for t in T:
        for o in O:
            for s in S:
                if datetime.strptime(t, '%H:%M:%S') >= datetime.strptime(o, '%H:%M:%S') and datetime.strptime(t, '%H:%M:%S') < datetime.strptime(o, '%H:%M:%S') + timedelta(hours=out_time):    
                    model.islanded_operation.add(expr = model.Ppcc_a_out[i, t, o, s] == 0)
                    model.islanded_operation.add(expr = model.Ppcc_b_out[i, t, o, s] == 0)
                    model.islanded_operation.add(expr = model.Ppcc_c_out[i, t, o, s] == 0)
                    model.islanded_operation.add(expr = model.Qpcc_a_out[i, t, o, s] == 0)
                    model.islanded_operation.add(expr = model.Qpcc_b_out[i, t, o, s] == 0)
                    model.islanded_operation.add(expr = model.Qpcc_c_out[i, t, o, s] == 0) 

#------------- Operation with outage -------------------------------------------

#-----------------------New constraint-----------------------------------------

def active_power_positive_a_rule_out(model, i, t, o, s):
    return (model.Ppcc_a_out[i,t,o,s] - model.Ppcc_a_out_po[i,t,o,s] + model.Ppcc_a_out_ne[i,t,o,s] == 0)
model.active_power_positive_a_out = Constraint(List_NTOS, rule=active_power_positive_a_rule_out)

def active_power_positive_b_rule_out(model, i, t, o, s):
    return (model.Ppcc_b_out[i,t,o,s] - model.Ppcc_b_out_po[i,t,o,s] + model.Ppcc_b_out_ne[i,t,o,s] == 0)
model.active_power_positive_b_out = Constraint(List_NTOS, rule=active_power_positive_b_rule_out)

def active_power_positive_c_rule_out(model, i, t, o, s):
    return (model.Ppcc_c_out[i,t,o,s] - model.Ppcc_c_out_po[i,t,o,s] + model.Ppcc_c_out_ne[i,t,o,s] == 0)
model.active_power_positive_c_out = Constraint(List_NTOS, rule=active_power_positive_c_rule_out)

# Active losses ----------------------------------------------------------------
def active_losses_a_rule_out(model, i, j, t, o, s):
    return (
        (1 / (Va_0_out[i, t, o, s] * Va_0_out[i, t, o, s])) * 
        (Raa_p[i, j] * model.Pa_sqr_out[i, j, t, o, s] + 
        Raa_p[i, j] * model.Qa_sqr_out[i, j, t, o, s] - 
        Xaa_p[i, j] * Pa_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] + 
        Xaa_p[i, j] * Qa_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s]) +
        (1 / (Va_0_out[i, t, o, s] * Vb_0_out[i, t, o, s])) * 
        (Rab_p[i, j] * Pb_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
        Rab_p[i, j] * Qb_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] - 
        Xab_p[i, j] * Pb_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] + 
        Xab_p[i, j] * Qb_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s]) +
        (1 / (Va_0_out[i, t, o, s] * Vc_0_out[i, t, o, s])) * 
        (Rac_p[i, j] * Pc_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
        Rac_p[i, j] * Qc_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] - 
        Xac_p[i, j] * Pc_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] + 
        Xac_p[i, j] * Qc_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s]) == model.Plss_a_out[i, j, t, o, s])
model.active_losses_a_out = Constraint(List_LTOS, rule=active_losses_a_rule_out)

def active_losses_b_rule_out(model, i, j, t, o, s):
    return (
        (1 / (Vb_0_out[i, t, o, s] * Va_0_out[i, t, o, s])) * 
        (Rba_p[i, j] * Pa_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
        Rba_p[i, j] * Qa_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] - 
        Xba_p[i, j] * Pa_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] + 
        Xba_p[i, j] * Qa_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s]) +
        (1 / (Vb_0_out[i, t, o, s] * Vb_0_out[i, t, o, s])) * 
        (Rbb_p[i, j] * model.Pb_sqr_out[i, j, t, o, s]  + 
        Rbb_p[i, j] * model.Qb_sqr_out[i, j, t, o, s]  - 
        Xbb_p[i, j] * Pb_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] + 
        Xbb_p[i, j] * Qb_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s]) +
        (1 / (Vb_0_out[i, t, o, s] * Vc_0_out[i, t, o, s])) * 
        (Rbc_p[i, j] * Pc_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
        Rbc_p[i, j] * Qc_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] - 
        Xbc_p[i, j] * Pc_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] + 
        Xbc_p[i, j] * Qc_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s]) == model.Plss_b_out[i, j, t, o, s])
model.active_losses_b_out = Constraint(List_LTOS, rule=active_losses_b_rule_out)

def active_losses_c_rule_out(model, i, j, t, o, s):
    return (
        (1 / (Vc_0_out[i, t, o, s] * Va_0_out[i, t, o, s])) * 
        (Rca_p[i, j] * Pa_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
        Rca_p[i, j] * Qa_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] - 
        Xca_p[i, j] * Pa_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] + 
        Xca_p[i, j] * Qa_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s]) +
        (1 / (Vc_0_out[i, t, o, s] * Vb_0_out[i, t, o, s])) * 
        (Rcb_p[i, j] * Pb_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
        Rcb_p[i, j] * Qb_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] - 
        Xcb_p[i, j] * Pb_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] + 
        Xcb_p[i, j] * Qb_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s]) +
        (1 / (Vc_0_out[i, t, o, s] * Vc_0_out[i, t, o, s])) * 
        (Rcc_p[i, j] * model.Pc_sqr_out[i, j, t, o, s]  + 
        Rcc_p[i, j] * model.Qc_sqr_out[i, j, t, o, s]  - 
        Xcc_p[i, j] * Pc_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] + 
        Xcc_p[i, j] * Qc_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s]) == model.Plss_c_out[i, j, t, o, s])
model.active_losses_c_out = Constraint(List_LTOS, rule=active_losses_c_rule_out)

# Reactive losses ----------------------------------------------------------------
def reactive_losses_a_rule_out(model, i, j, t, o, s):
    return (
        (1 / (Va_0_out[i, t, o, s] * Va_0_out[i, t, o, s])) * 
        (Raa_p[i, j] * Pa_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] - 
        Raa_p[i, j] * Qa_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
        Xaa_p[i, j] * model.Pa_sqr_out[i, j, t, o, s]  + 
        Xaa_p[i, j] * model.Qa_sqr_out[i, j, t, o, s] ) +
        (1 / (Va_0_out[i, t, o, s] * Vb_0_out[i, t, o, s])) * 
        (Rab_p[i, j] * Pb_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] - 
        Rab_p[i, j] * Qb_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
        Xab_p[i, j] * Pb_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
        Xab_p[i, j] * Qb_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s]) +
        (1 / (Va_0_out[i, t, o, s] * Vc_0_out[i, t, o, s])) * 
        (Rac_p[i, j] * Pc_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s] - 
        Rac_p[i, j] * Qc_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
        Xac_p[i, j] * Pc_0_out[i, j, t, o, s] * model.Pa_out[i, j, t, o, s] + 
        Xac_p[i, j] * Qc_0_out[i, j, t, o, s] * model.Qa_out[i, j, t, o, s]) == model.Qlss_a_out[i, j, t, o, s])
model.reactive_losses_a_out = Constraint(List_LTOS, rule=reactive_losses_a_rule_out)

def reactive_losses_b_rule_out(model, i, j, t, o, s):
    return (
        (1 / (Vb_0_out[i, t, o, s] * Va_0_out[i, t, o, s])) * 
        (Rba_p[i, j] * Pa_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] - 
        Rba_p[i, j] * Qa_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
        Xba_p[i, j] * Pa_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
        Xba_p[i, j] * Qa_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s]) +
        (1 / (Vb_0_out[i, t, o, s] * Vb_0_out[i, t, o, s])) * 
        (Rbb_p[i, j] * Pb_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] - 
        Rbb_p[i, j] * Qb_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
        Xbb_p[i, j] * model.Pb_sqr_out[i, j, t, o, s]  + 
        Xbb_p[i, j] * model.Qb_sqr_out[i, j, t, o, s] ) +
        (1 / (Vb_0_out[i, t, o, s] * Vc_0_out[i, t, o, s])) * 
        (Rbc_p[i, j] * Pc_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s] - 
        Rbc_p[i, j] * Qc_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
        Xbc_p[i, j] * Pc_0_out[i, j, t, o, s] * model.Pb_out[i, j, t, o, s] + 
        Xbc_p[i, j] * Qc_0_out[i, j, t, o, s] * model.Qb_out[i, j, t, o, s]) == model.Qlss_b_out[i, j, t, o, s])
model.reactive_losses_b_out = Constraint(List_LTOS, rule= reactive_losses_b_rule_out)

def reactive_losses_c_rule_out(model, i, j, t, o, s):
    return (
        (1 / (Vc_0_out[i, t, o, s] * Va_0_out[i, t, o, s])) * 
        (Rca_p[i, j] * Pa_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] - 
        Rca_p[i, j] * Qa_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
        Xca_p[i, j] * Pa_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
        Xca_p[i, j] * Qa_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s]) +
        (1 / (Vc_0_out[i, t, o, s] * Vb_0_out[i, t, o, s])) * 
        (Rcb_p[i, j] * Pb_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] - 
        Rcb_p[i, j] * Qb_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
        Xcb_p[i, j] * Pb_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
        Xcb_p[i, j] * Qb_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s]) +
        (1 / (Vc_0_out[i, t, o, s] * Vc_0_out[i, t, o, s])) * 
        (Rcc_p[i, j] * Pc_0_out[i, j, t, o, s] * model.Qc_out[i, j, t, o, s] - 
        Rcc_p[i, j] * Qc_0_out[i, j, t, o, s] * model.Pc_out[i, j, t, o, s] + 
        Xcc_p[i, j] * model.Pc_sqr_out[i, j, t, o, s]  + 
        Xcc_p[i, j] * model.Qc_sqr_out[i, j, t, o, s] ) == model.Qlss_c_out[i, j, t, o, s])
model.reactive_losses_c_out = Constraint(List_LTOS, rule= reactive_losses_c_rule_out)

# Active Power Flow ----------------------------------------------------------------

def active_power_balance_rule_out_a(model, i, t, o, s):
    return (
        sum(model.Pa_out[a, j, t, o, s]*df[(i,a,j)] for (a,j) in L) -  
        sum(model.Plss_a_out[a, j, t, o, s]*p[(i,a,j)] for (a,j) in L) +
        model.Ppcc_a_out[i, t, o, s] +
        sum(model.PGa_out[a, t, o, s] for a in dict_nos_gd[i]) +
        sum(model.PB_dis_a[a, t] for a in dict_nos_bs[i]) -
        sum(model.PB_ch_a[a, t] for a in dict_nos_bs[i]) -
        # sum(model.PEV_ch_a_1[a, t] for a in dict_nos_ev[i]) -
        # sum(model.PEV_ch_a_2[a, t] for a in dict_nos_ev[i]) -
        PDa[(i,t)]*sd[s]*model.xd[i, t, o, s] + PVa[(i,t)]*spv[s]*model.xpv[i, t, o, s] == 0)
model.active_power_balance_a_out = Constraint(List_NTOS, rule=active_power_balance_rule_out_a)

def active_power_balance_rule_out_b(model, i, t, o, s):
    return (
        sum(model.Pb_out[a, j, t, o, s]*df[(i,a,j)] for (a,j) in L) -
        sum(model.Plss_b_out[a, j, t, o, s]*p[(i,a,j)] for (a,j) in L) +
        model.Ppcc_b_out[i, t, o, s] +
        sum(model.PGb_out[a, t, o, s] for a in dict_nos_gd[i]) +
        sum(model.PB_dis_b[a, t] for a in dict_nos_bs[i]) -
        sum(model.PB_ch_b[a, t] for a in dict_nos_bs[i]) -
        # sum(model.PEV_ch_1[a, t] for a in dict_nos_ev[i]) -
        # sum(model.PEV_ch_2[a, t] for a in dict_nos_ev[i]) -
        PDa[(i,t)]*sd[s]*model.xd[i, t, o, s] + PVa[(i,t)]*spv[s]*model.xpv[i, t, o, s] == 0)
model.active_power_balance_b_out = Constraint(List_NTOS, rule=active_power_balance_rule_out_b)

def active_power_balance_rule_out_c(model, i, t, o, s):
    return (
        sum(model.Pc_out[a, j, t, o, s]*df[(i,a,j)] for (a,j) in L) -
        sum(model.Plss_c_out[a, j, t, o, s]*p[(i,a,j)] for (a,j) in L) +
        model.Ppcc_c_out[i, t, o, s] +
        sum(model.PGc_out[a, t, o, s] for a in dict_nos_gd[i]) +
        sum(model.PB_dis_c[a, t] for a in dict_nos_bs[i]) -
        sum(model.PB_ch_c[a, t] for a in dict_nos_bs[i]) -
        # sum(model.PEV_ch_c_1[a, t] for a in dict_nos_ev[i]) -
        # sum(model.PEV_ch_c_2[a, t] for a in dict_nos_ev[i]) -
        PDa[(i,t)]*sd[s]*model.xd[i, t, o, s] + PVa[(i,t)]*spv[s]*model.xpv[i, t, o, s] == 0)
model.active_power_balance_c_out = Constraint(List_NTOS, rule=active_power_balance_rule_out_c)  

# Reactive Power Flow ----------------------------------------------------------------
def reactive_power_balance_out_rule_out_a(model, i, t, o, s):
    return (
        sum(model.Qa_out[a, j, t, o, s]*df[(i,a,j)] for (a,j) in L) -
        sum(model.Qlss_a_out[a, j, t, o, s]*p[(i,a,j)] for (a,j) in L) +
        model.Qpcc_a_out[i, t, o, s] +
        sum(model.QGa_out[a, t, o, s] for a in dict_nos_gd[i]) -
        (QDa[(i,t)]*sd[s]) * model.xd[i, t, o, s] == 0)
model.reactive_power_balance_out_a = Constraint(List_NTOS, rule=reactive_power_balance_out_rule_out_a)

def reactive_power_balance_out_rule_out_b(model, i, t, o, s):
    return (
        sum(model.Qb_out[a, j, t, o, s]*df[(i,a,j)] for (a,j) in L) -
        sum(model.Qlss_b_out[a, j, t, o, s]*p[(i,a,j)] for (a,j) in L) +
        model.Qpcc_b_out[i, t, o, s] +
        sum(model.QGb_out[a, t, o, s] for a in dict_nos_gd[i]) -
        (QDb[(i,t)]*sd[s]) * model.xd[i, t, o, s] == 0)
model.reactive_power_balance_out_b = Constraint(List_NTOS, rule=reactive_power_balance_out_rule_out_b)

def reactive_power_balance_out_rule_out_c(model, i, t, o, s):
    return (
        sum(model.Qc_out[a, j, t, o, s]*df[(i,a,j)] for (a,j) in L) -
        sum(model.Qlss_c_out[a, j, t, o, s]*p[(i,a,j)] for (a,j) in L) +
        model.Qpcc_c_out[i, t, o, s] +
        sum(model.QGc_out[a, t, o, s] for a in dict_nos_gd[i]) -
        (QDc[(i,t)]*sd[s]) * model.xd[i, t, o, s] == 0)
model.reactive_power_balance_out_c = Constraint(List_NTOS, rule=reactive_power_balance_out_rule_out_c)

# Voltage Droop in the Lines ----------------------------------------------------------------
def voltage_droop_out_rule_out_a(model, i, j, t, o, s):
    return((2*(Raa_p[i,j]*model.Pa_out[i, j, t, o, s] + Xaa_p[i,j]*model.Qa_out[i, j, t, o, s])) + 
            (2*(Rab_p[i,j]*model.Pb_out[i, j, t, o, s] + Xab_p[i,j]*model.Qb_out[i, j, t, o, s])) + 
            (2*(Rac_p[i,j]*model.Pc_out[i, j, t, o, s] + Xac_p[i,j]*model.Qc_out[i, j, t, o, s])) -
        (1/Va_0_out[i, t, o, s]**2) * ((Raa_p[i,j]**2 + Xaa_p[i,j]**2) * (model.Pa_sqr_out[i, j, t, o, s] + 
        model.Qa_sqr_out[i, j, t, o, s])) == model.Va_sqr_out[i, t, o, s] - model.Va_sqr_out[j, t, o, s])
model.voltage_droop_out_a = Constraint(List_LTOS, rule= voltage_droop_out_rule_out_a)

def voltage_droop_out_rule_out_b(model, i, j, t, o, s):
    return((2*(Rba_p[i,j]*model.Pa_out[i, j, t, o, s] + Xba_p[i,j]*model.Qa_out[i, j, t, o, s])) + 
        (2*(Rbb_p[i,j]*model.Pb_out[i, j, t, o, s] + Xbb_p[i,j]*model.Qb_out[i, j, t, o, s])) + 
        (2*(Rbc_p[i,j]*model.Pc_out[i, j, t, o, s] + Xbc_p[i,j]*model.Qc_out[i, j, t, o, s])) -
        (1/Vb_0_out[i, t, o, s]**2) * ((Rbb_p[i,j]**2 + Xbb_p[i,j]**2) * (model.Pb_sqr_out[i, j, t, o, s] + 
        model.Qb_sqr_out[i, j, t, o, s])) == model.Vb_sqr_out[i, t, o, s] - model.Vb_sqr_out[j, t, o, s])
model.voltage_droop_out_b = Constraint(List_LTOS, rule= voltage_droop_out_rule_out_b)

def voltage_droop_out_rule_out_c(model, i, j, t, o, s):
    return((2*(Rca_p[i,j]*model.Pa_out[i, j, t, o, s] + Xca_p[i,j]*model.Qa_out[i, j, t, o, s])) + 
        (2*(Rcb_p[i,j]*model.Pb_out[i, j, t, o, s] + Xcb_p[i,j]*model.Qb_out[i, j, t, o, s])) + 
        (2*(Rcc_p[i,j]*model.Pc_out[i, j, t, o, s] + Xcc_p[i,j]*model.Qc_out[i, j, t, o, s])) -
        (1/Vc_0_out[i, t, o, s]**2) * ((Rcc_p[i,j]**2 + Xcc_p[i,j]**2) * (model.Pc_sqr_out[i, j, t, o, s] + 
        model.Qc_sqr_out[i, j, t, o, s])) == model.Vc_sqr_out[i, t, o, s] - model.Vc_sqr_out[j, t, o, s])
model.voltage_droop_out_c = Constraint(List_LTOS, rule= voltage_droop_out_rule_out_c)

# Limite máximo de fluxo de corrente e equações de linearização ----------------------------------------------------------------

def current_limits_rule_out_a(model, i, j, t, o, s):
    return((model.Pa_sqr_out[i, j, t, o, s] + model.Qa_sqr_out[i, j, t, o, s]) <= Imax[i,j]**2 * (model.Va_sqr_out[i, t, o, s]))
model.current_limits_a_out = Constraint(List_LTOS, rule = current_limits_rule_out_a)

def current_limits_rule_out_b(model, i, j, t, o, s):
    return((model.Pb_sqr_out[i, j, t, o, s] + model.Qb_sqr_out[i, j, t, o, s]) <= Imax[i,j]**2 * (model.Vb_sqr_out[i, t, o, s]))
model.current_limits_b_out = Constraint(List_LTOS, rule = current_limits_rule_out_b)

def current_limits_rule_out_c(model, i, j, t, o, s):
    return((model.Pc_sqr_out[i, j, t, o, s] + model.Qc_sqr_out[i, j, t, o, s]) <= Imax[i,j]**2 * (model.Vc_sqr_out[i, t, o, s]))
model.current_limits_c_out = Constraint(List_LTOS, rule = current_limits_rule_out_c)

# Active power linearization constraints
def pa_calculation_rule_out(model, i, j, t, o, s):
    return( model.Pa_sqr_out[i, j, t, o, s] - sum(S_ms[i,j,y] * model.Pa_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.Pa_calculation_out = Constraint(List_LTOS, rule = pa_calculation_rule_out)

def pb_calculation_rule_out(model, i, j, t, o, s):
    return( model.Pb_sqr_out[i, j, t, o, s] - sum(S_ms[i,j,y] * model.Pb_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.Pb_calculation_out = Constraint(List_LTOS, rule = pb_calculation_rule_out)

def pc_calculation_rule_out(model, i, j, t, o, s):
    return( model.Pc_sqr_out[i, j, t, o, s] - sum(S_ms[i,j,y] * model.Pc_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.Pc_calculation_out = Constraint(List_LTOS, rule = pc_calculation_rule_out)

# Reactive power linearization constraints
def qa_calculation_rule_out(model, i, j, t, o, s):
    return( model.Qa_sqr_out[i, j, t, o, s] - sum(S_ms[i,j,y] * model.Qa_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.Qa_calculation_out = Constraint(List_LTOS, rule = qa_calculation_rule_out)

def qb_calculation_rule_out(model, i, j, t, o, s):
    return( model.Qb_sqr_out[i, j, t, o, s] - sum(S_ms[i,j,y] * model.Qb_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.Qb_calculation_out = Constraint(List_LTOS, rule = qb_calculation_rule_out)

def qc_calculation_rule_out(model, i, j, t, o, s):
    return( model.Qc_sqr_out[i, j, t, o, s] - sum(S_ms[i,j,y] * model.Qc_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.Qc_calculation_out = Constraint(List_LTOS, rule = qc_calculation_rule_out)

# Linearizations variables
def pa_p_rule_out(model, i, j, t,o, s):
    return( model.Pa_p_out[i, j, t, o, s] - model.Pa_n_out[i, j, t, o, s] - model.Pa_out[i, j, t, o, s] == 0)
model.Pa_p_constraint_out = Constraint(List_LTOS, rule = pa_p_rule_out)

def pb_p_rule_out(model, i, j, t,o, s):
    return( model.Pb_p_out[i, j, t, o, s] - model.Pb_n_out[i, j, t, o, s] - model.Pb_out[i, j, t, o, s] == 0)
model.Pb_p_constraint_out = Constraint(List_LTOS, rule = pb_p_rule_out)

def pc_p_rule_out(model, i, j, t,o, s):
    return( model.Pc_p_out[i, j, t, o, s] - model.Pc_n_out[i, j, t, o, s] - model.Pc_out[i, j, t, o, s] == 0)
model.Pc_p_constraint_out = Constraint(List_LTOS, rule = pc_p_rule_out)

def qa_p_rule_out(model, i, j, t,o, s):
    return( model.Qa_p_out[i, j, t, o, s] - model.Qa_n_out[i, j, t, o, s] - model.Qa_out[i, j, t, o, s] == 0)
model.Qa_p_constraint_out = Constraint(List_LTOS, rule = qa_p_rule_out)

def qb_p_rule_out(model, i, j, t,o, s):
    return( model.Qb_p_out[i, j, t, o, s] - model.Qb_n_out[i, j, t, o, s] - model.Qb_out[i, j, t, o, s] == 0)
model.Qb_p_constraint_out = Constraint(List_LTOS, rule = qb_p_rule_out)

def qc_p_rule_out(model, i, j, t,o, s):
    return( model.Qc_p_out[i, j, t, o, s] - model.Qc_n_out[i, j, t, o, s] - model.Qc_out[i, j, t, o, s] == 0)
model.Qc_p_constraint_out = Constraint(List_LTOS, rule = qc_p_rule_out)

def pa_abs_rule_out(model, i, j, t,o, s):
    return( model.Pa_p_out[i, j, t, o, s] + model.Pa_n_out[i, j, t, o, s] - sum(model.Pa_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.pa_abs_out = Constraint(List_LTOS, rule = pa_abs_rule_out)

def pb_abs_rule_out(model, i, j, t,o, s):
    return( model.Pb_p_out[i, j, t, o, s] + model.Pb_n_out[i, j, t, o, s] - sum(model.Pb_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.pb_abs_out = Constraint(List_LTOS, rule = pb_abs_rule_out)

def pc_abs_rule_out(model, i, j, t,o, s):
    return( model.Pc_p_out[i, j, t, o, s] + model.Pc_n_out[i, j, t, o, s] - sum(model.Pc_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.pc_abs_out = Constraint(List_LTOS, rule = pc_abs_rule_out)

def qa_abs_rule_out(model, i, j, t,o, s):
    return( model.Qa_p_out[i, j, t, o, s] + model.Qa_n_out[i, j, t, o, s] - sum(model.Qa_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.qa_abs_out = Constraint(List_LTOS, rule = qa_abs_rule_out)

def qb_abs_rule_out(model, i, j, t,o, s):
    return( model.Qb_p_out[i, j, t, o, s] + model.Qb_n_out[i, j, t, o, s] - sum(model.Qb_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.qb_abs_out = Constraint(List_LTOS, rule = qb_abs_rule_out)

def qc_abs_rule_out(model, i, j, t,o, s):
    return( model.Qc_p_out[i, j, t, o, s] + model.Qc_n_out[i, j, t, o, s] - sum(model.Qc_Dp_out[i, j, t, o, s, y] for y in Y) == 0)
model.qc_abs_out = Constraint(List_LTOS, rule = qc_abs_rule_out)

def pa_limits_rule_out(model, i, j, t, o, s, y):
    return( model.Pa_Dp_out[i, j, t, o, s, y] <= S_Dp_max[i,j])
model.pa_limits_out = Constraint(List_LTOSY, rule = pa_limits_rule_out)

def pb_limits_rule_out(model, i, j, t, o, s, y):
    return( model.Pb_Dp_out[i, j, t, o, s, y] <= S_Dp_max[i,j])
model.pb_limits_out = Constraint(List_LTOSY, rule = pb_limits_rule_out)

def pc_limits_rule_out(model, i, j, t, o, s, y):
    return( model.Pc_Dp_out[i, j, t, o, s, y] <= S_Dp_max[i,j])
model.pc_limits_out = Constraint(List_LTOSY, rule = pc_limits_rule_out)

def qa_limits_rule_out(model, i, j, t, o, s, y):
    return( model.Qa_Dp_out[i, j, t, o, s, y] <= S_Dp_max[i,j])
model.qa_limits_out = Constraint(List_LTOSY, rule = qa_limits_rule_out)

def qb_limits_rule_out(model, i, j, t, o, s, y):
    return( model.Qb_Dp_out[i, j, t, o, s, y] <= S_Dp_max[i,j])
model.qb_limits_out = Constraint(List_LTOSY, rule = qb_limits_rule_out)

def qc_limits_rule_out(model, i, j, t, o, s, y):
    return( model.Qc_Dp_out[i, j, t, o, s, y] <= S_Dp_max[i,j])
model.qc_limits_out = Constraint(List_LTOSY, rule = qc_limits_rule_out)

# Limete potência aparente fornecida pelo PCC ----------------------------------------------------------------
def ative_power_pcc_rule_out(model, i, t, o, s):
    return(model.Ppcc_out[i, t, o, s] - model.Ppcc_a_out[i, t, o, s] - model.Ppcc_b_out[i, t, o, s] - model.Ppcc_c_out[i, t, o, s] == 0)
model.active_power_pcc_out = Constraint(List_NTOS, rule = ative_power_pcc_rule_out)

def reative_power_pcc_rule_out(model, i, t, o, s):
    return(model.Qpcc_out[i, t, o, s] - model.Qpcc_a_out[i, t, o, s] - model.Qpcc_b_out[i, t, o, s] - model.Qpcc_c_out[i, t, o, s] == 0)
model.reactive_power_pcc_out = Constraint(List_NTOS, rule = reative_power_pcc_rule_out)

def apparent_power_pcc_rule_out(model, i, t, o, s):
    return(model.Ppcc_sqr_out[i, t, o, s] + model.Qpcc_sqr_out[i, t, o, s] <= Smax[i]**2)
model.apparent_power_pcc_out = Constraint(List_NTOS, rule = apparent_power_pcc_rule_out)


def ppcc_calculation_rule_out(model, i, t, o, s):
    return( model.Ppcc_sqr_out[i, t, o, s] - sum(Spcc_ms[i,y] * model.Ppcc_Dp_out[i, t, o, s, y] for y in Y) == 0)
model.Ppcc_calculation_out = Constraint(List_NTOS, rule = ppcc_calculation_rule_out)

def Qpcc_calculation_rule_out(model, i, t, o, s):
    return( model.Qpcc_sqr_out[i, t, o, s] - sum(Spcc_ms[i,y] * model.Qpcc_Dp_out[i, t, o, s, y] for y in Y) == 0)
model.Qpcc_calculation_out = Constraint(List_NTOS, rule = Qpcc_calculation_rule_out)

def ppcc_p_rule_out(model, i, t, o, s):
    return( model.Ppcc_p_out[i, t, o, s] - model.Ppcc_n_out[i, t, o, s] - model.Ppcc_out[i, t, o, s] == 0)
model.Ppcc_p_constraint_out = Constraint(List_NTOS, rule = ppcc_p_rule_out)

def qpcc_p_rule_out(model, i, t, o, s):
    return( model.Qpcc_p_out[i, t, o, s] - model.Qpcc_n_out[i, t, o, s] - model.Qpcc_out[i, t, o, s] == 0)
model.Qpcc_p_constraint_out = Constraint(List_NTOS, rule = qpcc_p_rule_out)

def ppcc_abs_rule_out(model, i, t, o, s):
    return( model.Ppcc_p_out[i, t, o, s] + model.Ppcc_n_out[i, t, o, s] - sum(model.Ppcc_Dp_out[i, t, o, s, y] for y in Y) == 0)
model.ppcc_abs_out = Constraint(List_NTOS, rule=ppcc_abs_rule_out)

def qpcc_abs_rule_out(model, i, t, o, s):
    return( model.Qpcc_p_out[i, t, o, s] + model.Qpcc_n_out[i, t, o, s] - sum(model.Qpcc_Dp_out[i, t, o, s, y] for y in Y) == 0)
model.qpcc_abs_out = Constraint(List_NTOS, rule=qpcc_abs_rule_out)

def ppcc_limits_rule_out(model, i, t, o, s, y):
    return( model.Ppcc_Dp_out[i, t, o, s, y] <= Spcc_Dp_max[i])
model.ppcc_limits_out = Constraint(List_NTOSY, rule=ppcc_limits_rule_out)

def qpcc_limits_rule_out(model, i, t, o, s, y):
    return( model.Qpcc_Dp_out[i, t, o, s, y] <= Spcc_Dp_max[i])
model.qpcc_limits_out = Constraint(List_NTOSY, rule=qpcc_limits_rule_out)

# Genset --------------------------------------------------------------------
def genset_power_rule_out(model, i, t, o, s):
    return(model.PGa_out[i, t, o, s] + model.PGb_out[i, t, o, s] + model.PGc_out[i, t, o, s] == model.PG_out[i, t, o, s])
model.genset_power_active_out = Constraint(List_GDTOS, rule = genset_power_rule_out)

def genset_power_reactive_rule_out(model, i, t, o, s):
    return(model.QGa_out[i, t, o, s] + model.QGb_out[i, t, o, s] + model.QGc_out[i, t, o, s] == model.QG_out[i, t, o, s])
model.genset_power_reactive_out = Constraint(List_GDTOS, rule = genset_power_reactive_rule_out)

def genset_power_active_limits_rule_out_1(model, i, t, o, s):
    return(model.PG_out[i, t, o, s] >= PG_min[i] * model.oG_out[i, t, o, s])
model.genset_power_active_limits_1_out = Constraint(List_GDTOS, rule = genset_power_active_limits_rule_out_1)

def genset_power_active_limits_rule_out_2(model, i, t, o, s):
    return(model.PG_out[i, t, o, s] <= PG_max[i] * model.oG_out[i, t, o, s])
model.genset_power_active_limits_2_out = Constraint(List_GDTOS, rule = genset_power_active_limits_rule_out_2)

def genset_power_reactive_limits_rule_out_1(model, i, t, o, s):
    return(model.QG_out[i, t, o, s] >= QG_min[i] * model.oG_out[i, t, o, s])
model.genset_power_reactive_limits_1_out = Constraint(List_GDTOS, rule = genset_power_reactive_limits_rule_out_1)

def genset_power_reactive_limits_rule_out_2(model, i, t, o, s):
    return(model.QG_out[i, t, o, s] <= QG_max[i] * model.oG_out[i, t, o, s])
model.genset_power_reactive_limits_2_out = Constraint(List_GDTOS, rule = genset_power_reactive_limits_rule_out_2)

model.genset_operation_grid_connected = ConstraintList()
for i in GD:
    for t in T:
        for o in O:
            for s in S:
                if datetime.strptime(t, '%H:%M:%S') < datetime.strptime(o, '%H:%M:%S') or datetime.strptime(t, '%H:%M:%S') >= datetime.strptime(o, '%H:%M:%S') + timedelta(hours=out_time):    

                    model.genset_operation_grid_connected.add(expr = model.PGa_out[i, t, o, s] == 0)
                    model.genset_operation_grid_connected.add(expr = model.PGb_out[i, t, o, s] == 0)
                    model.genset_operation_grid_connected.add(expr = model.PGc_out[i, t, o, s] == 0)
                    model.genset_operation_grid_connected.add(expr = model.QGa_out[i, t, o, s] == 0)
                    model.genset_operation_grid_connected.add(expr = model.QGb_out[i, t, o, s] == 0)
                    model.genset_operation_grid_connected.add(expr = model.QGc_out[i, t, o, s] == 0)

# Battery --------------------------------------------------------------------
def energy_bess_rule(model,i,t):
    if t == T[0]:
        return model.EB[i,t] - EBi[i] - model.PB[i,t]*delta_t == 0
    else:
        t0 = (datetime.strptime(t, '%H:%M') - timedelta(hours=delta_t)).strftime('%H:%M')
        return model.EB[i,t] - model.EB[i,t0] - model.PB[i,t]*delta_t == 0
model.energy_soc_bess = Constraint(List_BT, rule=energy_bess_rule)

def power_bess_rule(model,i,t):
    return(model.PB[i,t] - model.PB_ch[i,t]*eta_b[i] + model.PB_dis[i,t]*(1/eta_b[i]) == 0)
model.power_bess = Constraint(List_BT, rule=power_bess_rule)

def operation_mode_bess_rule(model,i,t):
    return(model.b_ch[i,t] + model.b_dis[i,t] <= 1)
model.operation_mode_bess = Constraint(List_BT, rule = operation_mode_bess_rule)

def power_ch_total_rule(model, i, t):
    return(model.PB_ch[i,t] - model.PB_ch_a[i,t] - model.PB_ch_b[i,t] - model.PB_ch_c[i,t] == 0)
model.power_ch_total_bess = Constraint(List_BT, rule= power_ch_total_rule)

def power_balance_charging_1_rule(model,i,t):
    return(model.PB_ch_a[i,t] == model.PB_ch_b[i,t])
model.power_balance_charging_1_bess = Constraint(List_BT, rule=power_balance_charging_1_rule)

def power_balance_charging_2_rule(model,i,t):
    return(model.PB_ch_a[i,t] == model.PB_ch_c[i,t])
model.power_balance_charging_2_bess = Constraint(List_BT, rule=power_balance_charging_2_rule)

def power_balance_charging_3_rule(model,i,t):
    return(model.PB_ch_b[i,t] == model.PB_ch_c[i,t])
model.power_balance_charging_3_bess = Constraint(List_BT, rule=power_balance_charging_3_rule)

def power_dis_total_rule(model,i,t):
    return(model.PB_dis[i,t] - model.PB_dis_a[i,t] - model.PB_dis_b[i,t] - model.PB_dis_c[i,t] == 0)
model.power_dis_total_bess = Constraint(List_BT, rule = power_dis_total_rule)

def power_balance_discharging_1_rule(model,i,t):
    return(model.PB_dis_a[i,t] == model.PB_dis_b[i,t])
model.power_balance_discharging_1_bess = Constraint(List_BT, rule=power_balance_discharging_1_rule)

def power_balance_discharging_2_rule(model,i,t):
    return(model.PB_dis_a[i,t] == model.PB_dis_c[i,t])
model.power_balance_discharging_2_bess = Constraint(List_BT, rule=power_balance_discharging_2_rule)

def power_balance_discharging_3_rule(model,i,t):
    return(model.PB_dis_b[i,t] == model.PB_dis_c[i,t])
model.power_balance_discharging_3_bess = Constraint(List_BT, rule=power_balance_discharging_3_rule)

def power_charge_limits_rule_1(model,i,t):
    return(model.PB_ch[i,t] >= 0)
model.power_charge_limits_1 = Constraint(List_BT, rule=power_charge_limits_rule_1)

def power_charge_limits_rule_2(model,i,t):
    return(model.PB_ch[i,t] <= PBmax[i] * model.b_ch[i,t])
model.power_charge_limits_2 = Constraint(List_BT, rule=power_charge_limits_rule_2)

def power_discharge_limits_rule_1(model,i,t):
    return(model.PB_dis[i,t] >= 0)
model.power_discharge_limits_1 = Constraint(List_BT, rule=power_discharge_limits_rule_1)

def power_discharge_limits_rule_2(model,i,t):
    return(model.PB_dis[i,t] <= PBmax[i] * model.b_dis[i,t])
model.power_discharge_limits_2 = Constraint(List_BT, rule = power_discharge_limits_rule_2)

def energy_bess_limits_rule_1(model,i,t):
    return(model.EB[i,t] >= EBmin[i])
model.energy_bess_limits_1 = Constraint(List_BT, rule = energy_bess_limits_rule_1)

def energy_bess_limits_rule_2(model,i,t):
    return(model.EB[i,t] <= EBmax[i])
model.energy_bess_limits_2 = Constraint(List_BT, rule = energy_bess_limits_rule_2)


#----------------- FIX Variables --------------------------------------------------
model.fix_active_power = ConstraintList()
for i in Tb:
    for t in T:
        for s in S:
            if Tb[i] == 1:
                model.fix_active_power.add(expr=model.Va[i, t, s] == Vnom)
                model.fix_active_power.add(expr=model.Vb[i, t, s] == Vnom)
                model.fix_active_power.add(expr=model.Vc[i, t, s] == Vnom)
                model.fix_active_power.add(expr=model.Va_sqr[i, t, s] == Vnom**2)
                model.fix_active_power.add(expr=model.Vb_sqr[i, t, s] == Vnom**2)
                model.fix_active_power.add(expr=model.Vc_sqr[i, t, s] == Vnom**2)
            else:
                model.fix_active_power.add(expr=model.Ppcc_a[i, t, s] == 0)
                model.fix_active_power.add(expr=model.Ppcc_b[i, t, s] == 0)
                model.fix_active_power.add(expr=model.Ppcc_c[i, t, s] == 0)
                model.fix_active_power.add(expr=model.Qpcc_a[i, t, s] == 0)
                model.fix_active_power.add(expr=model.Qpcc_b[i, t, s] == 0)
                model.fix_active_power.add(expr=model.Qpcc_c[i, t, s] == 0)

model.fix_voltage_out_1 = ConstraintList()
for i in Tb:
    for t in T:
        for o in O:
            for s in S:
                if Tb[i] == 1 and (datetime.strptime(t, '%H:%M:%S') < datetime.strptime(o, '%H:%M:%S') and datetime.strptime(t, '%H:%M:%S') >= datetime.strptime(o, '%H:%M:%S') + timedelta(hours=out_time)):
                    model.fix_voltage_out_1.add(expr=model.Va_out[i, t, o, s] == Vnom)
                    model.fix_voltage_out_1.add(expr=model.Vb_out[i, t, o, s] == Vnom)
                    model.fix_voltage_out_1.add(expr=model.Vc_out[i, t, o, s] == Vnom)
                    model.fix_voltage_out_1.add(expr=model.Va_sqr_out[i, t, o, s] == Vnom**2)
                    model.fix_voltage_out_1.add(expr=model.Vb_sqr_out[i, t, o, s] == Vnom**2)
                    model.fix_voltage_out_1.add(expr=model.Vc_sqr_out[i, t, o, s] == Vnom**2)

model.fix_voltage_out_2 = ConstraintList()
for i in Tb:
    for t in T:
        for o in O:
            for s in S:
                if Tb[i] == 2 and (datetime.strptime(t, '%H:%M:%S') >= datetime.strptime(o, '%H:%M:%S') and datetime.strptime(t, '%H:%M:%S') < datetime.strptime(o, '%H:%M:%S') + timedelta(hours=out_time)):
                    model.fix_voltage_out_2.add(expr = model.Va_out[i, t, o, s] == Vnom)
                    model.fix_voltage_out_2.add(expr = model.Vb_out[i, t, o, s] == Vnom)
                    model.fix_voltage_out_2.add(expr = model.Vc_out[i, t, o, s] == Vnom)
                    model.fix_voltage_out_2.add(expr = model.Va_sqr_out[i, t, o, s] == Vnom**2)
                    model.fix_voltage_out_2.add(expr = model.Vb_sqr_out[i, t, o, s] == Vnom**2)
                    model.fix_voltage_out_2.add(expr = model.Vc_sqr_out[i, t, o, s] == Vnom**2)

model.fix_active_power_out = ConstraintList()
for i in Tb:
    for t in T:
        for o in O:
            for s in S:
                if Tb[i] != 1:
                    model.fix_active_power_out.add(expr = model.Ppcc_a_out[i, t, o, s] == 0)
                    model.fix_active_power_out.add(expr = model.Ppcc_b_out[i, t, o, s] == 0)
                    model.fix_active_power_out.add(expr = model.Ppcc_c_out[i, t, o, s] == 0)

model.fix_reactive_power_out = ConstraintList()
for i in Tb:
    for t in T:
        for o in O:
            for s in S:
                if Tb[i] != 1:
                    model.fix_reactive_power_out.add(expr = model.Qpcc_a_out[i, t, o, s] == 0)
                    model.fix_reactive_power_out.add(expr = model.Qpcc_b_out[i, t, o, s] == 0)
                    model.fix_reactive_power_out.add(expr = model.Qpcc_c_out[i, t, o, s] == 0)



Resultado = SolverFactory('gurobi').solve(model)
print("Solver Status:", Resultado.solver.status)
print("Termination Condition:", Resultado.solver.termination_condition)


print("Solver Status:", Resultado.solver.status)
print("Termination Condition:", Resultado.solver.termination_condition)
print("Objective Function Value:", model.objective_1())

#----------------- Results --------------------------------------------------



# Inicialize uma lista para armazenar os dados
data = []

# Itere sobre os tempos e nós para coletar os valores das tensões
for t in T:
    row = {"Time": t}  # Comece a linha com o tempo
    for n in N:
        for s in S:
            row[f"V{n}a_{s}"] = model.Va_sqr[n, t, s].value  # Substitua '1' pelo cenário desejado
            row[f"V{n}b_{s}"] = model.Vb_sqr[n, t, s].value  # Substitua '1' pelo cenário desejado
            row[f"V{n}c_{s}"] = model.Vc_sqr[n, t, s].value  # Substitua '1' pelo cenário desejado
    data.append(row)

# Crie o DataFrame
df_voltages = pd.DataFrame(data)

# Exiba ou salve o DataFrame
print(df_voltages)
# df_voltages.to_csv("voltages.csv", index=False)


# Inicialize listas para armazenar os dados
data_power_nodes = []
data_power_battery = []

# Itere sobre os tempos, nós e cenários para coletar as potências dos nós
for t in T:
    row_nodes = {"Time": t}
    for n in N:
        for s in S:
            row_nodes[f"P{n}a_{s}"] = model.Ppcc_a[n, t, s].value
            row_nodes[f"P{n}b_{s}"] = model.Ppcc_b[n, t, s].value
            row_nodes[f"P{n}c_{s}"] = model.Ppcc_c[n, t, s].value
    data_power_nodes.append(row_nodes)

# Itere sobre os tempos e baterias para coletar as potências das baterias
for t in T:
    row_battery = {"Time": t}
    for b in B:
        row_battery[f"PB_{b}_ch"] = model.PB_ch[b, t].value
        row_battery[f"PB_{b}_dis"] = model.PB_dis[b, t].value
    data_power_battery.append(row_battery)

# Crie os DataFrames
df_power_nodes = pd.DataFrame(data_power_nodes)
df_power_battery = pd.DataFrame(data_power_battery)

# Concatene os DataFrames (usando Time como referência)
df_combined = pd.concat([df_power_nodes, df_power_battery], axis=1)

# Exiba ou salve o DataFrame combinado
print(df_combined)
# df_combined.to_csv("power_data.csv", index=False)


# Inicialize uma lista para armazenar os dados
data_battery_energy = []

# Itere sobre os tempos e baterias para coletar a energia armazenada
for t in T:
    row = {"Time": t}
    for b in B:
        row[f"Energy_B{b}"] = model.EB[b, t].value  # Energia da bateria b no tempo t
    data_battery_energy.append(row)

# Crie o DataFrame
df_battery_energy = pd.DataFrame(data_battery_energy)

# Exiba ou salve o DataFrame
print(df_battery_energy)
# df_battery_energy.to_csv("battery_energy_evolution.csv", index=False)


# Inicialize uma lista para armazenar os dados
data_evcs_power = []

# Itere sobre os tempos e conectores (C contém tuplas (EVCS, conector))
for t in T:
    row = {"Time": t}
    for evcs, connector in C:
        row[f"{evcs}_{connector}"] = model.PEVCS[t, (evcs, connector)].value
    data_evcs_power.append(row)

# Crie o DataFrame
df_evcs_power = pd.DataFrame(data_evcs_power)

# Exiba ou salve o DataFrame
print(df_evcs_power)
# df_evcs_power.to_csv("evcs_power.csv", index=False)

import pandas as pd

# Inicialize uma lista para armazenar os dados
data_ev_power_energy = []

# Itere sobre os tempos e EVs
for t in T:
    row = {"Time": t}  # Inicia a linha com o tempo
    for e in E:
        # Adiciona a potência de carga, descarga e a energia para cada EV
        row[f"PEV_{e}"] = model.PEV_c[t, e].value - model.PEV_d[t, e].value
        row[f"EEV_{e}"] = model.EEV[t, e].value
    data_ev_power_energy.append(row)

# Crie o DataFrame
df_ev_power_energy = pd.DataFrame(data_ev_power_energy)

# Exiba ou salve o DataFrame
print(df_ev_power_energy)
df_ev_power_energy.to_csv("ev_power_energy.csv", index=False)




import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyomo.environ as pyo  # Certifique-se de que as variáveis Pyomo sejam acessíveis no escopo

# Ajuste o loop conforme os seus conjuntos e variáveis Pyomo
for s in S:
    dic_values = {}  # Para os valores numéricos (ID do EV)
    dic_annotations = {}  # Para as anotações

    for evcs, connector in C:
        values = []  # Lista para armazenar os valores do ID do EV
        annotations = []  # Lista para armazenar as anotações

        for t in T:
            idev = 0  # ID do veículo
            idsoc = 0  # Estado de carga
            annotation = '0\n0%'  # Anotação padrão se nenhum EV estiver conectado

            for e in E:
                # Verifica se o EV está conectado ao EVCS e connector
                if pyo.value(model.aEV[t, e, (evcs, connector)]) == 1:
                    if idev > 0:
                        print(f'Error: More than one EV connected to {evcs}{connector} at {t}')
                    idev = int(e)
                    idsoc = int(100 * pyo.value(model.EEV[t, e])/EV[e]["Emax"])
                    annotation = f'{idev}\n{idsoc}%'  # Atualiza a anotação com valores reais

            values.append(idev)  # Adiciona o valor do ID para a coloração
            annotations.append(annotation)  # Adiciona a string formatada para anotações

        dic_values[f'{evcs}_{connector}'] = values
        dic_annotations[f'{evcs}_{connector}'] = annotations

    # Cria DataFrames para os valores e anotações
    df_values = pd.DataFrame.from_dict(dic_values, orient='index', columns=pd.to_datetime(T, format='%H:%M').time)
    df_annotations = pd.DataFrame.from_dict(dic_annotations, orient='index', columns=pd.to_datetime(T, format='%H:%M').time)

    # Cria o heatmap
    plt.figure(figsize=(16, 6))
    ax = sns.heatmap(df_values, cmap='tab20', cbar=False, linewidths=.5)

    # Adiciona anotações manualmente no heatmap
    for y, row in enumerate(df_annotations.values):
        for x, cell in enumerate(row):
            idev, idsoc = cell.split('\n')
            ax.text(x + 0.5, y + 0.3, idev, ha='center', va='center', fontsize=8)  # Tamanho da fonte para ID do EV
            ax.text(x + 0.5, y + 0.7, idsoc, ha='center', va='center', fontsize=6, color='gray')  # Tamanho da fonte para SoC

    # Configurações do gráfico
    plt.title(f'EV Connections - Scenario {s}')
    plt.xlabel('Time')
    plt.ylabel('EVCS_Connector')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Salvar o gráfico como PNG e PDF
    plt.savefig(f'Results/EVCS_Connections_s{s}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'Results/EVCS_Connections_s{s}.pdf', dpi=300, bbox_inches='tight')
    plt.close()


a = 1
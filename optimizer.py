import numpy as np
from scipy.optimize import minimize

def simulate_cost(x, data, penalty_weight=1000):
    P = data["P"]
    T = data["T"]
    x = np.clip(x, 0, None)  # Prevent negative generation
    generation = x.reshape((P, T))

    cost = 0
    penalty = 0

    # Unpack data
    cost_per_unit = np.array(data["cost_per_unit"])
    fixed_cost = np.array(data["fixed_cost"])
    min_output = np.array(data["min_output"])
    max_output = np.array(data["max_output"])
    ramp_rate = np.array(data["ramp_rate"])
    emissions = np.array(data["emissions"])
    emission_limit = np.array(data["emission_limit"])
    demand = np.array(data["demand"])
    transmission_cap = np.array(data["transmission_cap"])
    renewable_availability = np.array(data["renewable_availability"])
    plant_type = data["plant_type"]

    # Objective: cost + fixed cost
    for p in range(P):
        active = False
        for t in range(T):
            g = generation[p, t]
            cost += g * cost_per_unit[p]
            if g > 0:
                active = True
        if active:
            cost += fixed_cost[p]

    # Demand constraint
    for t in range(T):
        total_gen = np.sum(generation[:, t])
        if total_gen < demand[t]:
            penalty += (demand[t] - total_gen) ** 2
        if total_gen > transmission_cap[t]:
            penalty += (total_gen - transmission_cap[t]) ** 2

    # Emissions
    for p in range(P):
        total_emission = np.sum(generation[p, :] * emissions[p])
        if total_emission > emission_limit[p]:
            penalty += (total_emission - emission_limit[p]) ** 2

    # Ramp rate
    for p in range(P):
        for t in range(1, T):
            delta = abs(generation[p, t] - generation[p, t - 1])
            if delta > ramp_rate[p]:
                penalty += (delta - ramp_rate[p]) ** 2

    # Min/max output
    for p in range(P):
        for t in range(T):
            g = generation[p, t]
            if g > 0 and g < min_output[p]:
                penalty += (min_output[p] - g) ** 2
            if g > max_output[p]:
                penalty += (g - max_output[p]) ** 2

    # Renewable limits
    for p in range(P):
        if plant_type[p] == "Renewable":
            for t in range(T):
                if generation[p, t] > renewable_availability[p][t]:
                    penalty += (generation[p, t] - renewable_availability[p][t]) ** 2

    return cost + penalty_weight * penalty

def optimize_dfo(data, method="Nelder-Mead", verbose=True):
    P = data["P"]
    T = data["T"]
    x0 = np.full(P * T, 1.0)  # Start with minimal generation

    result = minimize(
        simulate_cost,
        x0,
        args=(data,),
        method=method,
        options={"maxiter": 10000, "disp": verbose}
    )

    return result

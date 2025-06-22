import json

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Sanity check for required keys
    required_keys = [
        "P", "T", "plant_type", "cost_per_unit", "fixed_cost", "min_output",
        "max_output", "ramp_rate", "emissions", "emission_limit",
        "demand", "transmission_cap", "renewable_availability"
    ]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required field in input data: {key}")

    return data

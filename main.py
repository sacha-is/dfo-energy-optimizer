import os
import json
from optimizer import optimize_dfo  # Replace with your actual solver function

DATA_DIR = "data"

def load_instance(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def main():
    for file_name in sorted(os.listdir(DATA_DIR)):
        if file_name.endswith(".json"):
            path = os.path.join(DATA_DIR, file_name)
            print(f"\n--- Solving {file_name} ---")
            try:
                instance = load_instance(path)
                result = optimize_dfo(instance)
                print(f"Result for {file_name}: {result}")
            except Exception as e:
                print(f"❌ Error solving {file_name}: {e}")

if __name__ == "__main__":
    main()

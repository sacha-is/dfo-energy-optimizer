import json
import os
from optimizer import optimize_dfo
from data_loader import load_data
from plotting import plot_generation_schedule

DATA_DIR = "data"
PLOT_DIR = "plots"

def main():
    for filename in sorted(os.listdir(DATA_DIR)):
        if filename.endswith(".json"):
            print(f"\n--- Solving {filename} ---")
            filepath = os.path.join(DATA_DIR, filename)
            try:
                data = load_data(filepath)
                result = optimize_dfo(data)
                if result.success:
                    print(f"Success. Final cost: {result.fun:.2f}")
                    plot_path = os.path.join(PLOT_DIR, filename.replace(".json", ".png"))
                    plot_generation_schedule(result, data, save_path=plot_path)
                    print(f"📊 Plot saved to {plot_path}")
                else:
                    print(f"Optimization failed: {result.message}")
            except Exception as e:
                print(f"Error solving {filename}: {e}")

if __name__ == "__main__":
    main()

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
                methods = ["Nelder-Mead", "Powell", "CG"]
                results = {}
                for method in methods:
                    print(f"  Running optimizer with method: {method}")
                    result = optimize_dfo(data, method=method)
                    results[method] = result
                    plot_filename = filename.replace(".json", f"_{method}.png")
                    plot_path = os.path.join(PLOT_DIR, plot_filename)
                    if result.success:
                        plot_generation_schedule(result, data, save_path=plot_path)
                        print(f"  Plot saved to {plot_path}")
                    else:
                        print(f"  Optimization failed: {result.message}")
                best_method = min(
                    (m for m in methods if results[m].success),
                    key=lambda m: results[m].fun,
                    default=None
                )
                if best_method:
                    result = results[best_method]
                    print(f"The best method is {best_method} with objective value: {result.fun}")
            except Exception as e:
                print(f"Error solving {filename}: {e}")

if __name__ == "__main__":
    main()

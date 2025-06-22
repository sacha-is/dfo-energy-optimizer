import numpy as np
import matplotlib.pyplot as plt
import os

def plot_generation_schedule(result, data, save_path=None):
    P = data["P"]
    T = data["T"]
    generation = np.clip(result.x, 0, None).reshape((P, T))
    plant_labels = [f"Plant {p+1}" for p in range(P)]

    plt.figure(figsize=(12, 6))
    for p in range(P):
        plt.plot(range(T), generation[p], label=plant_labels[p])

    plt.xlabel("Time Period")
    plt.ylabel("Generation (MW)")
    plt.title("Generation Schedule per Plant")
    plt.legend()
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

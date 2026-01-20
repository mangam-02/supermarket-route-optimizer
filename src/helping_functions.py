import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


def plot_costs(list_of_costs, shopping_list, saving_path=None):
    fig = plt.figure(figsize=(10,6))

    # Bins mit Breite 2
    min_cost = int(min(list_of_costs))
    max_cost = int(max(list_of_costs))
    # Mittelwert und Standardabweichung
    mean_cost = np.mean(list_of_costs)
    std_cost = np.std(list_of_costs)

    ## FIT
    # x-Werte für die Kurve
    x = np.linspace(min_cost, max_cost, 200)
    # y-Werte für die Gauß-Kurve
    y = norm.pdf(x, loc=mean_cost, scale=std_cost) * len(list_of_costs) * 2  # *2 wegen bin-width=2
    plt.plot(x, y, color='orange', linewidth=2, label='Normal Fit')



    ## Stats
    bins = np.arange(min_cost, max_cost + 2, 2)  # Schrittweite 2

    plt.hist(list_of_costs, bins=bins, color="#1f77b4", edgecolor="black", alpha=0.7)
    
    # Anzahl der Datenpunkte
    m_data = len(list_of_costs)
    n = len(shopping_list)

    plt.title(f"Distribution of Best Order Costs (m = {m_data}) (n = {n})", fontsize=16, fontweight="bold")
    plt.xlabel("Order Cost (Time)", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.5)

    # Linien für Mittelwert + Standardabweichung und beste Lösung
    plt.axvline(mean_cost, color="red", linestyle="dashed", linewidth=2,
                label=f"Mean = {mean_cost:.2f} ± {std_cost:.2f}")
    best_cost = min(list_of_costs)
    plt.axvline(best_cost, color="green", linestyle="solid", linewidth=2,
                label=f"Best = {best_cost:.0f}")

    plt.legend(fontsize=12)
    plt.tight_layout()
    
    if saving_path is not None:
        plt.savefig(saving_path, bbox_inches="tight", dpi=300)
    
    return mean_cost, std_cost

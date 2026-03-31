import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import os


def check_saving_path(saving_path: str) -> str:
    """
    Prüft den saving_path:
    - Wenn saving_path keinen Unterordner enthält, wird er zu assets/figures/ verschoben.
    - Andernfalls bleibt er unverändert.
    """
    if os.path.dirname(saving_path) == "":
        os.makedirs("assets/figures", exist_ok=True)
        saving_path = os.path.join("assets/figures", saving_path)
    return saving_path

def plot_costs(list_of_costs, shopping_list = None, saving_path=None):
    fig = plt.figure(figsize=(10,6))

    # Bins mit Breite 2
    min_cost = int(min(list_of_costs))
    max_cost = int(max(list_of_costs))
    # Mittelwert und Standardabweichung
    mean_cost = np.mean(list_of_costs)
    std_cost = np.std(list_of_costs)

    ## Stats
    bins = np.arange(min_cost, max_cost + 2, 2)  # Schrittweite 2

    plt.hist(list_of_costs, bins=bins, color="#1f77b4", edgecolor="black", alpha=0.7)
    
    # Anzahl der Datenpunkte
    m_data = len(list_of_costs)
    title = f"Distribution of Best Order Costs (m = {m_data})"
    if shopping_list:
        n = len(shopping_list)
        title += f" (n = {n})"
    plt.title(title, fontsize=16, fontweight="bold")
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
        saving_path = check_saving_path(saving_path)
        plt.savefig(saving_path, bbox_inches="tight", dpi=300)
    
    return mean_cost, std_cost

def plot_2d_history_costs(history_list, xlabel="Distance cost", ylabel="Weight cost", cmap='viridis', marker='x', s=60, alpha=0.9, line_color='0.7', line_width=1.0, saving_path=None):
    """Scatter-Plot mit Farbverlauf nach Iteration und verbindender Linie.

    Punkte bleiben als Kreuz (`marker='x'`) gefärbt nach Iteration; zusätzlich wird
    eine dünne graue Linie in der Reihenfolge der Iterationen gezeichnet.
    """
    distance_costs = [h[1] for h in history_list]
    weight_costs = [h[2] for h in history_list]
    iterations = list(range(len(history_list)))

    plt.figure()
    # Verbindungslinie in vorgegebener Reihenfolge (leicht grau)
    plt.plot(distance_costs, weight_costs, '-', color=line_color, linewidth=line_width, zorder=1)

    # Scatter überlagert, farblich nach Iteration (Cross-Marker)
    sc = plt.scatter(distance_costs, weight_costs, c=iterations, cmap=cmap, marker=marker, s=s, alpha=alpha, zorder=2)
    cbar = plt.colorbar(sc)
    cbar.set_label('Iteration')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title('History: Distance vs Weight Costs')
    plt.grid(True)
    plt.tight_layout()

    if saving_path is not None:
        import plotting as _plotting
        saving_path = _plotting.check_saving_path(saving_path)
        plt.savefig(saving_path, bbox_inches="tight", dpi=400)

    plt.show()

def compare_2d_populations(population1, population2, shopping_list, J_product, xlabel="Cost x", ylabel="Cost y", population1_label = "Population 1", population2_label = "Population_2", saving_path=None):
    import evolution_2d
    import evolution
    import plotting
    ranking_1, pareto_front_1, pareto_ranks_1, crowding_distances_1, weight_costs_1, distance_costs_1 = evolution_2d.evaluate_population_2d(population1, shopping_list, J_product)
    ranking_2, pareto_front_2, pareto_ranks_2, crowding_distances_2, weight_costs_2, distance_costs_2 = evolution_2d.evaluate_population_2d(population2, shopping_list, J_product)
    population1, pareto_ranks_1, ranking_1, weight_costs_1, distance_costs_1 = evolution.filter_best_pareto_rank(population1, pareto_ranks_1, ranking_1, weight_costs_1, distance_costs_1)
    population2, pareto_ranks_2, ranking_2, weight_costs_2, distance_costs_2 = evolution.filter_best_pareto_rank(population2, pareto_ranks_2, ranking_2, weight_costs_2, distance_costs_2)
    plt.figure()
    plt.scatter(distance_costs_1, weight_costs_1, label=population1_label, marker="x")
    plt.scatter(distance_costs_2, weight_costs_2, label=population2_label, marker="x")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title("Pareto Front")
    plt.legend(
        # loc="center left",
        # bbox_to_anchor=(1.02, 0.5),
        # borderaxespad=0
        )
    plt.tight_layout()
    if saving_path is not None:
        saving_path = plotting.check_saving_path(saving_path)
        plt.savefig(saving_path, bbox_inches="tight", dpi=300)

import imageio
import os
import evolution_2d

def create_pareto_gif_from_history(history_list, filename="assets/pareto_evolution.gif", duration=0.5, tmp_folder="_tmp_gif"):
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    images = []
    tmp_files = []  # <- speichert die Dateipfade

    for gen, gen_data in enumerate(history_list):
        pareto_ranks = gen_data["pareto_ranks"]
        weight_costs = gen_data["weight_costs"]
        distance_costs = gen_data["distance_costs"]
        
        tmp_file = os.path.join(tmp_folder, f"gen_{gen}.png")
        tmp_files.append(tmp_file)
        
        evolution_2d.plot_pareto_2(
            pareto_ranks, distance_costs, weight_costs,
            xlabel="Distance cost",
            ylabel="Weight cost",
            max_legend_ranks=6,
            plot_high_ranks=True,
            reference_point=None,
            saving_path=tmp_file
        )
        
        images.append(imageio.imread(tmp_file))
    
    # GIF speichern
    imageio.mimsave(filename, images, duration=duration)
    
    # Temporäre PNGs löschen
    for file_path in tmp_files:
        os.remove(file_path)
    os.rmdir(tmp_folder)
    
    print(f"GIF saved as {filename}")
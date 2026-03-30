import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import plotting
import os

class Zelle:
    def __init__(self, row, column, width, height, N, E, S, W):
        # N,E,S,W können sein: 0 (Gang), 1 (Wand), str (Regaltyp)
        self.seiten = {"N": N, "E": E, "S": S, "W": W}
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        
    def save(self):
        text = str(self.row) + ", " + str(self.column) + ", " + str(self.seiten)
        return text

class Grid:
    def __init__(self, path:str = None, grid_size:tuple = None):
        if path is not None:
            self.load(path)
        elif grid_size is not None:
            self.create_grid(grid_size)

    def plot(self, person_path:list = [], saving_path:str = None):
        grid = self.grid
        fig, ax = plt.subplots(figsize=(6, 6))
        rows, cols = grid.shape

        # Farben je Regaltyp sammeln (automatisch)
        regal_colors = {}
        color_cycle = plt.cm.tab20.colors
        color_idx = 0

        for r in range(rows):
            for c in range(cols):
                z = grid[r, c]
                x = c * z.width
                y = (rows - 1 - r) * z.height
                
                # Zelle zeichnen (Umriss)
                rect = Rectangle((x, y), z.width, z.height,
                                fill=False, edgecolor="black", linewidth=0.5,
                                linestyle=":")
                ax.add_patch(rect)

                # Jede Seite logik
                for side, val in z.seiten.items():
                    # Koordinaten der Seite bestimmen
                    if side == "N":
                        x0, x1 = x, x + z.width
                        y0 = y1 = y + z.height
                        offset = -0.1 * z.height
                    elif side == "S":
                        x0, x1 = x, x + z.width
                        y0 = y1 = y
                        offset = 0.1 * z.height
                    elif side == "E":
                        x0 = x1 = x + z.width
                        y0, y1 = y, y + z.height
                        offset = -0.1 * z.width
                    elif side == "W":
                        x0 = x1 = x
                        y0, y1 = y, y + z.height
                        offset = 0.1 * z.width
                    else:
                        continue

                    # Fall 1: Gang (0) -> nichts zeichnen
                    if val == 0:
                        continue

                    # Fall 2: Wand (1) -> dicke schwarze Linie
                    if val == 1:
                        ax.plot([x0, x1], [y0, y1], linewidth=2.5, color="black")
                        continue

                    # Fall 3: Regal (str) -> eingezogene gefärbte Linie
                    if isinstance(val, str):
                        # Farbe zuordnen
                        if val not in regal_colors:
                            regal_colors[val] = color_cycle[color_idx % len(color_cycle)]
                            color_idx += 1

                        col = regal_colors[val]

                        # Auch Wand zeichnen
                        ax.plot([x0, x1], [y0, y1], linewidth=2.5, color="black")

                        # Eingeschobene Linie: je nach Richtung verschieben
                        if side in ["N", "S"]:
                            ax.plot([x0, x1], [y0 + offset, y1 + offset],
                                    linewidth=1.8, color=col)
                        else:
                            ax.plot([x0 + offset, x1 + offset], [y0, y1],
                                    linewidth=1.8, color=col)

        if person_path:  # nur, wenn ein Pfad existiert
            import matplotlib.cm as cm
            import matplotlib.colors as mcolors

            cmap = cm.viridis
            total_segments = sum(len(path)-1 for path in person_path)  # alle Segmente
            seg_idx = 0  # globaler Segmentzähler

            for path in person_path:
                path_x = [c + 0.5 for r, c in path]
                path_y = [grid.shape[0] - 1 - r + 0.5 for r, c in path]

                n = len(path_x)
                for i in range(n - 1):
                    color = cmap(seg_idx / total_segments)
                    ax.plot([path_x[i], path_x[i + 1]], [path_y[i], path_y[i + 1]],
                            color=color, linewidth=2, linestyle="--")
                    seg_idx += 1

            # Horizontal Colorbar unterhalb des Plots
            norm = mcolors.Normalize(vmin=0, vmax=total_segments)
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])

            cbar = fig.colorbar(sm, ax=ax, orientation="horizontal",
                                fraction=0.046, pad=0.01)
            cbar.set_label("Progress along path")
            cbar.set_ticks([0, total_segments])
            cbar.set_ticklabels(["start", "end"])
        # Achsen konfigurieren
        ax.set_aspect("equal")
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.set_xticks([])
        ax.set_yticks([])

        # Legende erzeugen
        legend_elements = [Line2D([0], [0], color='black', lw=2.5, label="Wand")]
        for name, col in regal_colors.items():
            legend_elements.append(
                Line2D([0], [0], color=col, lw=1.8, label=f"{name}")
            )
        ax.legend(handles=legend_elements, bbox_to_anchor=(1.02, 1),loc="upper left")
        if saving_path is not None:
            saving_path = plotting.check_saving_path(saving_path)
            plt.savefig(saving_path, bbox_inches="tight", dpi=300)
        #plt.show()

    def save(self, save_path):
        # Default folder
        default_dir = "supermarket-grids"
        
        # If no subdirectory specified → use default_dir
        if "/" not in save_path and "\\" not in save_path:
            save_path = os.path.join(default_dir, save_path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        grid = self.grid
        text = ""
        grid_shape = grid.shape
        for r in range(grid_shape[0]):
            for c in range(grid_shape[1]):
                cell_text = grid[r,c].save()
                text += cell_text
                text += "\n"
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(text)

    def create_grid(self, grid_size):
        grid = np.empty(grid_size, dtype=object)
        for r in range(grid_size[0]):
            for c in range(grid_size[1]):
                grid[r, c] = Zelle(row = r, column = c, width = 1, height = 1, N=0, E=0, S=0, W=0)
        self.grid = grid

    def load(self, path):
        # Datei einlesen
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Erst Größe bestimmen
        # Jede Zeile hat Format: "r, c, {dict}"
        coords = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            left, right = line.split(",", 1)  # r und Rest
            r = int(left.strip())
            # zweite Zahl extrahieren
            c_str, rest = right.split(",", 1)
            c = int(c_str.strip())
            coords.append((r, c))

        if not coords:
            raise ValueError("Datei ist leer.")

        max_r = max(r for r, _ in coords)
        max_c = max(c for _, c in coords)
        rows = max_r + 1
        cols = max_c + 1

        # Grid anlegen
        grid = np.empty((rows, cols), dtype=object)
        for r in range(rows):
            for c in range(cols):
                grid[r, c] = Zelle(row=r, column=c, width=1, height=1, N=0, E=0, S=0, W=0)

        # Inhalte füllen
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Zerlegen
            # Beispiel: "0, 2, {'N': 'Käse', 'E': 0, 'S': 0, 'W': 'Fisch'}"
            parts = line.split(",", 2)
            r = int(parts[0].strip())
            c = int(parts[1].strip())

            # Dictionary-String bereinigen
            dict_str = parts[2].strip()
            # dict_str beginnt mit "{'N': ..." -> direkt evaluierbar
            seiten = eval(dict_str)  # hier ok, da Format unter eigener Kontrolle

            # In grid schreiben
            z = grid[r, c]
            z.seiten = seiten

        self.grid = grid

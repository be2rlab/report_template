import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, Optional


class LaTeXPlotter:

    COLORS = [
        "#1b9e77",  # teal
        "#d95f02",  # orange
        "#7570b3",  # lavender
        "#e7298a",  # pink
        "#66a61e",  # lime
        "#e6ab02",  # gold
        "#a6761d",  # ochre
        "#666666",  # medium gray
        "#e41a1c",  # vermillion
        "#377eb8",  # steel blue
        "#4daf4a",  # green
        "#984ea3",  # purple
        "#ff7f00",  # dark orange
        "#ffff33",  # yellow
        "#a65628",  # brown
        "#f781bf"   # light pink
    ]
    
    def __init__(self):
        self._base_font_size = 12
        self._setup_style(scale=1.0)
    
    def _setup_style(self, scale: float = 1.0):
        plt.rcParams.update({
            "text.usetex": True,
            "font.family": "serif",
            "font.serif": ["Times New Roman"],
            "font.size": 12 * scale,
            "axes.labelsize": 12 * scale,
            "legend.fontsize": 8 * scale,
            "xtick.labelsize": 8 * scale,
            "ytick.labelsize": 8 * scale,
            "axes.titlesize": 12 * scale,
            "lines.linewidth": 1.0,
            "text.latex.preamble": r"""
                \usepackage[english,russian]{babel}
                \usepackage[T2A]{fontenc}
                \usepackage[utf8]{inputenc}
            """
        })
    
    def create_figure(self, grid_shape: Tuple[int, int] = (1, 1)):
        
        width_cm, height_cm = self._calculate_dimensions(grid_shape)
        fig, axes = plt.subplots(*grid_shape, figsize=(width_cm/2.54, height_cm/2.54))
        
        if isinstance(axes, plt.Axes):
            axes = np.array([axes])
        
        for ax in axes.flat:
            self._setup_axes(ax)
        
        plt.subplots_adjust(
            left=0.15,
            right=0.95,
            bottom=0.1,
            top=0.95,
            wspace=0.3,
            hspace=0.3,
        )
        
        return fig, axes
    
    def _calculate_dimensions(self, grid_shape: Tuple[int, int]):
        base_width_cm = 15.0
        
        special_aspects = {
            (1, 1): 3.0,   # width:height = 3:1
            (2, 1): 2.5,    # 5:2
            (3, 1): 1.5,    # 3:2
            (4, 1): 1.25,    # 5:4
            (1, 2): 3.0,
            (1, 3): 3.0,
            (1, 4): 3.0,
            (2, 2): 2.5            
        }
        
        if grid_shape in special_aspects:
            aspect_ratio = special_aspects[grid_shape]
            return (base_width_cm, base_width_cm / aspect_ratio)
        
        rows, cols = grid_shape
        
        row_factor = 0.8 ** (rows - 1)
        col_factor = 0.9 ** (cols - 1)
        
        width = base_width_cm * col_factor
        height = (base_width_cm / 3) * row_factor
        
        min_width = 8.0
        min_height = 4.0
        
        return (max(width, min_width), max(height, min_height))
    
    def _setup_axes(self, ax: plt.Axes):
        ax.spines[['top', 'right']].set_visible(False)
        ax.spines['left'].set_position('zero')
        
        ax.grid(True, linestyle=':', alpha=0.5, color='#D3D3D3')
        
        # dafault lables because any figure MUST have it
        ax.set_xlabel(r'$x$, sec', loc='center')
        ax.set_ylabel(r'$y$, rad', loc='center')
    
    def set_axis_labels(self, ax: plt.Axes, 
                       xlabel: Optional[str] = None, 
                       ylabel: Optional[str] = None,
                       xunits: str = 'sec',
                       yunits: str = 'rad'):
        if xlabel is not None:
            ax.set_xlabel(fr'${xlabel}$, {xunits}', loc='center')
        if ylabel is not None:
            ax.set_ylabel(fr'${ylabel}$, {yunits}', loc='center')
    
    def save(self, filename: str = "plot.pdf", dpi: int = 50):
        plt.savefig(
            filename,
            bbox_inches='tight',
            dpi=dpi,
            pad_inches=0.05
        )
        plt.close()
        print(f"Plot saved to {filename}")


def example():
    from itertools import product
    
    # test data
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.cos(2 * x)

    aspect_combinations = list(product([1, 2, 3], repeat=2))

    for dx, dy in aspect_combinations:
        plotter = LaTeXPlotter()
        fig, axes = plotter.create_figure((dx, dy))
        
        if dx == 1 or dy == 1:
            axes = np.array([axes]).flatten()
        else:
            axes = axes.flatten()

        for i, ax in enumerate(axes):
            ax.plot(x, y, color=plotter.COLORS[i])
            plotter.set_axis_labels(ax, 't', 'A', 'сек', 'рад')

        plotter.save(f"example_{dx}x{dy}.pdf")


if __name__ == "__main__":

    # import pandas as pd
    # def read_csv(filename: str):
    #     data = pd.read_csv(filename)
    #     return data['x'].values, data['y'].values

    # import json
    # def read_json(filename: str):
    #     # for json structure: {'x': [...], 'y': [...]}
    #     with open(filename) as f:
    #         data = json.load(f)
    #     return np.array(data['x']), np.array(data['y'])

    example()

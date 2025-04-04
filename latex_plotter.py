import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, Optional

class LaTeXPlotter:

    COLORS = [
        "#1b9e77",
        "#d95f02",
        "#7570b3",
        "#e7298a",
        "#66a61e",
        "#e6ab02"
    ]
    
    def __init__(self):
        self._setup_style()
    
    def _setup_style(self):
        plt.rcParams.update({
            "text.usetex": True,
            "font.family": "serif",
            "font.serif": ["Times New Roman"],
            "font.size": 10,
            "axes.labelsize": 8,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "axes.titlesize": 10,
            "lines.linewidth": 0.5,
            "text.latex.preamble": r"""
                \usepackage[english,russian]{babel}
                \usepackage[T2A]{fontenc}
                \usepackage[utf8]{inputenc}
            """
        })
    
    def create_figure(self, grid_shape: Tuple[int, int] = (1, 1)) -> Tuple[plt.Figure, np.ndarray]:
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
            wspace=0.5,
            hspace=0.5
        )
        
        return fig, axes
    
    def _calculate_dimensions(self, grid_shape: Tuple[int, int]) -> Tuple[float, float]:
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
        ax.set_xlabel(r'$x$, sec', loc='center')
        ax.set_ylabel(r'$y$, rad', loc='center')
        
        ax.yaxis.set_label_coords(-0.1, 0.98)
    
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
    
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.cos(2 * x)

    aspect_combinations = list(product([1, 2, 3, 4], repeat=2))

    for dx, dy in aspect_combinations:
        plotter = LaTeXPlotter()
        fig, axes = plotter.create_figure((dx, dy))
        
        if dx == 1 or dy == 1:
            axes = np.array([axes]).flatten()
        else:
            axes = axes.flatten()

        for i, ax in enumerate(axes):
            ax.plot(x, y, color=plotter.COLORS[i])
            plotter.set_axis_labels(ax, 't', 'A', 'sec', 'rad')

        plotter.save(f"example_{dx}x{dy}.pdf")

def example1x1():
    plotter = LaTeXPlotter()
    x = np.linspace(-3, 3, 100)
    
    fig, ax = plotter.create_figure((1, 1))
    
    ax[0].plot(x, np.sin(x), color=plotter.COLORS[0], label=r'$\sin(x)$')
    ax[0].plot(x, np.cos(x), color=plotter.COLORS[1], label=r'$\cos(x)$')
    
    plotter.set_axis_labels(ax[0], 't', 'value', 'sec', 'rad')
    ax[0].legend()
    ax[0].set_xlim(-3, 3)
    ax[0].set_ylim(-1.5, 1.5)
    plotter.save("example1x1.pdf")

def example2x1():
    plotter = LaTeXPlotter()
    x = np.linspace(0, 10, 1000)
    
    fig, axes = plotter.create_figure((2, 1))
    
    for i in range(2):
        axes[i].plot(x, np.sin(2*(i+1)*x) * 1.2 * (i+1), color=plotter.COLORS[i])
        plotter.set_axis_labels(axes[i], 't', '\\sin(t)', 'sec', 'rad')

    plotter.save("example_2x1.pdf")
    
def example4x1():
    plotter = LaTeXPlotter()
    x = np.linspace(0, 10, 100)
    
    fig, axes = plotter.create_figure((4, 1))
    
    for i in range(4):
        axes[i].plot(x, np.sin(2*(i+1)*x) * 1.2 * (i+1), color=plotter.COLORS[i])
        plotter.set_axis_labels(axes[i], 't', '\\sin(t)', 'sec', 'rad')

    plotter.save("example_4x1.pdf")

def example1x2():
    plotter = LaTeXPlotter()
    x = np.linspace(0, 10, 100)
    
    fig, axes = plotter.create_figure((1, 2))
    
    for i in range(2):
        axes[i].plot(x, np.sin(2*(i+1)*x) * 1.2 * (i+1), color=plotter.COLORS[i])
        plotter.set_axis_labels(axes[i], 't', '\\sin(t)', 'sec', 'rad')

    plotter.save("example_1x2.pdf")

def example2x2():
    plotter = LaTeXPlotter()
    x = np.linspace(0, 10, 100)
    
    fig, axes = plotter.create_figure((2, 2))
    for i in range(2):
        for j in range(2):
            axes[i][j].plot(x, np.sin(2*(i+1) * (j + 1)*x) * 1.2 * (i+1), color=plotter.COLORS[i])
            plotter.set_axis_labels(axes[i][j], 't', '\\sin(t)', 'sec', 'rad')

    plotter.save("example_2x2.pdf")

if __name__ == "__main__":
    example()

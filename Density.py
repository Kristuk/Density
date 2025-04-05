import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox
from matplotlib.ticker import FuncFormatter

class AtomDensityVisualization:
    def __init__(self):
        self.total_size = 1.0
        self.max_display_atoms = 100000
        self.default_density = 1e8
        self.min_zoom, self.max_zoom = 1, 1e11

        plt.close('all')
        self.fig = plt.figure(figsize=(12, 7))
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Scientific notation formatter
        def sci_formatter(x, pos):
            return '0' if x == 0 else f'$10^{{{int(np.floor(np.log10(abs(x))))}}}$'

        for axis in [self.ax.xaxis, self.ax.yaxis, self.ax.zaxis]:
            axis.set_major_formatter(FuncFormatter(sci_formatter))
            # Set only first and last ticks
            axis.set_ticks([0, self.total_size])

        # Zoom slider
        self.ax_zoom = self.fig.add_axes([0.2, 0.02, 0.6, 0.03])
        self.zoom_slider = Slider(
            self.ax_zoom, 'Zoom', 
            np.log10(self.min_zoom), np.log10(self.max_zoom), 
            valinit=0, valstep=0.5
        )
        self.zoom_slider.on_changed(self.update_plot)

        # Density input box
        self.ax_box = self.fig.add_axes([0.2, 0.07, 0.2, 0.04])
        self.text_box = TextBox(
            self.ax_box, 
            "Density (atoms/m³)", 
            initial=f"{self.default_density:.2e}"
        )
        self.text_box.on_submit(self.update_density)

        # Initial setup
        self.viewport_size = self.total_size
        self.current_density = self.default_density
        self.update_plot(0)

        self.fig.subplots_adjust(bottom=0.2)
        plt.show()

    def generate_atoms(self, density, viewport_size):
        viewport_volume = viewport_size ** 3
        total_atoms = int(density * viewport_volume)
        n_atoms_display = min(total_atoms, self.max_display_atoms)
        atoms = np.random.random((n_atoms_display, 3)) * viewport_size
        return atoms, total_atoms
    
    def atom_seperation(self, total_atoms):
        if total_atoms > 0:
            return (1/self.current_density)**(1/3)
        else:
            return 0
        
        
        
    def update_density(self, density_str):
        try:
            self.current_density = float(density_str)
            self.update_plot(self.zoom_slider.val)
        except ValueError:
            print("Invalid density input.")

    def update_plot(self, zoom_log):
        zoom = 10 ** zoom_log
        self.ax.clear()

        # Reapply scientific notation formatter
        def sci_formatter(x, pos):
            return '0' if x == 0 else f'$10^{{{int(np.floor(np.log10(abs(x))))}}}$'

        for axis in [self.ax.xaxis, self.ax.yaxis, self.ax.zaxis]:
            axis.set_major_formatter(FuncFormatter(sci_formatter))
            # Set only first and last ticks
            axis.set_ticks([0, self.total_size / zoom])

        # Calculate and generate atoms
        self.viewport_size = self.total_size / zoom
        atoms, total_atoms = self.generate_atoms(self.current_density, self.viewport_size)
        
        atom_seperation = self.atom_seperation(total_atoms)
        seperation_sci = f"{atom_seperation: .2e}"

        # Plot atoms
        self.ax.scatter(
            atoms[:, 0], atoms[:, 1], atoms[:, 2], 
            s=1, alpha=1, c='blue', edgecolors='none'
        )

        # Set axis properties
        for label in ['x', 'y', 'z']:
            getattr(self.ax, f'set_{label}label')(f'{label.upper()} (m)', fontsize=8)
            getattr(self.ax, f'{label}axis').set_tick_params(labelsize=7)

        # Set axis limits
        for axis in ['x', 'y', 'z']:
            getattr(self.ax, f'set_{axis}lim')(0, self.viewport_size)

        # Add title
        self.ax.set_title(
            f'Atom Distribution\n'
            f'Density: {self.current_density:.2e} atoms/m³ | '
            f'Total Atoms: {total_atoms:,} | '
            f'Average seperation between atoms: {seperation_sci:} m',
            fontsize=10
        )

        self.fig.canvas.draw_idle()

# Launch the visualization
AtomDensityVisualization()
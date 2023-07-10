# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.patches import Polygon
from matplotlib.widgets import PolygonSelector

# Load data from the .dat file
data = np.loadtxt('./DATA/data_res.dat')

# Extract distance, depth, resistivity, and conductivity
distance = data[:, 0]
depth = data[:, 1]
resistivity = data[:, 2]
conductivity = data[:, 3]

# Define the grid for the tomography plot
grid_resolution = 100  # Adjust this value for desired resolution
xi = np.linspace(min(distance), max(distance), grid_resolution)
yi = np.linspace(min(depth), max(depth), grid_resolution)
xi, yi = np.meshgrid(xi, yi)

# Perform grid data interpolation
interp_tri = tri.Triangulation(distance, depth)
interp_lin = tri.LinearTriInterpolator(interp_tri, resistivity)
resistivity_interp = interp_lin(xi, yi)

# Create the tomography plot
fig, ax = plt.subplots(figsize=(12, 4), num='L456 - ERtomo')
image = ax.imshow(resistivity_interp, origin='lower', extent=(min(distance), max(distance), min(depth), max(depth)), aspect='auto', cmap='jet')
scatter = ax.scatter(distance, depth, c=resistivity, cmap='jet', edgecolors='k', alpha=0.5, marker='o')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Depth (m)')
ax.set_title('2D Electrical Resistivity Tomography')

# Add a colorbar
colorbar = plt.colorbar(scatter)
colorbar.set_label('Resistivity')
colorbar.ax.yaxis.set_label_coords(-1.5, 0.5)  # Adjust the position of the label

# Increase the colorbar saturation
colorbar.solids.set(alpha=1)

# Define a list to store the polygon coordinates
polygon_coords = []

# Function to update the plot with the polygon
def update_polygon(selected_polygon):
    polygon = Polygon(selected_polygon, closed=True, fill=None, edgecolor='red')
    ax.add_patch(polygon)
    plt.draw()

# Function to handle mouse events
def onselect(verts):
    if len(verts) > 2:
        selected_polygon = np.array(verts)
        update_polygon(selected_polygon)

# Create the PolygonSelector
poly_selector = PolygonSelector(ax, onselect)

# Save the plot
plt.savefig('tomography_plot.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()

# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

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
plt.figure(figsize=(8, 2), num='L456 - ERtomo')
plt.imshow(resistivity_interp, origin='lower', extent=(min(distance), max(distance), min(depth), max(depth)), aspect='auto', cmap='jet')
plt.colorbar(label='Resistivity')
plt.scatter(distance, depth, c=resistivity, cmap='jet', edgecolors='k', alpha=0.1)
plt.xlabel('Distance (m)')
plt.ylabel('Depth (m)')
plt.title('2D Electrical Resistivity Tomography')
plt.show()
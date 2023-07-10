import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.patches import Polygon
from matplotlib.widgets import PolygonSelector
from tkinter import Tk, filedialog, Button, Menu


def create_plots():
    # Load data from the .dat file
    data = np.loadtxt(data_file_path)

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

    # Perform grid data interpolation for Resistivity
    interp_tri_res = tri.Triangulation(distance, depth)
    interp_lin_res = tri.LinearTriInterpolator(interp_tri_res, resistivity)
    resistivity_interp = interp_lin_res(xi, yi)

    # Create the tomography plot for Resistivity
    fig_res, ax_res = plt.subplots(figsize=(12, 4), num='L456 - ERtomo Resistivity')
    image_res = ax_res.imshow(resistivity_interp, origin='lower',
                              extent=(min(distance), max(distance), min(depth), max(depth)),
                              aspect='auto', cmap='jet')
    scatter_res = ax_res.scatter(distance, depth, c=resistivity, cmap='jet', edgecolors='k', alpha=0.5, marker='o')
    ax_res.set_xlabel('Distance (m)')
    ax_res.set_ylabel('Depth (m)')
    ax_res.set_title('2D Electrical Resistivity Tomography (Resistivity)')

    # Add a colorbar for Resistivity
    colorbar_res = plt.colorbar(scatter_res)
    colorbar_res.set_label('Resistivity')
    colorbar_res.ax.yaxis.set_label_coords(-1.5, 0.5)  # Adjust the position of the label

    # Increase the colorbar saturation for Resistivity
    colorbar_res.solids.set(alpha=1)

    # Define a list to store the polygon coordinates for Resistivity
    polygon_coords_res = []

    # Function to update the plot with the polygon for Resistivity
    def update_polygon_res(selected_polygon):
        polygon = Polygon(selected_polygon, closed=True, fill=None, edgecolor='red')
        ax_res.add_patch(polygon)
        plt.draw()

    # Function to handle mouse events for Resistivity
    def onselect_res(verts):
        if len(verts) > 2:
            selected_polygon = np.array(verts)
            update_polygon_res(selected_polygon)

    # Create the PolygonSelector for Resistivity
    poly_selector_res = PolygonSelector(ax_res, onselect_res)

    # Perform grid data interpolation for Conductivity
    interp_tri_con = tri.Triangulation(distance, depth)
    interp_lin_con = tri.LinearTriInterpolator(interp_tri_con, conductivity)
    conductivity_interp = interp_lin_con(xi, yi)

    # Create the tomography plot for Conductivity
    fig_con, ax_con = plt.subplots(figsize=(12, 4), num='L456 - ERtomo Conductivity')
    image_con = ax_con.imshow(conductivity_interp, origin='lower',
                              extent=(min(distance), max(distance), min(depth), max(depth)),
                              aspect='auto', cmap='jet')
    scatter_con = ax_con.scatter(distance, depth, c=conductivity, cmap='jet', edgecolors='k', alpha=0.5, marker='o')
    ax_con.set_xlabel('Distance (m)')
    ax_con.set_ylabel('Depth (m)')
    ax_con.set_title('2D Electrical Resistivity Tomography (Conductivity)')

    # Add a colorbar for Conductivity
    colorbar_con = plt.colorbar(scatter_con)
    colorbar_con.set_label('Conductivity')
    colorbar_con.ax.yaxis.set_label_coords(-1.5, 0.5)  # Adjust the position of the label

    # Increase the colorbar saturation for Conductivity
    colorbar_con.solids.set(alpha=1)

    # Define a list to store the polygon coordinates for Conductivity
    polygon_coords_con = []

    # Function to update the plot with the polygon for Conductivity
    def update_polygon_con(selected_polygon):
        polygon = Polygon(selected_polygon, closed=True, fill=None, edgecolor='red')
        ax_con.add_patch(polygon)
        plt.draw()

    # Function to handle mouse events for Conductivity
    def onselect_con(verts):
        if len(verts) > 2:
            selected_polygon = np.array(verts)
            update_polygon_con(selected_polygon)

    # Create the PolygonSelector for Conductivity
    poly_selector_con = PolygonSelector(ax_con, onselect_con)

    # Show the plots
    plt.show()


def select_data_file():
    global data_file_path
    # Ask for the .dat file using a file dialog
    data_file_path = filedialog.askopenfilename(title="Select .dat Data File", filetypes=[("DAT Files", "*.dat")])

    # Check if a file was selected
    if not data_file_path:
        print("No input file selected.")
        return

    create_plots()


def exit_application():
    plt.close('all')  # Close all matplotlib figures
    root.destroy()  # Destroy the Tkinter root window


# Create the main Tkinter window
root = Tk()
root.title("Plot Figures")
root.geometry("400x300")  # Set the size of the window

# Create a menu
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create a "File" menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add a "Plot Figures" option to the "File" menu
file_menu.add_command(label="Plot Figures", command=select_data_file)

# Add a separator in the "File" menu
file_menu.add_separator()

# Add an "Exit" option to the "File" menu
file_menu.add_command(label="Exit", command=exit_application)

# Start the Tkinter event loop
root.mainloop()

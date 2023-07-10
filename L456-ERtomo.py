import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.patches import Polygon
from matplotlib.widgets import PolygonSelector

data_file_path = ''  # Define data_file_path globally

def create_plots():
    global data_file_path

    if not data_file_path:
        messagebox.showinfo("Error", "No input file selected. Please open a data file first.")
        print("No input file selected. Please open a data file first.")
        return

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

    # Clear the existing table
    for item in tree_view.get_children():
        tree_view.delete(item)

    # Load data from the .dat file
    data = np.loadtxt(data_file_path)

    # Insert data into the table
    for row in data:
        tree_view.insert('', 'end', values=row)


def exit_application():
    plt.close('all')  # Close all matplotlib figures
    root.destroy()  # Destroy the Tkinter root window


# Create the main Tkinter window
root = tk.Tk()
root.title("Plot Figures")
root.geometry("400x300")  # Set the size of the window

# Create a Treeview widget to display the data table
tree_view = ttk.Treeview(root)
tree_view.pack(fill='both', expand=True)

# Add columns to the Treeview
tree_view["columns"] = ("Distance", "Depth", "Resistivity", "Conductivity")
tree_view.column("#0", width=0, stretch='no')
tree_view.column("Distance", width=70, anchor='center')
tree_view.column("Depth", width=70, anchor='center')
tree_view.column("Resistivity", width=100, anchor='center')
tree_view.column("Conductivity", width=100, anchor='center')

# Set column headings
tree_view.heading("#0", text="")
tree_view.heading("Distance", text="Distance (m)")
tree_view.heading("Depth", text="Depth (m)")
tree_view.heading("Resistivity", text="Resistivity")
tree_view.heading("Conductivity", text="Conductivity")

# Create a menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add an "Open Data File" option to the "File" menu
file_menu.add_command(label="Open Data File", command=select_data_file)

# Add a "Plot Figures" option to the "File" menu
file_menu.add_command(label="Plot Figures", command=create_plots)

# Add a separator in the "File" menu
file_menu.add_separator()

# Add an "Exit" option to the "File" menu
file_menu.add_command(label="Exit", command=exit_application)

# Start the Tkinter event loop
root.mainloop()

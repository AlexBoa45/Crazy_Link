import logging
import sys
import time
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from tkinter import Label

from turtledemo.penrose import start

import numpy as np
from shapely.geometry import Polygon
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.collections import LineCollection

import configparser

# This function its main purpose is to change the color of the button when the cursor is over it
def on_enter(event, color):
            # Change background color when the cursor enters the button
            event.widget.config(bg=color)

# This function its main purpose is to change the color of the button when the  cursor leaves it
def on_leave(event, color):
            # Reset background color when the cursor leaves the button
            event.widget.config(bg=color)

# Main object to develop the complex geocage
class custom_circuit:
    # Init part, defines the main parameters and the basic layout
    def __init__(self, root, dron=None):
        new_window_custom = tk.Toplevel(root)  # We create a new window over the main root
        new_window_custom.title("Complex Geocage")  # We put the title
        new_window_custom.geometry("1000x600+300+200") # Geometry and position over the screen
        new_window_custom.configure(bg="light gray")  # Color of the background
        new_window_custom.focus_force()
        new_window_custom.grab_set()
        new_window_custom.resizable(False, False)

        # Have in root the main dron class created before
        self.dron = dron
        # List to store points drawn by the user
        self.x_coor = []
        self.y_coor = []

        # Define the main cage and the excluison
        self.geocage = None
        self.exclusion =[]

        # Create a left frame for widgets inside the new window
        left_frame = tk.Frame(new_window_custom, bg="lightblue", width=300, height=400)
        left_frame.pack(side="left", fill="both", expand=True)

        # Create a right frame for the canvas inside the new window
        right_frame = tk.Frame(new_window_custom, bg="white", width=700, height=400)
        right_frame.pack(side="right", fill="both", expand=True)

        label = tk.Label(left_frame, text="Configurador Custom",
                         font=("Helvetica", 15, 'bold underline'), bg='light blue')
        label.place(relx=0.5, rely=0.05, anchor="center")

        self.combo = ttk.Combobox(left_frame, values=["Geocage", "Exclusion"],
                                  font=("Segoe UI", 14), width=23,
                                  height=5, state="readonly", justify="center")
        self.combo.set("Geocage")
        self.combo.place(relx=0.5, rely=0.12, anchor="center")


        label = tk.Label(left_frame, text="Tamaño del recinto:",
                         font=("Helvetica", 15, 'bold underline'), bg='light blue')
        label.place(relx=0.5, rely=0.2, anchor="center")

        label = tk.Label(left_frame, text="Anchura (x-axis) [m]:",
                         font=("Helvetica", 13, 'bold '), bg='light blue')
        label.place(relx=0.5, rely=0.25, anchor="center")

        label = tk.Label(left_frame, text="(+)",
                         font=("Helvetica", 15), bg='light blue')
        label.place(relx=0.25, rely=0.3, anchor="center")

        self.custom_entry_x_pos = tk.Spinbox(left_frame, from_=0, to=10, increment=0.2,
                                             textvariable=tk.StringVar(value='2'), font=("Helvetica", 14), width=10,
                                             justify="center", state="readonly")
        self.custom_entry_x_pos.place(relx=0.6, rely=0.3, anchor="center")

        label = tk.Label(left_frame, text="(-)",
                         font=("Helvetica", 15), bg='light blue')
        label.place(relx=0.25, rely=0.35, anchor="center")

        self.custom_entry_x_ne = tk.Spinbox(left_frame, from_=-10, to=0, increment=0.2,
                                            textvariable=tk.StringVar(value='-2'), font=("Helvetica", 14), width=10,
                                            justify="center", state="readonly")
        self.custom_entry_x_ne.place(relx=0.6, rely=0.35, anchor="center")


        label = tk.Label(left_frame, text="Profundidad (y-axis) [m]:",
                         font=("Helvetica", 13, 'bold '), bg='light blue')
        label.place(relx=0.5, rely=0.4, anchor="center")

        label = tk.Label(left_frame, text="(+)",
                         font=("Helvetica", 15), bg='light blue')
        label.place(relx=0.25, rely=0.45, anchor="center")

        self.custom_entry_y_pos = tk.Spinbox(left_frame, from_=0, to=10, increment=0.2,
                                             textvariable=tk.StringVar(value='2'), font=("Helvetica", 14), width=10,
                                             justify="center", state="readonly")
        self.custom_entry_y_pos.place(relx=0.6, rely=0.45, anchor="center")

        label = tk.Label(left_frame, text="(-)",
                         font=("Helvetica", 15), bg='light blue')
        label.place(relx=0.25, rely=0.5, anchor="center")

        self.custom_entry_y_ne = tk.Spinbox(left_frame, from_=-10, to=0, increment=0.2,
                                            textvariable=tk.StringVar(value='-2'), font=("Helvetica", 14), width=10,
                                            justify="center", state="readonly")
        self.custom_entry_y_ne.place(relx=0.6, rely=0.5, anchor="center")


        button_plot = tk.Button(left_frame, text="Actualitzar las dimensiones", font=("Helvetica", 14),
                                relief='groove', bg='light green', width=23, cursor='hand2',
                                command=lambda: self.InteractivePlot())
        button_plot.place(relx=0.5, rely=0.6, anchor="center")
        button_plot.bind("<Enter>", lambda event: on_enter(event, 'lime green'))
        button_plot.bind("<Leave>", lambda event: on_leave(event, 'light green'))

        button_delete = tk.Button(left_frame, text="Eliminar último paso", font=("Helvetica", 14),
                                       relief='groove', bg='brown2', width=23, cursor='hand2',command=lambda: self.delete_last_point())
        button_delete.place(relx=0.5, rely=0.7, anchor="center")
        button_delete.bind("<Enter>", lambda event: on_enter(event, 'brown3'))
        button_delete.bind("<Leave>", lambda event: on_leave(event, 'brown2'))

        button_save_custom = tk.Button(left_frame, text="Guardar configuración", font=("Helvetica", 15, 'bold'),
                                       relief='groove', bg='gold', width=23, cursor='hand2',command=lambda: self.safe_config_custom())
        button_save_custom.place(relx=0.5, rely=0.82, anchor="center")
        button_save_custom.bind("<Enter>", lambda event: on_enter(event, 'goldenrod'))
        button_save_custom.bind("<Leave>", lambda event: on_leave(event, 'gold'))

        button_close_custom = tk.Button(left_frame, text="Guardar todo y cerrar", font=("Helvetica", 15, 'bold '),
                                       relief='groove', bg='gold', width=23, cursor='hand2',command=lambda: self.save_all_custom(new_window_custom))
        button_close_custom.place(relx=0.5, rely=0.92, anchor="center")
        button_close_custom.bind("<Enter>", lambda event: on_enter(event, 'goldenrod'))
        button_close_custom.bind("<Leave>", lambda event: on_leave(event, 'gold'))

        # Set up the matplotlib figure and axis
        self.fig, self.ax = plt.subplots()

        # Set up the canvas for embedding the figure into the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Bind mouse click event to the plot
        self.canvas.mpl_connect("button_press_event", self.on_click)

        self.update_plot()

# This function basically tries to save all the configuration and close this object/window to get back to the previous
    def save_all_custom(self, new_window_custom):
        try:
            if self.geocage is not None:

                self.dron.setComplexScenario(
                inside_polygon=self.geocage,
                exclusion=self.exclusion)

                new_window_custom.destroy()
            else:
                messagebox.showinfo("Advertencia", "No se ha definido ningún Geocage.")
        except Exception as e:
            messagebox.showerror("Error al guardar Geocage/Zona de exclusión", str(e))

# This function basically tries to save the coordinates into the selected geocage or exclusion list
    def safe_config_custom(self):
        try:
            if len(self.x_coor) > 2:
                coords = list(zip(self.x_coor, self.y_coor))

                if self.combo.get() == "Geocage":
                    self.geocage = coords  # lista de coordenadas
                    messagebox.showinfo("Geocage Creado", "La zona Geocage ha sido creada correctamente.")
                else:
                    self.exclusion.append(coords)
                    messagebox.showinfo("Zona de exclusión creada", "Se añadió una nueva zona de exclusión.")
        except Exception as e:
            messagebox.showerror("Error al crear Geocage/Zona de exclusión", str(e))

# This function tries to update the dimensions of the plot
    def InteractivePlot(self):
        # Display the plot
        self.update_plot()

# This function plot the cage/exclusion everytime it is clicked
    def on_click(self, event):
        # Get the mouse click position on the plot
        if event.xdata is not None and event.ydata is not None:
            # Add the clicked point to the points list
            round_x_coor = round(event.xdata, 1)
            round_y_coor = round(event.ydata, 1)

            # Just to make a geometrical figure
            if len(self.x_coor) > 2 :
                if self.x_coor[-1] ==  self.x_coor[0] and self.y_coor[-1] == self.y_coor[0]:
                    self.x_coor.pop()
                    self.y_coor.pop()

            # Check if the decimal part is an odd number and adjust for x
            decimal_str_x = str(round_x_coor).split('.')[-1]
            if decimal_str_x and int(decimal_str_x[-1]) % 2 != 0:
                # If it's odd, add 0.1 to make it even
                round_x_coor += 0.1

            # Check if the decimal part is an odd number and adjust for y
            decimal_str_y = str(round_y_coor).split('.')[-1]
            if decimal_str_y and int(decimal_str_y[-1]) % 2 != 0:
                # If it's odd, add 0.1 to make it even
                round_y_coor += 0.1

            # Check if the point (round_x_coor, round_y_coor) already exists in the list of points
            if (round_x_coor, round_y_coor) in zip(self.x_coor, self.y_coor):
                pass
            else:
                # Append the new point
                self.x_coor.append(round_x_coor)
                self.y_coor.append(round_y_coor)

            self.x_coor=[round(num, 1) for num in self.x_coor]
            self.y_coor=[round(num, 1) for num in self.y_coor]

            # Just to make a geometrical figure
            if len(self.x_coor) > 2:
                self.x_coor.append(self.x_coor[0])
                self.y_coor.append(self.y_coor[0])

            # Update the plot with the new point
            self.update_plot()

# Simple, it is what it is
    def delete_last_point(self):

        if len(self.x_coor)>0:
            self.x_coor.pop()
            self.y_coor.pop()

        self.update_plot()

# This function shows the main panel, with everything
    def update_plot(self):
        # Clear the previous plot
        self.ax.clear()

        # Set axis limits
        self.ax.set_xlim(float(self.custom_entry_x_ne.get()) - 0.6, float(self.custom_entry_x_pos.get()) + 0.6)
        self.ax.set_ylim(float(self.custom_entry_y_ne.get()) - 0.6, float(self.custom_entry_y_pos.get()) + 0.6)

        # Set ticks at every 0.2 meters
        self.ax.set_xticks([round(i, 2) for i in np.arange(float(self.custom_entry_x_ne.get()) - 0.6,
                                                           float(self.custom_entry_x_pos.get()) + 0.6, 0.2)])
        self.ax.set_yticks([round(i, 2) for i in np.arange(float(self.custom_entry_y_ne.get()) - 0.6,
                                                           float(self.custom_entry_y_pos.get()) + 0.6, 0.2)])
        # Mark start
        self.ax.scatter(0, 0, color="green", s=100, label="Start", edgecolors="black", zorder=3)

        # Add annotations
        self.ax.annotate("Inicio", (0, 0), textcoords="offset points", xytext=(-20, -10),
                         ha="center", fontsize=10, color="green")

        # Adjust tick label size
        self.ax.tick_params(axis='x', labelrotation=-60)  # Rotate x-axis label
        self.ax.tick_params(axis='both', labelsize=7)

        # Draw grid
        self.ax.grid(True, linestyle="--", linewidth=0.5)

        self.ax.set_title('Dibuja el poligono')
        # Add axis labels
        self.ax.set_xlabel("Izquierda/Derecha [m]")
        self.ax.set_ylabel("Atrás/Delante [m]")

        # Plot the points as a line
        self.ax.plot(self.x_coor, self.y_coor, marker='o', color='b', linestyle='-', markersize=5)

        # Redraw the canvas
        self.canvas.draw()

# This is just to make tests
if __name__ == "__main__":
    root=tk.Tk()
    app = custom_circuit(root)
    root.mainloop()
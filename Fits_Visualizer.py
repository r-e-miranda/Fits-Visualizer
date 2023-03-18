# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
from tkinter import filedialog
from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def load_fits_data():
    file_path = filedialog.askopenfilename(filetypes=[("FITS files", "*.fits")])
    hdulist = fits.open(file_path)
    data = Table(hdulist[1].data)
    hdulist.close()
    global fits_data
    fits_data = data
    # clear existing items from column_listbox
    column_listbox.delete(0, tk.END)
    # add new column names to column_listbox
    for col in data.colnames:
        column_listbox.insert(tk.END, col)


def plot_columns():
    selected_columns = column_listbox.curselection()
    if not selected_columns:
        error_label.config(text="Please select one or more columns")
        return
    selected_columns = [column_listbox.get(i) for i in selected_columns]
    data = fits_data[selected_columns]
    # create a new figure for the plot
    fig = plt.figure()
    if plot_type.get() == "line":
        plt.plot(data[selected_columns[0]], data[selected_columns[1]])
    else:
        plt.scatter(data[selected_columns[0]], data[selected_columns[1]])
    plt.xlabel(selected_columns[0])
    plt.ylabel(selected_columns[1])
    # create a new window for the plot
    plot_window = tk.Toplevel(root)
    plot_window.title("Plot")
    # embed the plot in a canvas in the new window
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    # add a save button to the plot window
    save_button = tk.Button(plot_window, text="Save Plot", command=lambda: save_plot(fig))
    save_button.pack()
    # show the new window with the plot
    plot_window.mainloop()

def save_plot(fig):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("EPS files", "*.eps"), ("SVG files", "*.svg")])
    if file_path:
        fig.savefig(file_path)



root = tk.Tk()
root.title("FITS Data Plotter")

load_button = tk.Button(root, text="Load FITS Data", command=load_fits_data)
load_button.pack(pady=10)

column_label = tk.Label(root, text="Select columns to plot:")
column_label.pack()

column_listbox = tk.Listbox(root, selectmode="multiple")
column_listbox.pack()

column_scrollbar = tk.Scrollbar(root, orient="vertical")
column_scrollbar.pack(side="right", fill="y")
column_listbox.config(yscrollcommand=column_scrollbar.set)
column_scrollbar.config(command=column_listbox.yview)

plot_type_label = tk.Label(root, text="Select plot type:")
plot_type_label.pack(pady=10)

plot_type = tk.StringVar(value="line")

line_button = tk.Radiobutton(root, text="Line Plot", variable=plot_type, value="line")
line_button.pack(anchor="w")
scatter_button = tk.Radiobutton(root, text="Scatter Plot", variable=plot_type, value="scatter")
scatter_button.pack(anchor="w")

plot_button = tk.Button(root, text="Plot Columns", command=plot_columns)
plot_button.pack(pady=10)

error_label = tk.Label(root, fg="red")
error_label.pack(pady=5)

# Start the GUI event loop
root.mainloop()
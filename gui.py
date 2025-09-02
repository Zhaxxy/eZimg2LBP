"""
this file entirely made by ChatGPT, none for main.py though
"""
FILE_DEMILTER = ';'

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import traceback

from main import images_to_lbp_mods

def run_conversion():
    try:
        output_path = Path(output_var.get())
        img_paths = [Path(p) for p in images_var.get().split(FILE_DEMILTER) if p.strip()]
        desc = description_var.get().strip() or None
        user = username_var.get().strip() or None
        show_ext = show_ext_var.get()

        images_to_lbp_mods(output_path, img_paths, desc, user, show_ext)
        messagebox.showinfo("Success", "Mod file created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n\n{traceback.format_exc()}")

def browse_output():
    file_path = filedialog.asksaveasfilename(defaultextension=".mod", filetypes=[("Mod files", "*.mod")])
    if file_path:
        output_var.set(file_path)

def browse_images():
    files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tex")])
    if files:
        images_var.set(FILE_DEMILTER.join(files))

# Main window
root = tk.Tk()
root.title("eZimg2LBP")
root.iconbitmap("eZimg2LBP.ico")

# Variables
output_var = tk.StringVar()
images_var = tk.StringVar()
description_var = tk.StringVar()
username_var = tk.StringVar()
show_ext_var = tk.BooleanVar()

# Output mod
tk.Label(root, text="Output Mod File:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=output_var, width=40).grid(row=0, column=1)
tk.Button(root, text="Browse...", command=browse_output).grid(row=0, column=2)

# Images
tk.Label(root, text="Images:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=images_var, width=40).grid(row=1, column=1)
tk.Button(root, text="Browse...", command=browse_images).grid(row=1, column=2)

# Description
tk.Label(root, text="Description:").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=description_var, width=40).grid(row=2, column=1, columnspan=2)

# Username
tk.Label(root, text="Username:").grid(row=3, column=0, sticky="e")
tk.Entry(root, textvariable=username_var, width=40).grid(row=3, column=1, columnspan=2)

# Show extensions
tk.Checkbutton(root, text="Include file extensions in sticker names", variable=show_ext_var).grid(row=4, column=1, sticky="w")

# Run button
tk.Button(root, text="Create Mod File", command=run_conversion, bg="#4CAF50", fg="white").grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()

"""
Wine Correlation Tool
A Tkinter-based GUI application that computes and visualizes correlations
between numeric columns in a MySQL wine dataset.
Author: Sravani Peddi
Date: March 2025
"""

import mysql.connector  # type: ignore
import pandas as pd  # type: ignore
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import os

def connect_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Sravanipeddi',
            database='python_wine'
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None

def get_columns():
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM wine_data")
        columns = [col[0] for col in cursor.fetchall()]
        conn.close()
        return columns
    return []

def compute_correlation():
    for widget in result_frame.winfo_children():
        widget.destroy()
        
    col1 = col1_var.get()
    col2 = col2_var.get()
    
    if not col1 or not col2:
        messagebox.showwarning("Selection Error", "Please select both columns.")
        return
    if col1 == col2:
        messagebox.showwarning("Input Error", "Same column names given.")
        return
    
    conn = connect_database()
    if conn:
        try:
            cursor = conn.cursor()
            query = f"SELECT `{col1}`, `{col2}` FROM wine_data"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            
            df = pd.DataFrame(data, columns=[col1, col2])
            
            for col in [col1, col2]:
                if df[col].dtype == 'object':
                    raise ValueError(f"Column '{col}' contains string values. Please select numeric columns only.")
            
            df[col1] = pd.to_numeric(df[col1], errors='coerce')
            df[col2] = pd.to_numeric(df[col2], errors='coerce')
            
            df = df.dropna()
            
            if len(df) < 2:
                messagebox.showerror("Data Error", "Insufficient numeric data points for correlation.")
                return
                
            correlation = df[col1].corr(df[col2])
            
            corr_label = ttk.Label(result_frame, 
                                 text=f"The correlation between {col1} and {col2} is {correlation:.4f}",
                                 font=('Arial', 12), background='white')
            corr_label.pack(pady=5)
            
            fig = plt.Figure(figsize=(4, 3), dpi=100)
            ax = fig.add_subplot(111)
            ax.scatter(df[col1], df[col2], color="blue", alpha=0.5)
            ax.set_xlabel(col1)
            ax.set_ylabel(col2)
            ax.set_title(f"Scatter Plot: {col1} vs {col2}")
            ax.grid(True)
            
            canvas = FigureCanvasTkAgg(fig, master=result_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()
            
        except ValueError as ve:
            messagebox.showerror("Data Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Tkinter GUI
root = tk.Tk()
root.title("Column Correlation Tool")
root.geometry("700x600")

# Background image setup
image_path = "background.jpg"
print(f"Current working directory: {os.path.abspath('.')}")
print(f"Looking for image at: {os.path.abspath(image_path)}")

if os.path.exists(image_path):
    try:
        bg_image = Image.open(image_path)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo  # Keep reference to avoid garbage collection
        bg_label.lower()  # Ensure it stays behind other widgets
        print("Background image loaded successfully")
    except Exception as e:
        print(f"Error loading background image: {e}")
        bg_label = tk.Label(root, bg="lightgray")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()
else:
    print(f"File 'background.jpg' not found at {os.path.abspath(image_path)}")
    bg_label = tk.Label(root, bg="lightgray")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()

# Input frame (kept compact at the top)
input_frame = ttk.Frame(root)
input_frame.place(x=20, y=20)  # Positioned at top-left with some padding

# Result frame (separate, positioned below input frame)
result_frame = ttk.Frame(root)
result_frame.place(x=20, y=150)  # Positioned below input frame

# Widgets for input frame
columns = get_columns()
col1_var = tk.StringVar()
col2_var = tk.StringVar()

ttk.Label(input_frame, text="Select Column 1:").grid(row=0, column=0, pady=5, padx=5)
col1_dropdown = ttk.Combobox(input_frame, textvariable=col1_var, values=columns, state="readonly")
col1_dropdown.grid(row=0, column=1, pady=5, padx=5)

ttk.Label(input_frame, text="Select Column 2:").grid(row=1, column=0, pady=5, padx=5)
col2_dropdown = ttk.Combobox(input_frame, textvariable=col2_var, values=columns, state="readonly")
col2_dropdown.grid(row=1, column=1, pady=5, padx=5)

submit_btn = ttk.Button(input_frame, text="Compute Correlation", command=compute_correlation)
submit_btn.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
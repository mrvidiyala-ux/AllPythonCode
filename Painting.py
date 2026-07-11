import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw
import io

def paint(event):
    if tool == "brush":
        canvas.create_oval(event.x - brush_size//2, event.y - brush_size//2, 
                          event.x + brush_size//2, event.y + brush_size//2, 
                          fill=color, outline=color)
    elif tool == "eraser":
        canvas.create_oval(event.x - brush_size//2, event.y - brush_size//2, 
                          event.x + brush_size//2, event.y + brush_size//2, 
                          fill="white", outline="white")

def start_shape(event):
    global shape_start
    shape_start = (event.x, event.y)

def draw_shape(event):
    if tool in ["rectangle", "circle"] and shape_start:
        canvas.delete("temp_shape")
        if tool == "rectangle":
            canvas.create_rectangle(shape_start[0], shape_start[1], event.x, event.y, 
                                   outline=color, width=brush_size, tag="temp_shape")
        elif tool == "circle":
            canvas.create_oval(shape_start[0], shape_start[1], event.x, event.y, 
                              outline=color, width=brush_size, tag="temp_shape")
    elif tool == "line" and shape_start:
        canvas.delete("temp_line")
        canvas.create_line(shape_start[0], shape_start[1], event.x, event.y, 
                          fill=color, width=brush_size, tag="temp_line")

def end_shape(event):
    global shape_start
    if shape_start:
        canvas.delete("temp_shape")
        canvas.delete("temp_line")
        if tool == "rectangle":
            canvas.create_rectangle(shape_start[0], shape_start[1], event.x, event.y, 
                                   outline=color, width=brush_size)
        elif tool == "circle":
            canvas.create_oval(shape_start[0], shape_start[1], event.x, event.y, 
                              outline=color, width=brush_size)
        elif tool == "line":
            canvas.create_line(shape_start[0], shape_start[1], event.x, event.y, 
                              fill=color, width=brush_size)
        shape_start = None

def choose_color():
    global color
    result = colorchooser.askcolor(title="Choose a color")
    if result[1]:
        color = result[1]
        color_btn.config(bg=color)

def set_tool(selected_tool):
    global tool
    tool = selected_tool
    brush_btn.config(relief="sunken" if tool == "brush" else "raised")
    eraser_btn.config(relief="sunken" if tool == "eraser" else "raised")
    line_btn.config(relief="sunken" if tool == "line" else "raised")
    rect_btn.config(relief="sunken" if tool == "rectangle" else "raised")
    circle_btn.config(relief="sunken" if tool == "circle" else "raised")

def set_brush_size(value):
    global brush_size
    brush_size = int(value)
    size_label.config(text=f"Size: {brush_size}")

def clear_canvas():
    if messagebox.askyesno("Clear", "Are you sure you want to clear the canvas?"):
        canvas.delete("all")

def save_canvas():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
    if file_path:
        messagebox.showinfo("Save", "Feature requires PIL library installation")

def undo_drawing():
    messagebox.showinfo("Undo", "Undo feature coming soon")

root = tk.Tk()
root.title("Paint - Drawing App")
root.geometry("900x650")

color = "black"
brush_size = 5
tool = "brush"
shape_start = None

# Main toolbar
toolbar = tk.Frame(root, bg="lightgray", height=80)
toolbar.pack(side="top", fill="x", padx=5, pady=5)

# Row 1: Tools
tools_frame = tk.Frame(toolbar, bg="lightgray")
tools_frame.pack(side="top", fill="x", padx=5, pady=5)

tk.Label(tools_frame, text="Tools:", bg="lightgray", font=("Arial", 10, "bold")).pack(side="left", padx=5)

brush_btn = tk.Button(tools_frame, text="✏ Brush", command=lambda: set_tool("brush"), relief="sunken", width=10)
brush_btn.pack(side="left", padx=2)

eraser_btn = tk.Button(tools_frame, text="🗑 Eraser", command=lambda: set_tool("eraser"), width=10)
eraser_btn.pack(side="left", padx=2)

line_btn = tk.Button(tools_frame, text="/ Line", command=lambda: set_tool("line"), width=10)
line_btn.pack(side="left", padx=2)

rect_btn = tk.Button(tools_frame, text="▭ Rectangle", command=lambda: set_tool("rectangle"), width=10)
rect_btn.pack(side="left", padx=2)

circle_btn = tk.Button(tools_frame, text="○ Circle", command=lambda: set_tool("circle"), width=10)
circle_btn.pack(side="left", padx=2)

# Row 2: Color & Size
options_frame = tk.Frame(toolbar, bg="lightgray")
options_frame.pack(side="top", fill="x", padx=5, pady=5)

color_btn = tk.Button(options_frame, text="  ", command=choose_color, bg=color, width=4, height=1)
color_btn.pack(side="left", padx=5)

tk.Label(options_frame, text="Color", bg="lightgray").pack(side="left")

tk.Label(options_frame, text="  ", bg="lightgray").pack(side="left", padx=10)

size_label = tk.Label(options_frame, text=f"Size: {brush_size}", bg="lightgray", width=10)
size_label.pack(side="left", padx=5)

size_slider = tk.Scale(options_frame, from_=1, to=50, orient="horizontal", command=set_brush_size, length=120)
size_slider.set(5)
size_slider.pack(side="left", padx=5)

# Action buttons
tk.Button(options_frame, text="↶ Undo", command=undo_drawing, width=8).pack(side="left", padx=2)
tk.Button(options_frame, text="💾 Save", command=save_canvas, width=8).pack(side="left", padx=2)
tk.Button(options_frame, text="🗑 Clear", command=clear_canvas, width=8).pack(side="left", padx=2)

# Canvas
canvas = tk.Canvas(root, bg="white", width=900, height=500, cursor="cross")
canvas.pack(pady=10, fill="both", expand=True)
canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-1>", start_shape)
canvas.bind("<B1-Motion>", draw_shape)
canvas.bind("<ButtonRelease-1>", end_shape)

# Status bar
status_bar = tk.Frame(root, bg="lightgray", height=30)
status_bar.pack(side="bottom", fill="x")
status_label = tk.Label(status_bar, text="Ready", bg="lightgray", anchor="w")
status_label.pack(side="left", padx=5)

root.mainloop()
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw
import os

class TuxPaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tux Paint - Drawing App")
        self.root.geometry("1000x700")
        
        # Drawing state
        self.drawing = False
        self.brush_color = "black"
        self.brush_size = 5
        self.tool = "brush"
        self.last_x = 0
        self.last_y = 0
        
        # Create PIL image for saving
        self.image = Image.new("RGB", (900, 600), "white")
        self.draw = ImageDraw.Draw(self.image)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Toolbar frame
        toolbar = tk.Frame(self.root, bg="lightgray", height=60)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Color button
        tk.Button(toolbar, text="Color", command=self.choose_color, 
                  bg=self.brush_color, width=10).pack(side=tk.LEFT, padx=5)
        
        # Tool buttons
        tk.Button(toolbar, text="Brush", command=lambda: self.set_tool("brush")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Eraser", command=lambda: self.set_tool("eraser")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Line", command=lambda: self.set_tool("line")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Rectangle", command=lambda: self.set_tool("rect")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Circle", command=lambda: self.set_tool("circle")).pack(side=tk.LEFT, padx=2)
        
        # Size slider
        tk.Label(toolbar, text="Size:", bg="lightgray").pack(side=tk.LEFT, padx=5)
        self.size_slider = tk.Scale(toolbar, from_=1, to=50, orient=tk.HORIZONTAL, 
                                     command=self.set_brush_size, length=100)
        self.size_slider.set(5)
        self.size_slider.pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        tk.Button(toolbar, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Save", command=self.save_image).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Open", command=self.open_image).pack(side=tk.LEFT, padx=2)
        
        # Canvas
        self.canvas = tk.Canvas(self.root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
    
    def set_tool(self, tool):
        self.tool = tool
    
    def set_brush_size(self, value):
        self.brush_size = int(value)
    
    def choose_color(self):
        color = colorchooser.askcolor(self.brush_color)
        if color[1]:
            self.brush_color = color[1]
    
    def on_mouse_down(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
    
    def on_mouse_drag(self, event):
        if not self.drawing:
            return
        
        if self.tool == "brush":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                   fill=self.brush_color, width=self.brush_size, capstyle=tk.ROUND, smooth=True)
            self.draw.line([self.last_x, self.last_y, event.x, event.y],
                          fill=self.brush_color, width=self.brush_size)
        
        elif self.tool == "eraser":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                   fill="white", width=self.brush_size, capstyle=tk.ROUND)
            self.draw.line([self.last_x, self.last_y, event.x, event.y],
                          fill="white", width=self.brush_size)
        
        self.last_x = event.x
        self.last_y = event.y
    
    def on_mouse_up(self, event):
        self.drawing = False
        
        if self.tool == "line":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                   fill=self.brush_color, width=self.brush_size)
            self.draw.line([self.last_x, self.last_y, event.x, event.y],
                          fill=self.brush_color, width=self.brush_size)
        
        elif self.tool == "rect":
            self.canvas.create_rectangle(self.last_x, self.last_y, event.x, event.y,
                                        outline=self.brush_color, width=self.brush_size)
            self.draw.rectangle([self.last_x, self.last_y, event.x, event.y],
                               outline=self.brush_color, width=self.brush_size)
        
        elif self.tool == "circle":
            r = ((event.x - self.last_x)**2 + (event.y - self.last_y)**2)**0.5
            self.canvas.create_oval(self.last_x - r, self.last_y - r, 
                                   self.last_x + r, self.last_y + r,
                                   outline=self.brush_color, width=self.brush_size)
            self.draw.ellipse([self.last_x - r, self.last_y - r, 
                              self.last_x + r, self.last_y + r],
                             outline=self.brush_color, width=self.brush_size)
    
    def clear_canvas(self):
        if messagebox.askyesno("Clear", "Clear the entire canvas?"):
            self.canvas.delete("all")
            self.image = Image.new("RGB", (900, 600), "white")
            self.draw = ImageDraw.Draw(self.image)
    
    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Success", f"Image saved as {os.path.basename(file_path)}")
    
    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        if file_path:
            self.image = Image.open(file_path)
            self.draw = ImageDraw.Draw(self.image)
            self.canvas.delete("all")
            # Display the image on canvas (simplified)
            messagebox.showinfo("Open", "Image loaded. Start drawing on top of it!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TuxPaintApp(root)
    root.mainloop()

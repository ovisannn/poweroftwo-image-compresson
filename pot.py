import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os

class ImageScalerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Scaler App")
        self.root.geometry("800x600")

        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.image_frame = ttk.Frame(self.root, width=600, height=400)
        self.image_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.status_var = tk.StringVar()
        self.status_var.set("Welcome! Load images to begin.")

        self.status_label = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_label.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.load_button = ttk.Button(self.control_frame, text="Load Images", command=self.load_images)
        self.load_button.grid(row=0, column=0, pady=5, sticky="ew")

        self.scale_up_button = ttk.Button(self.control_frame, text="Upscale (2x)", command=self.upscale_images, state="disabled")
        self.scale_up_button.grid(row=1, column=0, pady=5, sticky="ew")

        self.scale_down_button = ttk.Button(self.control_frame, text="Downscale (0.5x)", command=self.downscale_images, state="disabled")
        self.scale_down_button.grid(row=2, column=0, pady=5, sticky="ew")

        self.crop_button = ttk.Button(self.control_frame, text="Crop Images", command=self.enable_crop, state="disabled")
        self.crop_button.grid(row=3, column=0, pady=5, sticky="ew")

        self.save_button = ttk.Button(self.control_frame, text="Save Images", command=self.save_images, state="disabled")
        self.save_button.grid(row=4, column=0, pady=5, sticky="ew")

        self.image_label = ttk.Label(self.image_frame)
        self.image_label.grid(row=0, column=0, sticky="nsew")
        
        self.images = []  
        self.image_paths = []  
        self.tk_images = []
        self.crop_enabled = False
        self.crop_rectangle = None
        self.start_x = self.start_y = 0

        self.canvas = tk.Canvas(self.image_frame, width=600, height=400)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scrollbar = ttk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.v_scrollbar = ttk.Scrollbar(self.image_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.config(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
    def load_images(self):
        self.image_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.png;*.jpeg;*.bmp")])
        if self.image_paths:
            self.images = [Image.open(path) for path in self.image_paths]
            self.display_image(self.images[0])
            self.status_var.set(f"Loaded {len(self.images)} images")
            self.enable_controls(True)

    def display_image(self, image):
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def enable_controls(self, enable=True):
        state = "normal" if enable else "disabled"
        self.scale_up_button.config(state=state)
        self.scale_down_button.config(state=state)
        self.crop_button.config(state=state)
        self.save_button.config(state=state)

    def upscale_images(self):
        if self.images:
            for i, image in enumerate(self.images):
                width, height = image.size
                new_size = (width * 2, height * 2)
                self.images[i] = image.resize(new_size, Image.Resampling.LANCZOS)
            self.display_image(self.images[0])
            self.status_var.set("Upscaled all images 2x")

    def downscale_images(self):
        if self.images:
            for i, image in enumerate(self.images):
                width, height = image.size
                new_size = (width // 2, height // 2)
                self.images[i] = image.resize(new_size, Image.Resampling.LANCZOS)
            self.display_image(self.images[0])
            self.status_var.set("Downscaled all images 0.5x")

    def enable_crop(self):
        self.crop_enabled = True
        self.status_var.set("Select an area to crop")
        self.canvas.bind("<Button-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.finish_crop)

    def start_crop(self, event):
        if self.crop_enabled:
            self.start_x = self.canvas.canvasx(event.x)
            self.start_y = self.canvas.canvasy(event.y)

    def update_crop(self, event):
        if self.crop_enabled:
            if self.crop_rectangle:
                self.canvas.delete(self.crop_rectangle)
            self.crop_rectangle = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y),
                outline="red", width=2
            )

    def finish_crop(self, event):
        if self.crop_enabled:
            end_x = self.canvas.canvasx(event.x)
            end_y = self.canvas.canvasy(event.y)
            crop_box = (self.start_x, self.start_y, end_x, end_y)
            for i in range(len(self.images)):
                self.images[i] = self.images[i].crop(crop_box)
            self.display_image(self.images[0])
            self.status_var.set("Cropped all images")
            self.crop_enabled = False

    def save_images(self):
        # Save all processed images
        if self.images:
            folder_path = filedialog.askdirectory()
            if folder_path:
                for i, image in enumerate(self.images):
                    file_name = os.path.basename(self.image_paths[i])
                    # save_path = os.path.join(folder_path, f"processed_{file_name}")
                    save_path = os.path.join(folder_path, f"{file_name}")
                    image.save(save_path)
                self.status_var.set(f"Saved {len(self.images)} images to {folder_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageScalerApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import math

def nearest_power_of_two(n):
    return 2 ** int(math.log2(n))

def resize_to_power_of_two(image):
    width, height = image.size
    new_width = nearest_power_of_two(width)
    new_height = nearest_power_of_two(height)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def auto_crop(image):
    gray_image = image.convert('L')
    bbox = gray_image.getbbox()
    if bbox:
        return image.crop(bbox)
    else:
        return image  

def process_image():
    global img_display
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
    if not file_path:
        return

    img = Image.open(file_path)

    resized_img = resize_to_power_of_two(img)

    cropped_img = auto_crop(resized_img)

    img_display = ImageTk.PhotoImage(cropped_img)

    canvas.create_image(10, 10, anchor=tk.NW, image=img_display)
    canvas.config(width=cropped_img.width, height=cropped_img.height)

    save_button.config(state=tk.NORMAL)

    global processed_image
    processed_image = cropped_img

def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg;*.jpeg"),
                                                        ("All files", "*.*")])
    if file_path:
        processed_image.save(file_path)
        messagebox.showinfo("Image Saved", f"Image saved as {file_path}")

root = tk.Tk()
root.title("Power of Two Image Compressor")

canvas = tk.Canvas(root, width=300, height=300, bg="gray")
canvas.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

open_button = tk.Button(root, text="Open Image", command=process_image)
open_button.grid(row=1, column=0, padx=10, pady=10)

save_button = tk.Button(root, text="Save Image", command=save_image, state=tk.DISABLED)
save_button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()

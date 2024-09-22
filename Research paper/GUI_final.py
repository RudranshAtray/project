import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random

# Function to encrypt a single RGB pixel
def caesar_encrypt_pixel(pixel, shift):
    r, g, b = pixel
    encrypted_r = (r + shift) % 256
    encrypted_g = (g + shift) % 256
    encrypted_b = (b + shift) % 256
    return (encrypted_r, encrypted_g, encrypted_b)

# Function to decrypt an encrypted RGB pixel
def caesar_decrypt_pixel(encrypted_pixel, shift):
    r, g, b = encrypted_pixel
    decrypted_r = (r - shift) % 256
    decrypted_g = (g - shift) % 256
    decrypted_b = (b - shift) % 256
    return (decrypted_r, decrypted_g, decrypted_b)

# Function to encrypt an image
def encrypt_image(image_path, shift):
    original_image = Image.open(image_path)
    encrypted_image = Image.new("RGB", original_image.size)

    for x in range(original_image.width):
        for y in range(original_image.height):
            pixel_value = original_image.getpixel((x, y))
            encrypted_pixel = caesar_encrypt_pixel(pixel_value, shift)
            encrypted_image.putpixel((x, y), encrypted_pixel)

    encrypted_image_path = f"encrypt_{image_path.split('/')[-1]}"
    encrypted_image.save(encrypted_image_path)
    return encrypted_image_path

# Function to decrypt an image
def decrypt_image(encrypted_image_path, shift):
    encrypted_image = Image.open(encrypted_image_path)
    decrypted_image = Image.new("RGB", encrypted_image.size)

    for x in range(encrypted_image.width):
        for y in range(encrypted_image.height):
            encrypted_pixel_value = encrypted_image.getpixel((x, y))
            decrypted_pixel = caesar_decrypt_pixel(encrypted_pixel_value, shift)
            decrypted_image.putpixel((x, y), decrypted_pixel)

    decrypted_image_path = f"decrypt_{encrypted_image_path.split('/')[-1]}"
    decrypted_image.save(decrypted_image_path)
    return decrypted_image_path

# Function to generate random mask
def generate_random_mask(image_path):
    input_image = Image.open(image_path)
    mask = Image.new("RGB", input_image.size)
    mask_pixels = mask.load()

    for x in range(mask.width):
        for y in range(mask.height):
            r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            mask_pixels[x, y] = (r, g, b)

    mask_path = f"masks/mask_{image_path.split('/')[-1]}"
    mask.save(mask_path)
    return mask_path

# Function to subtract mask from image
def subtract_images(image_path1, image_path2, output_path):
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    if image1.size != image2.size:
        raise ValueError("Images must have the same dimensions")

    subtracted_image = Image.new("RGB", image1.size)
    subtracted_pixels = []

    for x in range(image1.width):
        for y in range(image1.height):
            pixel1 = image1.getpixel((x, y))
            pixel2 = image2.getpixel((x, y))
            subtracted_pixel = tuple(max(0, p1 - p2) for p1, p2 in zip(pixel1, pixel2))
            subtracted_pixels.append(subtracted_pixel)

    subtracted_image.putdata(subtracted_pixels)
    subtracted_image.save(output_path)

# GUI functions
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        entry_image_path.delete(0, tk.END)
        entry_image_path.insert(0, file_path)

def process_images():
    image_path = entry_image_path.get()
    if not image_path:
        messagebox.showerror("Error", "Please select an image file.")
        return

    shift_value = 55  # Fixed shift value for encryption/decryption

    try:
        # Generate random mask
        mask_path = generate_random_mask(image_path)
        messagebox.showinfo("Info", f"Random mask saved as {mask_path}")

        # Encrypt the image
        encrypted_image_path = encrypt_image(image_path, shift_value)
        messagebox.showinfo("Info", f"Image encrypted and saved as {encrypted_image_path}")

        # Decrypt the image
        decrypted_image_path = decrypt_image(encrypted_image_path, shift_value)
        messagebox.showinfo("Info", f"Image decrypted and saved as {decrypted_image_path}")

        # Subtract the mask from the decrypted image
        subtracted_image_path = f"encrypted_images/subtracted_{image_path.split('/')[-1]}"
        subtract_images(decrypted_image_path, mask_path, subtracted_image_path)
        messagebox.showinfo("Info", f"Subtracted image saved as {subtracted_image_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the GUI
root = tk.Tk()
root.title("Image Processing")

# Create and place widgets
label_image_path = tk.Label(root, text="Image Path:")
label_image_path.grid(row=0, column=0, padx=5, pady=5)

entry_image_path = tk.Entry(root, width=50)
entry_image_path.grid(row=0, column=1, padx=5, pady=5)

button_browse = tk.Button(root, text="Browse", command=open_file)
button_browse.grid(row=0, column=2, padx=5, pady=5)

button_process = tk.Button(root, text="Process", command=process_images)
button_process.grid(row=1, column=1, padx=5, pady=5)

# Start the GUI event loop
root.mainloop()

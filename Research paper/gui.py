from PIL import Image
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
    encrypted_image = Image.new("RGB", original_image.size)  # Create a new RGB image

    for x in range(original_image.width):
        for y in range(original_image.height):
            pixel_value = original_image.getpixel((x, y))
            encrypted_pixel = caesar_encrypt_pixel(pixel_value, shift)
            encrypted_image.putpixel((x, y), encrypted_pixel)

    encrypted_image_path = f"encrypt_{image_path[8:]}"
    encrypted_image.save(encrypted_image_path)
    print(f"Color image encrypted and saved as {encrypted_image_path}.")
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

    decrypted_image_path = f"decrypt_{encrypted_image_path[8:]}"
    decrypted_image.save(decrypted_image_path)
    print(f"Color image decrypted and saved as {decrypted_image_path}.")
    return decrypted_image_path

# Load the input image
input_image_path = "samples/image1.jpg"
input_image = Image.open(input_image_path)

# Create a new image with the same size as the input image
mask = Image.new("RGB", input_image.size)

# Get the pixel data for the mask
mask_pixels = mask.load()

# Generate random black and white values for the mask
for x in range(mask.width):
    for y in range(mask.height):
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        mask_pixels[x, y] = (r, g, b)

# Save the black and white mask image
mask_path = f"masks/mask_{input_image_path[8:]}"
mask.save(mask_path)

print(f"Random image saved as {mask_path}")

# Encrypt the original image
shift_value = 55
encrypted_image_path = encrypt_image(input_image_path, shift_value)

# Decrypt the encrypted image
decrypted_image_path = decrypt_image(encrypted_image_path, shift_value)

# Load the two images for subtraction
image1 = Image.open(decrypted_image_path)
image2 = Image.open(mask_path)

# Ensure both images have the same dimensions
if image1.size != image2.size:
    raise ValueError("Images must have the same dimensions")

# Subtract the pixel values of image2 from image1
subtracted_image = Image.new("RGB", image1.size)
subtracted_pixels = []

for x in range(image1.width):
    for y in range(image1.height):
        pixel1 = image1.getpixel((x, y))
        pixel2 = image2.getpixel((x, y))
        subtracted_pixel = tuple(max(0, p1 - p2) for p1, p2 in zip(pixel1, pixel2))
        subtracted_pixels.append(subtracted_pixel)

subtracted_image.putdata(subtracted_pixels)

# Save the subtracted image
subtracted_image_path = f"encrypted_images/subtracted_{input_image_path[8:]}"
subtracted_image.save(subtracted_image_path)

print(f"Pixels subtracted and saved as {subtracted_image_path}")

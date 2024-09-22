from PIL import Image
import random

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
        r,g,b=random.randint(0,255), random.randint(0,255), random.randint(0,255)
        mask_pixels[x, y] = r,g,b

# Save the black and white mask image
mask_path = f"masks/mask_{input_image_path[8:]}"
mask.save(mask_path)

print(f"Random image saved as {mask_path}")

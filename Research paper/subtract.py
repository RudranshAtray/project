from PIL import Image

# Load the two images (replace with your image paths)
image1_path = "encrypt_image1.jpg"
image2_path = "masks/mask_image1.jpg"

image1 = Image.open(image1_path)
image2 = Image.open(image2_path)

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
subtracted_image_path = f"encypted/subtracted_{image1_path}"
subtracted_image.save(subtracted_image_path)

print(f"Pixels subtracted and saved as {subtracted_image_path}")

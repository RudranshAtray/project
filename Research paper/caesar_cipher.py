from PIL import Image

def caesar_encrypt_pixel(pixel, shift):
    # Encrypt a single RGB pixel
    r, g, b = pixel
    encrypted_r = (r + shift) % 256
    encrypted_g = (g + shift) % 256
    encrypted_b = (b + shift) % 256
    return (encrypted_r, encrypted_g, encrypted_b)

def caesar_decrypt_pixel(encrypted_pixel, shift):
    # Decrypt an encrypted RGB pixel
    r, g, b = encrypted_pixel
    decrypted_r = (r - shift) % 256
    decrypted_g = (g - shift) % 256
    decrypted_b = (b - shift) % 256
    return (decrypted_r, decrypted_g, decrypted_b)

def encrypt_image(image_path, shift):
    original_image = Image.open(image_path)
    encrypted_image = Image.new("RGB", original_image.size)  # Create a new RGB image

    for x in range(original_image.width):
        for y in range(original_image.height):
            pixel_value = original_image.getpixel((x, y))
            encrypted_pixel = caesar_encrypt_pixel(pixel_value, shift)
            encrypted_image.putpixel((x, y), encrypted_pixel)

    encrypted_image.save(f"encrypt_{image_path[8:]}")
    print(f"Color image encrypted and saved as 'encrypt_{image_path[8:]}'.")

def decrypt_image(encrypted_image_path, shift):
    encrypted_image = Image.open(encrypted_image_path)
    decrypted_image = Image.new("RGB", encrypted_image.size)

    for x in range(encrypted_image.width):
        for y in range(encrypted_image.height):
            encrypted_pixel_value = encrypted_image.getpixel((x, y))
            decrypted_pixel = caesar_decrypt_pixel(encrypted_pixel_value, shift)
            decrypted_image.putpixel((x, y), decrypted_pixel)

    decrypted_image.save(f"decrypt_{image_path[8:]}")
    print(f"Color image decrypted and saved as 'decrypt_{image_path[8:]}'.")

# Example usage
image_path = "samples/image1.jpg"
shift_value = 55
encrypt_image(image_path, shift_value)
decrypt_image(f"encrypt_{image_path[8:]}", shift_value)

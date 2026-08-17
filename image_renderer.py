from PIL import Image

# Aesthetic presets for ASCII rendering. Choose your preferred style below:
ASCII_PRESETS = {
    "blocks": "█▓▒░.",             # Dark-to-light block ramp for black terminals
    "clean": ".:-=+*#%@█",          # Classic text art with a stronger dark-to-light ramp
    "halftone": "·°*oO#@.",         # Retro dot-matrix print style, dark-to-light order
    "hacker": ".:-=+*#%@#",          # Slightly denser set for better mid-tone spread on black terminals
    "extended": ".'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" # Maximum detail, dark-to-light order
}

# Note: If you are using a light terminal theme, you can reverse the character set (e.g. ASCII_PRESETS["blocks"][::-1])
ASCII_CHARS = ASCII_PRESETS["hacker"]

def brightness_to_ascii(brightness):
    normalized = brightness / 255.0
    index = int((normalized ** 1.35) * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[min(index, len(ASCII_CHARS) - 1)]



def render_pillow_image(img, screen):
    # Convert to grayscale
    rgb = img.convert("RGB")
    gray=img.convert("L")
    img_width,img_height=gray.size

    scale = min(
        screen.width / img_width,
        (screen.height * 2) / img_height
    )

    new_width = int(img_width * scale)
    new_height = int(img_height * scale / 2)

    rgb = rgb.resize((new_width, new_height))

    x_offset = (screen.width - new_width) // 2
    y_offset = (screen.height - new_height) // 2

    screen.clear_buffer()

    for y in range(new_height):
        for x in range(new_width):
            r,g,b=rgb.getpixel((x,y))
            brightness = gray.getpixel((x, y))
            char = brightness_to_ascii(brightness)
            screen.set_pixel(x + x_offset, y + y_offset, char,(r,g,b))

    screen.render()
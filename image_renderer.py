from PIL import Image

# Aesthetic presets for ASCII rendering. Choose your preferred style below:
ASCII_PRESETS = {
    "blocks": " ░▒▓█",             # (Recommended) Modern grayscale shader look
    "clean": " .:-=+*#%@█",          # Classic text art with a solid block highlight
    "halftone": " .·°*oO#@",         # Retro dot-matrix print style
    "hacker": " .:-+*=%@#",          # Punctuation-only gradient (removes alphabet noise)
    "extended": " .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" # Maximum detail
}

# Note: If you are using a light terminal theme, you can reverse the character set (e.g. ASCII_PRESETS["blocks"][::-1])
ASCII_CHARS = ASCII_PRESETS["blocks"]

def brightness_to_ascii(brightness):
    index = brightness * (len(ASCII_CHARS) - 1) // 255
    return ASCII_CHARS[index]



def render_pillow_image(img, screen):
    # Convert to grayscale
    gray = img.convert("L")
    img_width,img_height=gray.size

    scale = min(
        screen.width / img_width,
        (screen.height * 2) / img_height
    )

    new_width = int(img_width * scale)
    new_height = int(img_height * scale / 2)

    gray = gray.resize((new_width, new_height))

    x_offset = (screen.width - new_width) // 2
    y_offset = (screen.height - new_height) // 2

    screen.clear_buffer()

    for y in range(new_height):
        for x in range(new_width):
            brightness = gray.getpixel((x, y))
            char = brightness_to_ascii(brightness)
            screen.set_pixel(x + x_offset, y + y_offset, char)

    screen.render()
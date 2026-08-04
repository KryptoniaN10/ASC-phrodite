from PIL import Image

ASCII_CHARS = " .:-=+*#%@"

def brightness_to_ascii(brightness):
    index = brightness * (len(ASCII_CHARS) - 1) // 255
    return ASCII_CHARS[index]


def render_image(filename, screen):
    img = Image.open(filename)

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

    screen.clear_buffer()

    for y in range(new_height):
        for x in range(new_width):
            brightness = gray.getpixel((x, y))
            char = brightness_to_ascii(brightness)
            screen.set_pixel(x, y, char)

    screen.render()
from PIL import Image

# Aesthetic presets for ASCII rendering. Choose your preferred style below:
ASCII_PRESETS = {
    "blocks": "░▒▓█",             # Dark-to-light block ramp for black terminals
    "clean": ".:-=+*#%@█",          # Classic text art with a stronger dark-to-light ramp
    "halftone": "·°*oO#@.",         # Retro dot-matrix print style, dark-to-light order
    "hacker": ".:-=+*#%@#",          # Slightly denser set for better mid-tone spread on black terminals
    "extended": ".'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" # Maximum detail, dark-to-light order
}

# Note: If you are using a light terminal theme, you can reverse the character set (e.g. ASCII_PRESETS["blocks"][::-1])
ASCII_CHARS = ASCII_PRESETS["blocks"]

def brightness_to_ascii(brightness):
    normalized = brightness / 255.0
    index = int((normalized ** 1.35) * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[min(index, len(ASCII_CHARS) - 1)]

# Precompute lookup table for fast access
ASCII_LOOKUP = [brightness_to_ascii(b) for b in range(256)]


def render_pillow_image(img, screen, quantize_bits=4):
    rgb = img.convert("RGB")
    img_width, img_height = rgb.size

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

    # Load pixels for fast C-level access
    rgb_pixels = rgb.load()
    buf = screen.buffer
    lookup = ASCII_LOOKUP

    for y in range(new_height):
        row = buf[y + y_offset]
        for x in range(new_width):
            r, g, b = rgb_pixels[x, y]
            # Standard luminance formula to calculate brightness using fast integer math
            brightness = (r * 77 + g * 150 + b * 29) >> 8
            char = lookup[brightness]
            
            # Quantize color to reduce the number of unique colors in the frame
            if quantize_bits > 0:
                rq = (r >> quantize_bits) << quantize_bits
                gq = (g >> quantize_bits) << quantize_bits
                bq = (b >> quantize_bits) << quantize_bits
                row[x + x_offset] = (char, (rq, gq, bq))
            else:
                row[x + x_offset] = (char, (r, g, b))

    screen.render()
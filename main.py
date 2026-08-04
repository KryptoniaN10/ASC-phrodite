from screen import Screen
from image_renderer import render_image

screen = Screen(80, 40)

screen.clear_terminal()

render_image("boombang.png", screen)
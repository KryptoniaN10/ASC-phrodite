from screen import Screen
from video_renderer import play_video

screen = Screen(200,100)

screen.clear_terminal()

play_video("media/odyssey.mp4", screen)
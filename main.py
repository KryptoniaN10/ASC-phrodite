from screen import Screen
from video_renderer import play_video

screen = Screen(200,100)

screen.clear_terminal()

play_video("test.mp4", screen)
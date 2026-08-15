import cv2
from PIL import Image
from image_renderer import render_pillow_image

def play_video(filename, screen):
    video = cv2.VideoCapture(filename)

    while True:

        success, frame = video.read()

        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(frame_rgb)

        # update terminal size so rendering always fits current terminal
        try:
            screen.update_size()
        except Exception:
            pass

        render_pillow_image(img, screen)

    video.release()
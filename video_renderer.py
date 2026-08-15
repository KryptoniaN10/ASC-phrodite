import cv2
from PIL import Image
import time
from image_renderer import render_pillow_image

def play_video(filename, screen):
    video = cv2.VideoCapture(filename)
    fps=video.get(cv2.CAP_PROP_FPS)

    if(fps<0):
        print("could not determine video fps")
        video.release()
        return 
    frame_duration=1/fps

    while True:
        start=time.perf_counter()
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
        elapsed=time.perf_counter()-start
        remaining=frame_duration-elapsed
        if(remaining>0):
            time.sleep(remaining)

    video.release()
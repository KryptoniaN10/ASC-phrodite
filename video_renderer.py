import cv2
from PIL import Image
import time
from image_renderer import render_pillow_image

def play_video(filename, screen):
    video = cv2.VideoCapture(filename)
    video_fps=video.get(cv2.CAP_PROP_FPS)

    if(video_fps<=0):
        print("could not determine video fps")
        video.release()
        return 
    frame_duration = 1 / video_fps
    start_time = time.perf_counter()
    frame_count = 0
    rendered_count = 0
    try:
        while True:
            target_time = start_time + frame_count * frame_duration
            
            success, frame = video.read()
            if not success:
                break

            frame_count += 1

            # Frame Dropping: If we are late by more than a frame duration, skip rendering to catch up
            now = time.perf_counter()
            if now > target_time + frame_duration:
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)

            # update terminal size so rendering always fits current terminal (throttled)
            if frame_count % 30 == 0:
                try:
                    screen.update_size()
                except Exception:
                    pass

            render_pillow_image(img, screen)
            rendered_count += 1

            # High-Precision Sleep:
            # Sleep for the bulk of the duration (leaving 5ms margin for Windows timer resolution)
            now = time.perf_counter()
            remaining = target_time - now
            if remaining > 0.010:
                time.sleep(remaining - 0.005)
            # Spin-wait for the exact target time to achieve microsecond alignment
            while time.perf_counter() < target_time:
                pass
    finally:
        video.release()
        
    total_time = time.perf_counter() - start_time
    average_fps = rendered_count / total_time
    actual_fps = frame_count / total_time

    print(f"\nVideo FPS: {video_fps:.2f}")
    print(f"Frames decoded: {frame_count}")
    print(f"Frames rendered: {rendered_count} (Dropped: {frame_count - rendered_count})")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average Render FPS: {average_fps:.2f}")
    print(f"Actual Playback FPS: {actual_fps:.2f}")

import cv2
from PIL import Image
import time
from image_renderer import render_pillow_image
from audio_extractor import extract_audio
from audio_player import AudioPlayer


def play_video(filename, screen):
    video = cv2.VideoCapture(filename)
    video_fps = video.get(cv2.CAP_PROP_FPS)

    if video_fps <= 0:
        print("could not determine video fps")
        video.release()
        return

    frame_duration = 1 / video_fps

    audio_path = extract_audio(filename)
    audio = AudioPlayer()
    has_audio = False
    if audio_path:
        try:
            audio.load(audio_path)
            has_audio = True
        except Exception as e:
            print(f"Failed to load audio: {e}")

    try:
        screen.update_size()
    except Exception:
        pass

    if has_audio:
        audio.play()

    start_time = time.perf_counter()
    frame_index = 0
    current_frame = None
    try:
        while True:
            if has_audio and audio.is_finished():
                break

            if has_audio:
                current_time = audio.get_position()
            else:
                current_time = time.perf_counter() - start_time

            target_frame = int(current_time * video_fps)

            while frame_index <= target_frame:
                success, frame = video.read()
                if not success:
                    return
                frame_index += 1
                current_frame = frame

            if current_frame is None:
                continue

            if frame_index % 30 == 0:
                try:
                    screen.update_size()
                except Exception:
                    pass

            frame_rgb = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            render_pillow_image(img, screen)

            if not has_audio:
                target_time = frame_index * frame_duration
                now = time.perf_counter() - start_time
                remaining = target_time - now
                if remaining > 0.010:
                    time.sleep(remaining - 0.005)
                while time.perf_counter() - start_time < target_time:
                    pass

    finally:
        if has_audio:
            audio.stop()
        video.release()
        if audio_path:
            try:
                import os
                os.unlink(audio_path)
            except Exception:
                pass

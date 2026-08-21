import subprocess
import tempfile
import os


def _get_ffmpeg_path():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def extract_audio(video_path):
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_wav.close()

    ffmpeg = _get_ffmpeg_path()

    try:
        result = subprocess.run(
            [
                ffmpeg, "-y",
                "-i", video_path,
                "-vn",
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                temp_wav.name,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            if "does not contain any stream" in result.stderr or "No audio stream" in result.stderr:
                print("No audio track found in video.")
                os.unlink(temp_wav.name)
                return None
            print(f"ffmpeg error: {result.stderr.strip()}")
            os.unlink(temp_wav.name)
            return None

        return temp_wav.name

    except FileNotFoundError:
        print("ffmpeg not found. Audio playback disabled.")
        if os.path.exists(temp_wav.name):
            os.unlink(temp_wav.name)
        return None

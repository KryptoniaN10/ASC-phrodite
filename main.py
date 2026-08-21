import subprocess
import sys

REQUIRED = ["opencv-python", "Pillow", "sounddevice", "soundfile", "numpy", "imageio-ffmpeg"]


def ensure_deps():
    missing = []
    for pkg in REQUIRED:
        try:
            __import__(pkg.replace("-", "_").split("[")[0])
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])


ensure_deps()

from screen import Screen
from video_renderer import play_video

screen = Screen(200, 100)

screen.clear_terminal()

try:
    play_video("media/bnd.mp4", screen)
except KeyboardInterrupt:
    pass

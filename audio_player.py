import sounddevice as sd
import soundfile as sf
import time
import threading


class AudioPlayer:
    def __init__(self):
        self._data = None
        self._samplerate = None
        self._channels = None
        self._start_time = 0.0
        self._playing = False
        self._finished = False

    def load(self, wav_path):
        self._data, self._samplerate = sf.read(wav_path, dtype="float32")
        if self._data.ndim == 1:
            self._channels = 1
            self._data = self._data.reshape(-1, 1)
        else:
            self._channels = self._data.shape[1]

    def play(self):
        if self._data is None:
            return
        self._playing = True
        self._finished = False
        self._start_time = time.perf_counter()
        threading.Thread(target=self._play_loop, daemon=True).start()

    def _play_loop(self):
        try:
            sd.play(self._data, self._samplerate, blocking=True)
        except Exception as e:
            print(f"Audio playback error: {e}")
        finally:
            self._playing = False
            self._finished = True

    def get_position(self):
        if not self._playing:
            return 0.0
        return time.perf_counter() - self._start_time

    def is_playing(self):
        return self._playing

    def is_finished(self):
        return self._finished

    def stop(self):
        self._playing = False
        try:
            sd.stop()
        except Exception:
            pass

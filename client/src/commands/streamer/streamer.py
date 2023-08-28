import subprocess
from typing import Optional


class Streamer:
    def __init__(
            self,
            stream_host: str,
            username: str,
            password: str,
            port: int = 1985,
            ffmpeg_threads: int = 2,
            resolution: str = "1280x720",
            frames: int = 30
    ):
        self._stream_host = stream_host
        self._username = username
        self._password = password
        self._port = port
        self._ffmpeg_threads = ffmpeg_threads
        self._resolution = resolution
        self._frames = frames

        self._cmd = f"/usr/local/src/ffmpeg-webrtc/ffmpeg -f v4l2 -framerate {self._frames} -i /dev/video0 \
                    -f lavfi -i anullsrc \
                    -vcodec libx264 -pix_fmt yuv420p -profile:v baseline -preset:v ultrafast -b:v 800k \
                    -s {self._resolution} -r {self._frames} -g 60 -tune zerolatency -threads {self._ffmpeg_threads} -bf 0 \
                    -acodec libopus -ar 48000 -ac 2 \
                    -f whip \"{self._stream_host}:{self._port}/rtc/v1/whip/?app=live&stream=livestream&username={self._username}&password={self._password}&\""

        self._process: Optional[subprocess.Popen] = None

    def start(self) -> None:
        if self._process is None:
            self._process = subprocess.Popen(self._cmd, shell=True)

    def stop(self) -> None:
        if self._process:
            self._process.terminate()
            self._process = None

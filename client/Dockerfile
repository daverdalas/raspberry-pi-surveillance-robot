FROM python:3.11-alpine

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1

RUN apk update && apk add --no-cache  \
    bash \
    libffi-dev \
    openssl-dev \
    build-base \
    rust \
    cargo \
    git \
    pkgconfig \
    opus-dev \
    x264-dev

RUN cargo install watchexec-cli
RUN cp /root/.cargo/bin/watchexec /bin

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /usr/local/src
# Install ffmpeg with WHIP support
RUN git clone -b feature/rtc-muxer https://github.com/winlinvip/ffmpeg-webrtc.git
RUN cd ffmpeg-webrtc && ./configure --disable-asm --enable-muxer=whip --enable-openssl --enable-version3 \
                            --enable-libx264 --enable-gpl --enable-libopus
RUN cd ffmpeg-webrtc && make -j10

# on PI ./ffmpeg \
        #-f v4l2 -framerate 30 -i /dev/video0 \
        #-f lavfi -i anullsrc \
        #-vcodec libx264 -pix_fmt yuv420p -profile:v baseline -preset:v ultrafast -b:v 800k \
        #-s 1280x720 -r 30 -g 60 -tune zerolatency -threads 1 -bf 0 \
        #-acodec libopus -ar 48000 -ac 2 \
        #-f whip "http://192.168.0.129:1985/rtc/v1/whip/?app=live&stream=livestream"
#macos ./ffmpeg -f avfoundation -framerate 30 -i "0:0" \
       #    -vcodec libx264 -pix_fmt yuv420p -profile:v baseline -preset:v ultrafast \
       #    -b:v 800k -s 640x480 -r 30 -g 60 -tune zerolatency -threads 1 -bf 0 \
       #    -acodec libopus -ar 48000 -ac 2 \
       #    -f whip "http://192.168.0.129:1985/rtc/v1/whip/?app=live&stream=livestream"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
COPY src /app/src

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /app

ENTRYPOINT ["tail", "-f", "/dev/null"]

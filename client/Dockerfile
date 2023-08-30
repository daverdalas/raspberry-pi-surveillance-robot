FROM python:alpine3.18 AS build

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
RUN pip install "poetry==$POETRY_VERSION"

RUN wget --output-document=download.zip https://github.com/joan2937/pigpio/archive/master.zip \
    # Downloaded content is placed inside specific folder to not be depended of branch naming from repo
    && mkdir download \
    && unzip -d download download.zip \
    && cd /download/* \
    # Fix for compiling on Alpine, https://github.com/joan2937/pigpio/issues/107
    && sed -i -e 's/ldconfig/echo ldconfig disabled/g' Makefile \
    && make \
    && make install

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

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

COPY . /app

ENTRYPOINT ["tail", "-f", "/dev/null"]

FROM build as local

RUN cargo install watchexec-cli
RUN cp /root/.cargo/bin/watchexec /bin

ENTRYPOINT ["tail", "-f", "/dev/null"]

FROM build as production

STOPSIGNAL SIGKILL
EXPOSE 8888

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["tail", "-f", "/dev/null"]

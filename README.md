# Line Up Notifier

The software reads video stream from connected webcam or Bilibili Live (downloaded using [bilibili-live-recorder](https://github.com/zachMelody/bilibili-live-recorder), will be sent to [rtsp-simple-server](https://github.com/aler9/rtsp-simple-server) via [ffmpeg](https://github.com/FFmpeg/FFmpeg) first), and analyzes the stream with [yolov7](https://github.com/WongKinYiu/yolov7).

After getting a rough number of people in stream, it sends a warning message to a certain QQ group using [Nonebot](https://github.com/nonebot/nonebot), if the number is low enough.

## Requirements

Docker is recommended.

## Configuration

### Specify QQ Account

Execute `go-cqhttp/go-cqhttp.tar.gz` first, you'll get a `config.yml`.

Edit it according to [go-cqhttp](https://github.com/Mrs4s/go-cqhttp).

### Edit Bilibili Live Room ID

In `compose-files/docker-compose.yml`, edit `ROOM_ID`.

### Edit MySQL Password

In `compose-files/docker-compose.yml`, edit `PASSWORD`.

### Edit QQ Debugger and Group

In `qq_bot`, create `secret.py`, fill in:

```python
secret_qq_debugger = YOUR_QQ
secret_qq_group = YOUR_QQ_GROUP
```

### Edit message

In `qq_bot/localize.py`, edit function `send` and/or `interp`.

## Deploy

Execute the following commands in root folder:

```shell
docker build -t go-cqhttp ./go-cqhttp
docker build -t bili-live-rec ./live-rec
docker build -t qq-bot ./qq_bot
docker build -t nab-server ./go-server/src
docker build -t nab-yolov7 ./yolov7
```

In `compose-files`, execute `docker-compose up -d`.

## Stack

- Golang: [Gin](https://github.com/gin-gonic/gin), [Gorm](https://github.com/go-gorm/gorm), [go-cqhttp](https://github.com/Mrs4s/go-cqhttp), [rtsp-simple-server](https://github.com/aler9/rtsp-simple-server)
- Python: [yolov7](https://github.com/WongKinYiu/yolov7), [Nonebot](https://github.com/nonebot/nonebot), [bilibili-live-recorder](https://github.com/zachMelody/bilibili-live-recorder)
- [ffmpeg](https://github.com/FFmpeg/FFmpeg)
- Mysql

## Contribute

Pull requests are welcomed :)

## License

As yolov7 is licensed by GPL-3.0, this software inherits GPL-3.0 as well.

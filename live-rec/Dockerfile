# 建立 python3.7 环境
FROM python:3.7-alpine

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 设置 pip 源为国内源
COPY pip.conf /root/.pip/pip.conf

# 创建文件夹
RUN mkdir -p /app

# 设置容器内工作目录
WORKDIR /app

# 设置 apk 镜像源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

# 更新设置
RUN apk update

# 添加 ffmpeg
RUN apk add --no-cache ffmpeg

# 先复制依赖包
COPY ./requirements.txt .

# 利用 pip 安装依赖
RUN pip install -r requirements.txt

# 修改时区
RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata

# 将当前目录文件加入到容器工作目录中（. 表示当前宿主机目录）
COPY . .

# 执行测试
CMD ["/bin/bash", "-c", "python test.py"]
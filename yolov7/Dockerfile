# 建立 python3.7 环境
FROM python:3.7

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 设置 pip 源为国内源
COPY pip.conf /root/.pip/pip.conf

# 创建文件夹
RUN mkdir -p /app

# 设置容器内工作目录
WORKDIR /app

# 先复制依赖包
COPY ./requirements.txt .

# 利用 pip 安装依赖
RUN pip install -r requirements.txt

# 设置 apt-get 镜像源
RUN sed -i "s@http://deb.debian.org@https://mirrors.ustc.edu.cn@g" /etc/apt/sources.list

# 添加需要的包
RUN apt-get update
RUN sh -c '/bin/echo -e "Y" | apt-get install libgtk2.0-dev'
RUN sh -c '/bin/echo -e "Y" | apt-get install pkg-config'
RUN sh -c '/bin/echo -e "Y" | apt-get install python3-opencv'

# 修改时区
ENV TZ="Asia/Shanghai"

# 复制 models
COPY ./models .

# 将当前目录文件加入到容器工作目录中（. 表示当前宿主机目录）
COPY ./code .

# 利用 bash 运行一条命令
CMD ["/bin/bash", "-c", "python detect_exporting.py --source rtsp://rtsp-server:8554/1 --weights yolov7x.pt --nosave"]
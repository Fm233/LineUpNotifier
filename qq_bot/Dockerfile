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

# 安装 scheduler 模块
RUN pip install "nonebot[scheduler]"

# 将当前目录文件加入到容器工作目录中（. 表示当前宿主机目录）
COPY . .

# 修改时区
ENV TZ="Asia/Shanghai"

# 利用 bash 运行多条命令
CMD ["/bin/bash", "-c", "python init.py"]
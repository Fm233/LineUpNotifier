# 建立 alpine 环境
FROM alpine:latest

# 新建文件夹
RUN mkdir -p /app

# 设置容器内工作目录
WORKDIR /app

# 将当前目录文件加入到容器工作目录中（. 表示当前宿主机目录）
ADD ./go-cqhttp.tar.gz .

# 复制配置文件
COPY ./config .

# 设置 apk 镜像源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

# 修改时区
RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata

# 运行 go-cqhttp
CMD ["./go-cqhttp"]
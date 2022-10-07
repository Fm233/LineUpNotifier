# 创建 Golang 编译镜像
FROM golang:1.19.1-alpine3.16 AS builder
WORKDIR /build
RUN adduser -u 10001 -D app-runner

# 下载依赖
ENV GOPROXY https://goproxy.cn
COPY go.mod .
COPY go.sum .
RUN go mod download

# 编译项目
COPY . .
RUN CGO_ENABLED=0 GOARCH=amd64 GOOS=linux go build -a -o go-server .

# 创建纯净 Alpine 镜像
FROM alpine:3.16 AS final
WORKDIR /app

# 修改时区
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update \
    && apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata

# 复制资源
COPY --from=builder /build/go-server ./
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# 低权运行应用
ENV GIN_MODE=release
USER app-runner
ENTRYPOINT ["/app/go-server"]
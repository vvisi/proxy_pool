FROM python:3.6-alpine

LABEL maintainer="vvvis <zjhdota@163.com>"

WORKDIR /app

COPY ./requirements.txt .

# apk 源为官方源
RUN sed -i 's|http://dl-cdn.alpinelinux.org/alpine/|http://dl-cdn.alpinelinux.org/alpine/v3.15/|g' /etc/apk/repositories

# timezone
RUN apk add -U tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && apk del tzdata

# runtime environment
RUN apk add bash musl-dev gcc libxml2-dev libxslt-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev

COPY . .

EXPOSE 5010

ENTRYPOINT [ "sh", "start.sh" ]

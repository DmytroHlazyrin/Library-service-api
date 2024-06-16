FROM python:3.12-slim
LABEL maintainer="dmytro.hlazyrin@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHOUNNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p /files/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user
RUN chown -R my_user /files/media/
RUN chown -R 755 /files/media

USER my_user


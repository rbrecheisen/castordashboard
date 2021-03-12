FROM python:3.9.2
MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt
RUN mkdir /static
RUN mkdir /src
WORKDIR /src

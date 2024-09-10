FROM python:3.12

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y libusb-1.0-0
RUN pip install poetry
RUN cp -n default_setup.json setup.json
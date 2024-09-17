FROM python:3.12

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y libusb-1.0-0
RUN pip install poetry
RUN poetry config virtualenvs.create false # to install dependencies system wide and not in a venv
RUN make venv
RUN cp -n default_setup.json setup.json

ENV PYTHONPATH="/app/src"
CMD ["python", "src/main.py"]
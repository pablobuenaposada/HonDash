FROM python:3.11

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install --no-install-recommends -y libusb-1.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv && make venv
RUN cp -n default_setup.json setup.json

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
CMD ["python", "src/main.py"]

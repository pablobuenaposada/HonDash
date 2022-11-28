# Docker image for installing dependencies on Linux and running tests.
# Build with:
# docker build --tag=pablobuenaposada/hondash .
# Run with:
# docker run pablobuenaposada/hondash /bin/sh -c 'make test'
# Or for interactive shell:
# docker run -it --rm pablobuenaposada/hondash
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive
ENV PY_FILE=src/backend/main.py

RUN apt update && apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa

WORKDIR /app
COPY . /app

RUN apt install --yes --no-install-recommends \
	lsb-release make sudo && \
	make system_dependencies

RUN make virtualenv
RUN cp -n default_setup.json setup.json
CMD sudo PYTHONPATH=src venv/bin/python $PY_FILE
# Docker image for installing dependencies on Linux and running tests.
# Build with:
# docker build --tag=hondash .
# Run with:
# docker run hondash /bin/sh -c '. venv/bin/activate && make test'
# Or for interactive shell:
# docker run -it --rm hondash
# TODO:
#	- delete archives to keep small the container small
#	- setup caching (for apt, and pip)
FROM ubuntu:18.04

# configure locale
RUN apt update -qq > /dev/null && apt install --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# install system dependencies
RUN apt update -qq > /dev/null && apt install --yes --no-install-recommends \
	python3 python3-dev virtualenv make lsb-release pkg-config git build-essential \
    libssl-dev tox

WORKDIR /app
COPY . /app
RUN make virtualenv

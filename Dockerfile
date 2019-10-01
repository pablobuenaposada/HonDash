# Docker image for installing dependencies on Linux and running tests.
# Build with:
# docker build --tag=hondash .
# Run with:
# docker run hondash /bin/sh -c 'make test'
# Or for interactive shell:
# docker run -it --rm hondash
# TODO:
#	- delete archives to keep small the container small
#	- setup caching (for apt, and pip)
FROM ubuntu:19.04

# configure locale
RUN apt update -qq > /dev/null && apt install --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

WORKDIR /app
COPY . /app

RUN apt update -qq > /dev/null && apt install --yes --no-install-recommends \
	lsb-release make sudo && \
	make system_dependencies
RUN make virtualenv

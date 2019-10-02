# Docker image for installing dependencies on Linux and running tests.
# Build with:
# docker build --tag=pablobuenaposada/hondash .
# Run with:
# docker run pablobuenaposada/hondash /bin/sh -c 'make test'
# Or for interactive shell:
# docker run -it --rm pablobuenaposada/hondash
FROM ubuntu:18.04

# configure locale
RUN apt update -qq > /dev/null && apt install --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

WORKDIR /app
COPY Makefile /app

RUN apt update -qq > /dev/null && apt install --yes --no-install-recommends \
	lsb-release make sudo && \
	make system_dependencies
COPY . /app
RUN make virtualenv

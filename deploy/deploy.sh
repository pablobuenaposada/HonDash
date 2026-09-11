#!/bin/sh
# Brings the demo stack on the droplet up to date with whatever is checked out.
#
# This lives in the repository rather than inside the cloud-init user_data on
# purpose: changing a droplet's user_data replaces the droplet, so keeping the
# deploy steps here means they can be edited without ever destroying anything.
set -eu

unset CDPATH
cd "$(dirname -- "$0")/.."

# the backend comes from the registry, the frontend is built from its own repo
docker compose -f docker-compose.demo.yml pull --ignore-buildable
docker compose -f docker-compose.demo.yml up -d --build --remove-orphans
docker image prune -f

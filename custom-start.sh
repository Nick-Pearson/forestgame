#! /usr/bin/env sh
echo "Custom start running"
LISTEN_PORT=${PORT:-80}
echo "Port: ${LISTEN_PORT}"

exec "/start.sh"

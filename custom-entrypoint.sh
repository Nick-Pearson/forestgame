#! /usr/bin/env sh
echo "Custom entrypoint running"
LISTEN_PORT=${PORT:-80}
echo "Port: ${LISTEN_PORT}"

exec "/entrypoint.sh"

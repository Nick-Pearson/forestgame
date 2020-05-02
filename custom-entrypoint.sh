#! /usr/bin/env sh
export LISTEN_PORT=${PORT:-80}
echo "Server starting on port ${LISTEN_PORT}"
exec 'sh /main-entrypoint.sh'
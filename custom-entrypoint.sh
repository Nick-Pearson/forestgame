#! /usr/bin/env sh
export LISTEN_PORT=${PORT:-80}
echo "Server starting on port ${LISTEN_PORT}"
ls
echo "Running:"
cat '/main-entrypoint.sh'
exec '/main-entrypoint.sh'
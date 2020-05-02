#! /usr/bin/env sh
export LISTEN_PORT=${PORT:-80}
echo "Server starting on port ${LISTEN_PORT}"
pwd
echo "ls"
ls
echo "ls /"
ls /
echo "Running:"
cat '/main-entrypoint.sh'
exec '/main-entrypoint.sh'
#!/bin/bash

set -e

SUPERVISOR_APP_NAME=$1
APP_WSGI=$2
APP_PORT_NUMBER=$3
DJANGO_SETTINGS_MODULE="${APP_WSGI:0:${#APP_WSGI}-5}.settings.dev"

# Create main Supervisord config file
echo "=> Creating supervisord config"

mkdir -p /etc/supervisor/conf.d/ && \
    mkdir -p /var/log/supervisor && \

cat > /etc/supervisord.conf <<-EOM
; supervisor config file

[unix_http_server]
file=/var/run/supervisor.sock   ; (the path to the socket file)
chmod=0700                       ; sockef file mode (default 0700)

[supervisord]
logfile=/var/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
childlogdir=/var/log/supervisor            ; ('AUTO' child log dir, default $TEMP)

; the below section must remain in the config file for RPC
; (supervisorctl/web interface) to work, additional interfaces may be
; added by defining them in separate rpcinterface: sections
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///var/run/supervisor.sock ; use a unix:// URL  for a unix socket

; The [include] section can just contain the "files" setting.  This
; setting can list multiple files (separated by whitespace or
; newlines).  It can also contain wildcards.  The filenames are
; interpreted as relative to this file.  Included files *cannot*
; include files themselves.

[include]
files = /etc/supervisor/conf.d/*.conf
EOM

# Redis
echo "=> Creating Redis supervisor config"
cat > /etc/supervisor/conf.d/redis.conf <<-EOM
[program:redis]
command = redis-server
directory = /
redirect_stderr = true
EOM

# App
echo "=> Creating Tracker supervisor config"
cat > /etc/supervisor/conf.d/app.conf <<-EOM
[program:$SUPERVISOR_APP_NAME]
command = gunicorn --bind 0.0.0.0:$APP_PORT_NUMBER $APP_WSGI
environment = DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE"
directory = /deploy/
redirect_stderr = true
EOM

echo "=> Starting Supervisord"
supervisord -c /etc/supervisord.conf

echo "=> Tailing logs"
tail -qF /var/log/supervisor/*.log

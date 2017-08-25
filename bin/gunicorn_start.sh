#!/bin/bash

NAME="unifinca_app"
DJANGODIR=/home/jortiz/unifinca/
SOCKFILE=/home/jortiz/unifinca/run/gunicorn.sock
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=unifinca.settings
DJANGO_WSGI_MODULE=unifinca.settings

echo "Starting $NAME as 'choluteca'"

cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-files=-

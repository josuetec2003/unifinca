APPNAME=unifinca
APPDIR=/home/jortiz/unifinca/
LOGDIR=/home/jortiz/log/

LOGFILE=$LOGDIR'gunicorn.log'
ERRORFILE=$LOGDIR'gunicorn-error.log'

NUM_WORKERS=3

ADDRESS=127.0.0.1:8001

#cd $APPDIR
echo "Vamos a cargar source ~/.bashrc para unifinca"
source ~/.bashrc
echo "Vamos con el workon de unifinca"
source /home/jortiz/.virtualenvs/unifinca/bin/activate
echo "Ya esta unifinca"

exec gunicorn unifinca.wsgi:application \
-w $NUM_WORKERS --bind=$ADDRESS \
--log-level=debug \
--log-file=$LOGFILE 2>>$LOGFILE  1>>$ERRORFILE &

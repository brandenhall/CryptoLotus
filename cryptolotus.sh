#! /bin/bash
### BEGIN INIT INFO
# Provides:          CryptoLotus
# Required-Start:    $local_fs $remote_fs $network $syslog
# Required-Stop:     $local_fs $remote_fs $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start/stop CryptoLotus server
### END INIT INFO

logger "CryptoLotus: Start script executed"

pushd `dirname $0` > /dev/null
CRYPTOLOTUSPATH=`pwd -P`
popd > /dev/null

export PYTHONPATH="$CRYPTOLOTUSPATH:$PYTHONPATH"
export CRYPTOLOTUSPATH="$CRYPTOLOTUSPATH"

case "$1" in
  start)
    logger "CryptoLotus: Starting"
    echo "Starting cryptolotus..."
    source ./env/bin/activate && ./env/bin/twistd -y "$CRYPTOLOTUSPATH/cryptolotus.py" -l "$CRYPTOLOTUSPATH/logs/cryptolotus.log" --pidfile "$CRYPTOLOTUSPATH/cryptolotus.pid"
    ;;
  stop)
    logger "CryptoLotus: Stopping"
    echo "Stopping CryptoLotus..."
    kill `cat "$CRYPTOLOTUSPATH/cryptolotus.pid"`
    ;;
  debug)
    logger "CryptoLotus: Debugging"
    echo "Starting CryptoLotus..."
    source ./env/bin/activate && ./env/bin/twistd -noy "$CRYPTOLOTUSPATH/cryptolotus.py" --pidfile "$CRYPTOLOTUSPATH/cryptolotus.pid"
    ;;
  *)
    logger "CryptoLotus: Invalid usage"
    echo "Usage: CryptoLotus {start|stop}"
    exit 1
    ;;
esac

exit 0

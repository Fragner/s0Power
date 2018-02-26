#! /bin/sh

### BEGIN INIT INFO
# Provides:		s0Power2vz
# Required-Start:	$remote_fs $syslog
# Required-Stop:	$remote_fs $syslog
# Default-Start:	2 3 4 5
# Default-Stop:		1
# Short-Description: S0/Impulse->Power to Volkszaehler 'RaspberryPI deamon'
#### END INIT INFO

set -e 

DAEMON=/usr/local/sbin/s0Power2vz
PIDFILE=/tmp/s0Power2vz.pid


# /etc/init.d/s0Power2vz: start and stop the s0Powervz daemon

test -x ${DAEMON} || exit 0

### umask 022

## . /lib/lsb/init-functions

### export PATH="${PATH:+$PATH:}/usr/local/sbin"

case "$1" in

	start)
		test ! -f $PIDFILE || { echo "Deamon already running!"; exit 0; }
		chrt -r 99 su -c $DAEMON pi
		su -c "renice -99 `pidof $DAEMON`" >/dev/null 2>&1
		;;

	stop)
		killall -q s0Power2vz
		rm -f /tmp/s0Power2vz.pid
		;;

	restart)
		$0 stop
		$0 start
		;;

	*)
	echo "Usage: $0 {start|stop|restart}"
	exit 1
	;;
esac

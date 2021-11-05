S0/Impulse to Volkszaehler daemon.
==================================

This is a Linux SYSFS daemon. Written in ANSI C, provides low memory signature and minimal CPU load.  
Its fully interrupt driven with no cpu eating idle loops!

Hardware by Udo S.  
http://wiki.volkszaehler.org/hardware/controllers/raspberry_pi_erweiterung

![My image](http://wiki.volkszaehler.org/_media/hardware/controllers/raspi_6xs0_3x1-wire_1xir_bestueckt.png?w=200)  

Backend-Software  
http://volkszaehler.org/

![My image](http://wiki.volkszaehler.org/_media/software/releases/demo-screenshot.jpg?w=300)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Raspberry pi preparation
============
### Configure GPIO as input<br>
At first it must created<br>
eg GPIO2:
```
echo 2 > /sys/class/gpio/export
```
now set as input
```
echo in > /sys/class/gpio/gpio2/direction
```

### GPIO-state
To determine the state, i.e. "high" or "low", at a GPIO, the following command is sufficient. The GPIO can be both an input and an output.
```
cat /sys/class/gpio/gpio2/value
```
Installation
============

Precondition: Raspian Linux (http://www.raspberrypi.org/downloads) 

Binding libraries: libcurl & libconfig -> 'sudo apt-get install libcurl4-gnutls-dev libconfig-dev'

Download: 'sudo git clone https://github.com/fragner/s0Power2vz /usr/local/src/s0Power2vz'

---

s0Power2vz.c	-> 'sudo gcc -o /usr/local/sbin/s0Power2vz /usr/local/src/s0Power2vz/s0Power2vz.c -lconfig -lcurl'
or ./compile.sh

s0Power2vz.cfg	-> /etc/  

s0Power2vz.service	-> /etc/systemd/system/


Configuration
=============
```
sudo nano /etc/s0Power2vz.cfg ( edit your config )
```
Autostart:
```
sudo systemctl daemon-reload
sudo systemctl enable s0Power2vz.service (make deamon autostart) 
sudo systemctl start s0Power2vz.service
```


License
=======
This is a fork from https://github.com/w3llschmidt/s0vz


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

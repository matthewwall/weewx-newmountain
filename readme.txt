weewx-nm150

This is a driver for weewx that collects data from New Mountain NM150
weather stations.

  http://www.newmountain.com/acoustic-weather-station/

Installation

0) install weewx, select 'Simulator' driver (see the weewx user guide)

dpkg -i weewx_x.y.z-r.deb

0) install python NMEA library

pip install pynmea2

1) download the driver

wget -O weewx-nm150.zip https://github.com/matthewwall/weewx-nm150/archive/master.zip

2) install the driver

wee_extension --install weewx-nm150.zip

3) configure the driver

wee_config --reconfigure

4) start weewx

sudo /etc/init.d/weewx start

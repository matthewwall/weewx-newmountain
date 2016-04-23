weewx-newmountain

This is a driver for weewx that collects data from New Mountain
weather stations.


Installation

0) install weewx, select 'Simulator' driver (see the weewx user guide)

dpkg -i weewx_x.y.z-r.deb

1) download the driver

wget -O weewx-newmountain.zip https://github.com/matthewwall/weewx-newmountain/archive/master.zip

2) install the driver

wee_extension --install weewx-newmountain.zip

3) configure the driver

wee_config --reconfigure

4) start weewx

sudo /etc/init.d/weewx start

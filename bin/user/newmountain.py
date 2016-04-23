#!/usr/bin/env python
# NewMountain driver for weewx
#
# Copyright 2016 Matthew Wall, all rights reserved
#
# based on implementation by Jonathan Lassof
#   https://github.com/weewx/weewx/pull/107
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.
#
# See http://www.gnu.org/licenses/

"""A weewx driver for New Mountain NMEA-0183-based stations.

The New Mountain NM150 is an ultrasonic weather station with no moving parts:

  http://www.newmountain.com/acoustic-weather-station/

This driver requires the pynmea library for NMEA0183 protocol:
  https://github.com/Knio/pynmea2
To install pynmea2:
  pip install pynmea2
The pynmea2 library is compatible with Python 2.7.  This driver may not work
with older versions of Python.
"""

import pynmea2
import re
import serial
import syslog
import time
import weewx
import weewx.drivers
import weewx.units

DRIVER_NAME = 'NewMountain'
DRIVER_VERSION = "0.2"


def loader(config_dict, _):
    return NewMountain(**config_dict[DRIVER_NAME])

def confeditor_loader():
    return NewMountainConfEditor()

def logmsg(level, msg):
    syslog.syslog(level, 'newmountain: %s' % msg)

def logdbg(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)


DEFAULT_PORT = '/dev/ttyUSB0'
DEFAULT_BAUD = 4800

class NewMountain(weewx.drivers.AbstractDevice):
    def __init__(self, **stn_dict):
        port = stn_dict.get('port', DEFAULT_PORT)
        baudrate = int(stn_dict.get('baud', DEFAULT_BAUD))
        timeout = 3 # seconds
        self.serial_port = serial.Serial(port, baudrate, timeout=timeout)
        
    def closePort(self):
        if self.serial_port is not None:
            self.serial_port.close()
            self.serial_port = None

    @property
    def hardware_name(self):
        return 'NewMountain'

    def genLoopPackets(self):
        while True:
            try:
                wimda_packet = self.get_wimda_packet()
                logdbg("wimda: %s" % wimda_packet)
                parsed = pynmea2.parse(wimda_packet)
                logdbg("parsed: %s" % parsed)
                packet = dict()
                packet['usUnits'] = weewx.US
                packet['dateTime'] = int(time.time() + 0.5)
                packet['barometer'] = float(wimda.b_pressure_inch)
                degree_C = (float(wimda.air_temp),
                            'degree_C', 'group_temperature')
                degree_F = weewx.units.convert(degree_C, 'degree_F')[0]
                packet['outTemp'] = degree_F
                wind_speed_knots = (
                    float(mda.wind_speed_knots), 'knot', 'group_speed')
                wind_speed_mph = weewx.units.convert(
                    wind_speed_knots, 'mile_per_hour')[0]
                packet['windSpeed'] = wind_speed_mph
                packet['windDir'] = float(mda.direction_true)
                logdbg("packet: %s" % packet)
                yield packet
            except (ValueError, serial.serialutil.SerialException), e:
                logerr("LOOP data failed: %s" % e)

    def get_wimda_packet(self):
        buf = ''
        while True:
            chunk = self.serial_port.read(70)
            chunk = chunk.strip('\00')
            buf = buf + chunk
            matches = re.search(r'(\$WIMDA,.*)\n', buf)
            if matches:
                return matches.group(1)


class NewMountainConfEditor(weewx.drivers.AbstractConfEditor):
    @property
    def default_stanza(self):
        return """
[NewMountain]
    # This section is for the NewMountain weather station.
    port = /dev/ttyUSB0
    driver = weewx.drivers.NewMountain
"""

    def prompt_for_settings(self):
        print "Specify the serial device NMEA-0183 data is coming in on."
        port = self._prompt('port', DEFAULT_PORT)
        return {'port': port}


# Test the driver by invoking it directly like this:
#   PYTHONPATH=bin python bin/user/newmountain.py

if __name__ == "__main__":
    with NewMountain(port=DEFAULT_PORT) as s:
        for pkt in s.genLoopPackets():
            print repr(pkt)

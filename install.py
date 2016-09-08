# installer for the weewx-nm150 driver
# Copyright 2016 Matthew Wall, all rights reserved

from setup import ExtensionInstaller

def loader():
    return NM150Installer()

class NM150Installer(ExtensionInstaller):
    def __init__(self):
        super(NM150Installer, self).__init__(
            version="0.3",
            name='NM150',
            description='Capture weather data from New Mountain stations',
            author="Matthew Wall",
            author_email="mwall@users.sourceforge.net",
            files=[('bin/user', ['bin/user/nm150.py'])]
            )

# installer for the weewx-newmountain driver
# Copyright 2016 Matthew Wall, all rights reserved

from setup import ExtensionInstaller

def loader():
    return NewMountainInstaller()

class NewMountainInstaller(ExtensionInstaller):
    def __init__(self):
        super(NewMountainInstaller, self).__init__(
            version="0.1",
            name='newmountain',
            description='Capture weather data from New Mountain stations',
            author="Matthew Wall",
            author_email="mwall@users.sourceforge.net",
            files=[('bin/user', ['bin/user/newmountain.py'])]
            )

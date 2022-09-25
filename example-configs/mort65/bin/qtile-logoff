#!/usr/bin/env python
# This script will logout from qtile

from libqtile.command import Client
import getpass
import subprocess

try:
    client = Client()
    client.shutdown()
except:
    subprocess.Popen(["loginctl", "terminate-user", getpass.getuser()])

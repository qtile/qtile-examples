#!/usr/bin/env python
from libqtile import command
import os

lazy = command.Client()

lazy.addgroup("socks")
lazy.group["socks"].toscreen()
os.system("urxvt -vb -rv +sb -fn 'xft:Anonymous Pro:pixelsize=18' -e bash -c '~/.bin/proxy.sh dave.tycho.ws'")

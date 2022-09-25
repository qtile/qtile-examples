#!/bin/bash

exec /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
exec /usr/bin/compton -b &
exec /usr/bin/nm-applet &
exec /usr/bin/volumeicon &
exec /usr/bin/clipit &
exec /usr/bin/indicator-kdeconnect &
exec /usr/bin/udiskie -2 -s &


#!/bin/sh

nitrogen --restore &
picom &
#xcompmgr &
lxpolkit &
urxvtd -q -o -f &
pulseaudio --start &
volumeicon &

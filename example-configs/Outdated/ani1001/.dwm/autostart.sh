#!/bin/sh

nitrogen --restore &
picom -b &
lxpolkit &
slstatus &
mpd &
emacs --daemon &
urxvtd -q -o -f &

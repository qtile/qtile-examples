#!/bin/sh

nitrogen --restore &
picom -b &
lxpolkit &
mpd &
urxvtd -q -o -f &
emacs --daemon &

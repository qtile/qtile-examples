#!/bin/sh

nitrogen --restore &
picom &
lxpolkit &
emacs --daemon &
urxvtd -q -o -f &
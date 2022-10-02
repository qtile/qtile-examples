#!/bin/bash

#use xrandr and arandr to know the
#possible resolutions, frequency
#and the names of your monitors

#IF you know your native resolution and frequency
#for example 1920x1080 @ 60 herz
# type this in your terminal
# gtf 1920 1080 60
# This is the result
# You will need to copy/paste it later.
# 1920x1080 @ 60.00 Hz (GTF) hsync: 67.08 kHz; pclk: 172.80 MHz
# Modeline "1920x1080_60.00"  172.80  1920 2040 2248 2576  1080 1081 1084 1118  -HSync +Vsync

xrandr --newmode "1920x1080_60.00"  172.80  1920 2040 2248 2576  1080 1081 1084 1118  -HSync +Vsync
xrandr --addmode Virtual1 "1920x1080_60.00"
xrandr --output Virtual1 --primary --mode "1920x1080_60.00" --pos 0x0 --rotate normal

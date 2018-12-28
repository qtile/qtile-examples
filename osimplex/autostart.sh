#! /bin/bash 

/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &	# Graphical authentication agent
compton &													# Compositor
nitrogen --restore &										# Wallpaper
light-locker &												# Screen locker
xset b off &												# Disable beep
xfce4-power-manager &										# Power management
nm-applet &													# NetworkManager
redshift-gtk & 												# Red light screen
xfce4-clipman &												# Clipboard management
pa-applet &													# Volume manager
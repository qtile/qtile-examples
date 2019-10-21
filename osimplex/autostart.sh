#! /bin/bash

# If the process doesn't exists, start one in background
run() {
	if ! pgrep $1 ; then
		$@ &
	fi
}

# Just as the above, but if the process exists, restart it
run-or-restart() {
	if ! pgrep $1 ; then
		$@ &
	else
		process-restart $@
	fi
}

# Graphical authentication agent
run /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1

run xset b off 						# Disable beep

run nitrogen --restore 				# Wallpaper
run sxhkd							# Simple X HKey daemon
run tmux new-session -d -s common	# Tmux server
run dunst							# Notification daemon
run compton							# Compositor
run redshift						# Red screen

run volumeicon 						# Volume icon
run nm-applet 						# NetworkManager icon

# Some process you may want to start with Qtile

# run urxvtd -q -o					# URxvt daemon
# run cbatticon						# Battery icon and command
# run xfce4-power-manager 			# Power management
# run light-locker					# Screen locker
# run xfce4-clipman					# Clipboard management
# run mpd --no-daemon					# Music player daemon

# vim: tabstop=4 shiftwidth=4 noexpandtab

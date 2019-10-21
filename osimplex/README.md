osimplex
========

Description
-----------

Qtile example configuration with some OOP.

Features
--------

Here you will find:
1. Some custom lazy functions
1. Default layouts file for groups composition
1. A custom stackwide layout
1. Default widget file for easy bar composition
1. Double and single bar screens, with parameter for systray or no systray
1. A pure text and a powerline like, now broken, bar (from Derek Taylor)
1. Aesthetics file were you can define color, font _et cetera_
	* Put this stuff into aesthetics directory and symlink in configuration root
1. Scratchpad terminal defined with environment variables
1. A "minimized" windows group
1. An autostart script with some suggestions
1. Some window classes and names on rules and groups files

Required
--------

1. A Nerd Font for widgets
	* Was used Ubuntu Nerd Font for this config

Recommended
-----------

1. xcb-util-cursor: Without this, your cursor theme will not work as expected
1. python-psutil: For some widgets
1. python-setproctitle: Qtile will receive a weird process name after restart

Some stuff in this example
--------------------------

Autostart:
1. Polkit agent: polkit-gnome
1. Notification daemon: dunst
1. Compositor: compton
1. Wallpaper setter: nitrogen
1. Hotkeys: sxhkd + Qtile keys
1. Red screen: redshift
1. On systray: network-manager-applet, volumeicon

Scratchpad:
1. Terminal multiplexer: tmux
1. Music player: mpd + ncmpcpp

Notes
-----

1. This config doesn't have no WM related bindings (eg. spawn terminal)
	* Only on Scratchpad
1. Update widget was configured for Arch Linux (_pacman-contrib_ checkupdates)

Maybe tomorrow
--------------

1. Dmenu extension not used, but there is a default for this in aesthetics
1. Powerline like bar
1. Dynamical layout-based bindings

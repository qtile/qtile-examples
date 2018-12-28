# -*- coding: utf-8 -*-
# A customized config.py for Qtile window manager (http://www.qtile.org)
# Modified by O Simplex
#
# Base config by Derek Taylor
#
# The following comments are the copyright and licensing information from the default config.
# Copyright (c) 2010 Aldo Cortesi, 2010, 2014 dequis, 2012 Randall Ma, 2012-2014 Tycho Andersen,
# 2012 Craig Barnes, 2013 horsik, 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

##### IMPORTS #####

import os
import re
import socket
import subprocess
from libqtile.config import Key, Screen, Group, Match, Drag, Click, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer

##### MOVE WINDOW IN GROUPS #####

def window_to_prev_group():
	@lazy.function
	def __inner(qtile):
		i = qtile.groups.index(qtile.currentGroup)

		if qtile.currentWindow and i != 0:
			group = qtile.groups[i - 1].name
			qtile.currentWindow.togroup(group)
	return __inner

def window_to_next_group():
	@lazy.function
	def __inner(qtile):
		i = qtile.groups.index(qtile.currentGroup)

		if qtile.currentWindow and i != len(qtile.groups):
			group = qtile.groups[i + 1].name
			qtile.currentWindow.togroup(group)
	return __inner

##### KILL ALL WINDOWS #####

def kill_all_windows():
	@lazy.function
	def __inner(qtile):
		for window in qtile.currentGroup.windows:
			window.kill()
	return __inner

def kill_all_windows_except_current():
	@lazy.function
	def __inner(qtile):
		for window in qtile.currentGroup.windows:
			if window != qtile.currentWindow:
				window.kill()
	return __inner

##### MINIMIZE WINDOW #####

def minimize_window():
	@lazy.function
	def __inner(qtile):
		if qtile.currentGroup.name in ["VTB", "RES"]:
			qtile.currentWindow.toggle_minimize()
		else:
			qtile.currentWindow.togroup("M")
	return __inner

##### GENERAL KEYBINDINGS #####

def init_keys():
	return [
		# Fixed Screen
		# Key([mod], "comma",
		# 	lazy.to_screen(2)),							# Keyboard focus screen 3
		# Key([mod], "period",
		# 	lazy.to_screen(0)),							# Keyboard focus screen 1
		# Key([mod], "semicolon",
		# 	lazy.to_screen(1)),							# Keyboard focus screen 2

		# Dinamic screen
		# Key([mod], "Page_Up",
		# 	lazy.next_screen()),						# Switch to another screen
		# Key([mod], "Page_Down",
		# 	lazy.prev_screen()),						# Switch to another screen

		# Misc
		Key([mod, "control"], "Insert",
			lazy.restart()),							# Restart Qtile
		Key([mod, "control"], "Delete",
			lazy.shutdown()),							# Shutdown Qtile

		Key([mod, "shift"], "p", lazy.spawncmd()),		# Launch Qtile prompt

		Key([mod], "b",
			lazy.spawn("light-locker-command -l")),		# Lock screen

		# Rofi Launcher
		Key([mod], "q",
			lazy.spawn("rofi -show")),
		Key([mod, alt], "space",
			lazy.spawn("rofi -show drun")),

		# Window control
		Key([mod], "Home",
			lazy.window.bring_to_front()),				# Bring window to front

		Key([mod], "End",
			minimize_window()),							# Toogle minimize
		Key([mod, "shift"], "End",
			lazy.group["M"].toscreen()),				# Go to minimized windows gruop

		Key([mod], "k", lazy.layout.down()),			# Switch to next window
		Key([mod], "j", lazy.layout.up()),				# Switch to previous window

		Key([mod, "shift"], "k",
			lazy.layout.shuffle_down()),				# Move windows down in current stack
		Key([mod, "shift"], "j",
			lazy.layout.shuffle_up()),					# Move windows up in current stack

		Key([mod, "control"], "k",
			lazy.layout.client_to_next()),				# Move window to previous stack side
		Key([mod, "control"], "j",
			lazy.layout.client_to_previous()),			# Move window to next stack side

		Key([alt], "Tab",
			lazy.group.next_window()),					# Switch focus to other window
		Key([alt, "shift"], "Tab",
			lazy.group.prev_window()),					# Switch focus to other window

		Key([mod], "w",
			lazy.window.kill()),						# Kill active window
		Key([mod, alt], "w",
			lazy.spawn("xkill")),						# Terminate program
		Key([mod, "shift"], "w",
			kill_all_windows_except_current()),			# Kill all windows except current
		Key([mod, "control"], "w",
			kill_all_windows()),						# Kill all windows

		# Layout control
		Key([mod], "space", lazy.layout.next()),		# Move focus to another stack (Stack)

		Key([mod], "backslash",
			lazy.layout.swap_main()),					# Swap current window to main pane

		Key([mod], "l", lazy.layout.grow()),			# Grow size of window (Xmonad)

		Key([mod, "shift"], "l",
			lazy.layout.grow_main()),					# Grow size of main window (Xmonad)

		Key([mod], "h", lazy.layout.shrink()),			# Shrink size of window (Xmonad)

		Key([mod, "shift"], "h",
			lazy.layout.shrink_main()),					# Shrink size of main window (Xmonad)

		Key([mod, "shift"], "n",
			lazy.layout.normalize()),					# Restore all windows to default size ratios

		Key([mod, "shift"], "m",
			lazy.layout.maximize()),					# Toggle a window between min and max sizes

		Key([mod, "shift"], "space",
			lazy.layout.rotate(),						# Swap panes of split stack (Stack)
			lazy.layout.flip()),						# Switch side main pane occupies (Xmonad)

		Key([mod, "shift"], "Return",
			lazy.layout.toggle_split()),				# Toggle between split and unsplit (Stack)

		# Cycle layouts
		Key([mod], "Down", lazy.next_layout()),			# Toggle through layouts
		Key([mod], "Up", lazy.prev_layout()),			# Toggle through layouts

		# Layout related
		Key([mod, "control"], "Return",
			lazy.window.toggle_floating()),				# Toggle floating

		# On group and screen
		Key([mod], "Right", lazy.screen.next_group()),	# Move to right group
		Key([mod], "Left", lazy.screen.prev_group()),	# Move to left group
		Key([mod], "z", lazy.screen.togglegroup()),		# Move to previous visited group

		Key([mod, "shift"], "Right",
			window_to_next_group()),					# Move window to right workspace
		Key([mod, "shift"], "Left",
			window_to_prev_group()),					# Move window to left workspace

		Key([mod, "control"], "Right",
			window_to_next_group(),
			lazy.screen.next_group()),					# Move window to right workspace
		Key([mod, "control"], "Left",
			window_to_prev_group(),
			lazy.screen.prev_group()),					# Move window to left workspace

		Key([mod, "shift"], "i", lazy.next_urgent()),	# Move to next urgent group

		# General

		# Return
		Key([mod], "Return", lazy.spawn(defTerm)),		# Open terminal
		Key([mod, alt], "Return", lazy.spawn(fbkTerm)),	# Open program terminal

		# Function
		Key([mod], "F6",
			lazy.spawn("systemctl start org.cups.cupsd.service")),
		Key([mod], "F7",
			lazy.spawn("systemctl stop org.cups.cupsd.service")),
		Key([mod], "F8",
			lazy.spawn("nmcli radio wifi on")),
		Key([mod], "F9",
			lazy.spawn("nmcli radio wifi off")),
		Key([mod], "F10",
			lazy.spawn("systemctl restart NetworkManager")),

		Key([mod, "control"], "F11",
			lazy.spawn("cmus-remote -u")),
		Key([mod, "control"], "F12",
			lazy.spawn("cmus-remote -s")),
		Key([mod, "shift"], "F11",
			lazy.spawn("cmus-remote -v -5%")),
		Key([mod, "shift"], "F12",
			lazy.spawn("cmus-remote -v +5%")),

		# QWERT
		Key([mod, "shift"], "t", lazy.spawn(pgmTerm + " -e htop")),

		Key([mod], "e", lazy.spawn("subl3")),
		Key([mod], "r", lazy.spawn(pgmTerm + " -e ranger")),
		Key([mod], "t", lazy.spawn("xfce4-taskmanager")),
		Key([mod], "y", lazy.spawn(pgmTerm + " -e mpsyt")),
		Key([mod], "i", lazy.spawn(pgmTerm + " -e irssi")),
		Key([mod], "o", lazy.spawn("libreoffice")),
		Key([mod], "p", lazy.spawn("arandr")),

		# ASDFG
		Key([mod, "shift"], "a", lazy.spawn("chromium")),

		Key([mod], "a", lazy.spawn("firefox-developer-edition")),
		Key([mod], "s", lazy.spawn("pavucontrol")),
		Key([mod], "d", lazy.spawn("xlinks")),
		Key([mod], "f", lazy.spawn("thunar")),
		Key([mod], "g", lazy.spawn("geany")),

		# ZXCVB
		Key([mod], "x", lazy.spawn("pamac-manager")),
		Key([mod], "c", lazy.spawn(pgmTerm + " -e cmus")),
		Key([mod], "v", lazy.spawn("VirtualBox")),
		Key([mod], "n", lazy.spawn("nm-connection-editor")),

		Key([], prnt, lazy.spawn("xfce4-screenshooter"))
	]

##### GROUPS KEYBINDINGS #####

def init_group_keybindings():
	group_keys  = ["dead_grave"]
	group_keys += [str(i) for i in range(1, 10)]
	group_keys += ["0", "minus"]

	for i, group in enumerate(groups):
		# Switch to another group
		keys.append(Key([mod], group_keys[i], lazy.group[group.name].toscreen()))

		# Send current window to another group
		keys.append(Key([mod, "shift"], group_keys[i], lazy.window.togroup(group.name)))

		# Send current window to another group and switch to there
		keys.append(Key([mod, "control"], group_keys[i],
			lazy.window.togroup(group.name),
			lazy.group[group.name].toscreen()))

##### MOUSE #####

def init_mouse():
	return [
		Drag(
			[alt], "Button1", lazy.window.set_position_floating(),		# Move floating windows
			start=lazy.window.get_position()
		),
		Drag(
			[alt], "Button3", lazy.window.set_size_floating(),			# Resize floating windows
			start=lazy.window.get_size()
		),
		Click([mod], "Button1", lazy.window.bring_to_front())			# Bring to front
	]

##### GROUPS #####

def init_groups():
	return [
		Group("SYS",
			layout = "max",
			layouts = [
				layout.Max(**layout_theme),
				layout.MonadWide(**layout_theme),
				layout.MonadTall(**layout_theme)
			]
		),
		Group("CLP",
			layout = "monadtall",
			layouts = [
				layout.MonadTall(**layout_theme),
				layout.MonadWide(ratio = 0.6, **layout_theme)
			],
			matches = [
				Match(title = [
					"irssi",
					"cmus",
					"mpsyt"
				])
			]
		),
		Group("CLS",
			layout = "monadtall",
			layouts = [
				layout.MonadTall(**layout_theme),
				layout.Max(**layout_theme)
			],
			matches = [
				Match(title = ["calcurse"])
			]
		),
		Group("TYP",
			layout = "monadtall",
			layouts = [
				layout.MonadTall(ratio = 0.55, **layout_theme),
				layout.MonadWide(**layout_theme)
			],
			matches = [
				Match(wm_class = [
					"Subl3",
					"Geany"
				])
			]
		),
		Group("DKR",
			layout = "monadwide",
			layouts = [
				layout.MonadWide(**layout_theme),
				layout.MonadTall(**layout_theme)
			]
		),
		Group("VTB",
			layout = "floating",
			layouts = [
				layout.Floating(**layout_theme)
			],
			matches = [
				Match(wm_class = [re.compile("VirtualBox")])
			]
		),
		Group("RES",
			layout = "floating",
			layouts = [
				layout.Floating(**layout_theme)
			],
			matches = [
				Match(wm_class = ["Thunar"])
			]
		),
		Group("DOC",
			layout = "stack",
			layouts = [
				layout.Stack(stacks=2, **layout_theme),
				layout.Max(**layout_theme),
				layout.MonadTall(**layout_theme)
			],
			matches = [
				Match(wm_class = [
					"Zathura",
					"Evince"
				])
			]
		),
		Group("OFC",
			layout = "max",
			layouts = [
				layout.Max(**layout_theme),
				layout.MonadWide(**layout_theme)
			],
			matches = [
				Match(wm_class = ["calibre"]),
				Match(title = [re.compile("LibreOffice")])
			]
		),
		Group("GPX",
			layout = "max",
			layouts = [
				layout.MonadWide(**layout_theme),
				layout.Max(**layout_theme)
			],
			matches = [
				Match(wm_class = [
					"Inkscape",
					"mpv",
					re.compile("Gimp")
				])
			]
		),
		Group("TCM",
			layout = "max",
			layouts = [
				layout.MonadTall(**layout_theme),
				layout.Floating(**layout_theme),
				layout.MonadWide(**layout_theme),
				layout.Max(**layout_theme)
			],
			matches = [
				Match(wm_class = [
					"Firefox Developer Edition",
					"Tor Browser",
					"Chromium",
					"Links"
				])
			]
		),
		Group("M",
			layout = "zoomy",
			layouts = [
				layout.Zoomy(**layout_theme)
			]
		)
	]

##### RULES #####

def init_rules():
	return [
		# Floating types
		Rule(
			Match(wm_type = [
				"confirm", "download", "notification", "toolbar", "splash",
				"dialog", "error", "file_progress", "confirmreset",
				"makebranch", "maketag", "branchdialog", "pinentry",
				"sshaskpass"
			]),
			float = True
		),

		# Floating classes
		Rule(
			Match(wm_class = [
				"Xfce4-taskmanager",
				"Gparted",
				"Nitrogen",
				"Lightdm-gtk-greeter-settings",
				"Nm-connection-editor",
				"Lxappearance",
				"Pavucontrol",
				"Arandr",
				"qt5ct",
				"Thunar",
				"Engrampa",
				"File-roller",
				"Simple-scan",
				re.compile("VirtualBox")
			]),
			float = True,
			break_on_match = False
		)
	]

##### COLORS #####

def init_colors():
	return {
		"black":		["#2B303B", "#2B303B"],
		"grey":			["#40444D", "#424A5B"],
		"white":		["#C0C5CE", "#C0C5CE"],
		"red":			["#BF616A", "#BF616A"],
		"magenta":		["#B48EAD", "#B48EAD"],
		"green":		["#A3BE8C", "#A3BE8C"],
		"darkgreen":	["#859900", "#859900"],
		"blue":			["#8FA1B3", "#8FA1B3"],
		"darkblue":		["#65737E", "#65737E"],
		"orange":		["#EBCB8B", "#EBCB8B"]
	}

##### FONTS #####

def init_fonts():
	return {
		"base": "Ubuntu",
		"bold": "Ubuntu Bold",
		"mono": "Ubuntu Mono"
	}

##### LAYOUTS #####

def init_floating_layout():
	return layout.Floating(
		border_width = 2,
		border_focus = colors["blue"][0],
		border_normal = colors["black"][0]
	)

def init_layout_theme():
	return {
		"margin": 2,
		"border_width": 2,
		"border_focus": colors["blue"][0],
		"border_normal": colors["black"][0],
	}

def init_border_args():
	return {"border_width": 2}

##### WIDGETS #####

def init_widgets_defaults():
	return dict(
		font = fonts["base"],
		fontsize = 10.5,
		padding = 2,
		background = colors["black"],
		foreground = colors["white"]
	)

def init_top_widgets_list():
	return [
		widget.Sep(
			linewidth = 0,
			padding = 3,
		),
		widget.GroupBox(
			font = fonts["bold"],
			fontsize = 9,
			margin_y = 0,
			margin_x = 0,
			# padding_y = 6,
			padding_x = 3,
			borderwidth = 2,
			# hide_unused = True,
			active = colors["white"],
			inactive = "#8E9299",
			urgent_text = colors["white"],
			highlight_method = "line",
			highlight_color = ["2B303B", "14161B"],
			urgent_alert_method = "line",
			rounded = False,
			urgent_border = colors["red"],
			this_current_screen_border = colors["blue"],
			this_screen_border = colors["magenta"],
			other_current_screen_border = colors["magenta"],
			other_screen_border = colors["orange"],
			disable_drag = True,
			use_mouse_wheel = False
		),

		widget.Prompt(
			prompt = "λ : ",
			padding = 10,
			bell_style = "visual",
			foreground = colors["magenta"],
			background = colors["black"]
		),

		widget.Sep(
			linewidth = 0,
			padding = 1,
		),

		widget.WindowName(
			fontsize = 11,
			padding = 0,
			show_state = False,
			foreground = colors["darkgreen"]
		),

		widget.Image(
			scale = True,
			filename = "~/.config/qtile/bar06.png",
			background = colors["red"]
		),

		widget.Image(
			scale = True,
			filename = "~/.config/qtile/bar02-b.png",
			background = colors["red"]
		),
		widget.TextBox(
			fontsize = 14,
			text = " ↯",
			foreground = colors["black"],
			background = colors["red"]
		),
		widget.Net(
			interface = "eth0",
			foreground = colors["black"],
			background = colors["red"]
		),
		widget.Sep(
			linewidth = 0,
			padding = 3,
			background = colors["red"]
		),

		widget.Image(
			scale = True,
			filename = "~/.config/qtile/bar03.png",
			background = colors["magenta"]
		),
		widget.TextBox(
			font = fonts["bold"],
			fontsize = 14,
			text = " ☵",
			foreground = colors["black"],
			background = colors["magenta"]
		),
		widget.CurrentLayout(
			foreground = colors["black"],
			background = colors["magenta"]
		),
		widget.Sep(
			linewidth = 0,
			padding = 3,
			background = colors["magenta"]
		),

		widget.Image(
			scale = True,
			filename = "~/.config/qtile/bar04.png",
			background = colors["green"]
		),
		widget.TextBox(
			font = fonts["bold"],
			fontsize = 14,
			text = " ⛁",
			foreground = colors["black"],
			background = colors["green"]
		),
		widget.Pacman(
			execute = "pamac-manager",
			update_interval = 900,
			foreground = colors["black"],
			unavailable = colors["black"],
			background = colors["green"]
		),
		widget.Sep(
			linewidth = 0,
			padding = 3,
			background = colors["green"]
		),

		widget.Image(
			scale = True,
			filename = "~/.config/qtile/bar05.png",
			background = colors["blue"]
		),
		widget.Systray(
			icon_size = 19,
			background = colors["blue"]
		),
		widget.Sep(
			linewidth = 0,
			padding = 3,
			background = colors["blue"]
		)
	]

def init_bottom_widgets_list():
	return [
		widget.Sep(
			linewidth = 0,
			padding = 3,
		),
		widget.TaskList(
			fontsize = 11,
			margin_x = 0,
			margin_y = 1,
			padding_x = 6,
			padding_y = 2.3,
			borderwidth = 1,
			icon_size = 14,
			spacing = 1,
			# max_title_width = 190,
			title_width_method = 'uniform',
			urgent_alert_method = "text",
			highlight_method = "block",
			txt_minimized = "V ",
			txt_maximized = "",
			txt_floating = "",
			# unfocused_border = "None",
			rounded = True,
			# border = colors["blue"],
		),
		widget.Sep(
			linewidth = 0,
			padding = 3,
		),

		widget.Image(
			scale = True,
			filename = "~/.config/qtile/bar06.png",
			background = colors["red"]
		),
		widget.TextBox(
			fontsize = 14,
			text=" ↯",
			background = colors["grey"]
		),
		widget.ThermalSensor(
			tag_sensor = "CPU",
			threshold = 80,
			update_interval = 1,
			foreground_alert = colors["red"],
			foreground = colors["white"],
			background = colors["grey"]
		),
		widget.Sep(
			linewidth = 0,
			padding = 3,
			background = colors["grey"]
		),

		widget.TextBox(
			font = fonts["bold"],
			fontsize = 14,
			text = "⌬",
			background = colors["grey"]
		),
		widget.Memory(
			fmt = '{MemAvailable}M/{MemTotal}M',
			update_interval = 1,
			background = colors["grey"]
		),
		widget.Sep(
			linewidth = 0,
			padding = 3,
			background = colors["grey"]
		),

		widget.TextBox(
			font = fonts["bold"],
			fontsize = 14,
			text = "🕒",
			background = colors["grey"]
		),
		widget.Clock(
			format = "%a, %b %d - %H:%M",
			background = colors["grey"]
		),
		widget.Sep(
			linewidth = 0,
			padding = 3,
			background = colors["grey"]
		)
	]

##### SCREENS #####

# Top bar widgets
def init_top_screen_widgets():
	return bar.Bar(widgets = init_top_widgets_list(), opacity = 1, size = 21)

# Bottom bar widgets
def init_bottom_screen_widgets():
	return bar.Bar(widgets = init_bottom_widgets_list(), opacity = 1, size = 21)

def init_screens():
	return [
		Screen(
			top = init_top_screen_widgets(),
			bottom = init_bottom_screen_widgets()
		)
		# Screen(
		# 	top = init_top_screen_widgets(),
		# 	bottom = init_bottom_screen_widgets()
		# )
		# Screen(
		# 	top = init_top_screen_widgets(),
		# 	bottom = init_bottom_screen_widgets()
		# )
	]

##### FLOATING CLIENTS #####

@hook.subscribe.client_new
def floating_general(window):
	transient = window.window.get_wm_transient_for()

	if transient is not None:
		if window.window.get_wm_type() in transient:
			window.floating = True

@hook.subscribe.client_new
def libreoffice_dialogues(window):
	if ((window.window.get_wm_class() == ("VCLSalFrame", "libreoffice-calc")) or
	(window.window.get_wm_class() == ("VCLSalFrame", "LibreOffice 3.4"))):
		window.floating = True

@hook.subscribe.client_new
def inkscape_dialogues(window):
	if (window.window.get_name() == "Create new database"):
		window.floating = True

@hook.subscribe.client_new
def inkscape_dialogues(window):
	if (window.window.get_name() == "Sozi"):
		window.floating = True

##### INIT ALL #####

if __name__ in ["config", "__main__"]:
	# Key alias
	mod = "mod4"                                        # Sets mod key to SUPER/WINDOWS
	alt = "mod1"										# Sets alt key to ALT
	altgr = "ISO_Level3_Shift"							# Sets altgr key  to ALTGR
	prnt = "Print"										# Sets prnt key to PrntScr

	# Terminal
	defTerm = "xfce4-terminal --hide-menubar --hide-borders"
	fbkTerm = "tilix --window-style=borderless"
	pgmTerm = "termite"

	colors = init_colors()
	fonts = init_fonts()

	keys = init_keys()
	mouse = init_mouse()
	floating_layout = init_floating_layout()
	layout_theme = init_layout_theme()
	border_args = init_border_args()

	groups = init_groups()
	init_group_keybindings()
	dgroups_app_rules = init_rules()
	screens = init_screens()
	widget_defaults = init_widgets_defaults()

	cursor_warp = False
	bring_front_click = False
	follow_mouse_focus = True

##### STARTUP APPLICATIONS #####

@hook.subscribe.startup_once
def start_once():
	home = os.path.expanduser("~")
	subprocess.call([home + "/.config/qtile/autostart.sh"])

##### RESTART ON SCREEN CHANGE #####

# @hook.subscribe.screen_change
# def restart_on_randr(qtile, ev):
# 	qtile.cmd_restart()

##### NEEDED FOR SOME JAVA APPS #####

wmname = "LG3D"
# wmname = "qtile"
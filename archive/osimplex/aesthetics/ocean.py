from libqtile.layout.floating import Floating

class Colors(object):

	# Ocean
	black =		["#2B303B", "#2B303B"]
	grey =		["#40444D", "#424A5B"]
	lightgrey =	["#8E9299", "#8E9299"]
	white =		["#C0C5CE", "#C0C5CE"]
	red =		["#BF616A", "#BF616A"]
	magenta =	["#B48EAD", "#B48EAD"]
	green =		["#A3BE8C", "#A3BE8C"]
	darkgreen =	["#859900", "#859900"]
	blue =		["#8FA1B3", "#8FA1B3"]
	darkblue =	["#65737E", "#65737E"]
	orange =	["#EBCB8B", "#EBCB8B"]

class Fonts(object):

	base = "Ubuntu Condensed"
	bold = "Ubuntu Condensed Bold"

class Layout_Aesthetics(object):

	layout_theme = {
		"margin":			2,
		"border_width":		2,
		"border_focus":		Colors.blue[0],
		"border_normal":	Colors.black[0],
	}

	floating_layout = Floating(
		border_width = 	2,
		border_focus = 	Colors.blue[0],
		border_normal = Colors.black[0],
	)

class Widget_Aesthetics(object):

	widget_defaults = dict(
		font =			Fonts.base,
		fontsize =		10.5,
		padding =		2,
		foreground =	Colors.white,
		background =	Colors.black
	)

class Extension_Aesthetics(object):

	extension_defaults = dict(
		font =					Fonts.base,
		fontsize =				12,
		dmenu_ignorecase =		True,
		dmenu_prompt =			">",
		selected_foreground =	Colors.blue,
		foreground =			Colors.white,
		selected_background =	Colors.grey,
		background =			Colors.black
	)

# vim: tabstop=4 shiftwidth=4 noexpandtab

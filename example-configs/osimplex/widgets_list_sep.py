# from os.path import expanduser

from libqtile.widget import (
	GroupBox,
	Prompt,
	WindowName,
	TextBox,
	Net,
	CurrentLayout,
	# CurrentLayoutIcon,
	CheckUpdates,
	Systray,
	# CapsNumLockIndicator,
	TaskList,
	# Battery,
	ThermalSensor,
	Memory,
	Clock
)

from widget.battery import Battery
from widgets import Pipe_Widgets as Separator_Widgets
# from widgets import Colon_Widgets as Separator_Widgets
from widgets import Space_Widgets
from aesthetics import Colors, Fonts

class Widgets_List(object):

	color = Colors()
	font = Fonts()

	space = Space_Widgets()
	separator = Separator_Widgets()

	##### WIDGETS LIST #####

	def init_top_single(self, tray = True):

		wl  = []

		wl += [self.space.large_black()]
		wl += [GroupBox(
			font = self.font.bold,
			fontsize = 9,
			margin_y = 0,
			margin_x = 0,
			# padding_y = 6,
			padding_x = 3,
			borderwidth = 2,
			# hide_unused = True,
			active = self.color.white,
			inactive = self.color.lightgrey,
			urgent_text = self.color.white,
			highlight_method = "line",
			highlight_color = ["2B303B", "14161B"],
			urgent_alert_method = "line",
			rounded = False,
			urgent_border = self.color.red,
			this_current_screen_border = self.color.blue,
			other_screen_border = self.color.magenta,
			this_screen_border = self.color.orange,
			other_current_screen_border = self.color.magenta,
			disable_drag = True,
			use_mouse_wheel = False
		)]

		wl += [Prompt(
			prompt = "λ : ",
			padding = 5,
			bell_style = "visual",
			foreground = self.color.magenta,
			background = self.color.black
		)]

		wl += [self.space.large_black()]

		wl += [WindowName(
			fontsize = 11,
			padding = 0,
			show_state = False,
			foreground = self.color.darkgreen
		)]

		wl += [self.space.large_black()]

		wl += [TextBox(
			fontsize = 16,
			text = ""
		)]
		wl += [Net(
			interface = "eth0"
		)]

		wl += [self.separator.bold_white()]
		wl += [TextBox(
			text = ""
		)]
		wl += [ThermalSensor(
			tag_sensor = "CPU",
			threshold = 85,
			update_interval = 1,
			foreground_alert = self.color.red,
			foreground = self.color.white
		)]

		wl += [self.separator.bold_white()]
		wl += [TextBox(
			text = ""
		)]
		wl += [Battery(
			format = "{char} {percent:0.1%}",
			update_interval = 5,
			low_percentage = 0.10,
			unknown_char = "",
			full_char = "",
			charge_char = "+",
			discharge_char = "-",
			empty_char = "",
			low_foreground = self.color.red
		)]

		wl += [self.separator.bold_white()]
		wl += [TextBox(
			font = self.font.bold,
			text = ""
		)]
		wl += [Memory(
			# fmt = "{MemUsed}M/{MemTotal}M - {SwapUsed}M",
			fmt = "{MemUsed}M - {SwapUsed}M",
			update_interval = 1
		)]

		wl += [self.separator.bold_white()]
		wl += [TextBox(
			font = self.font.bold,
			text = ""
		)]
		wl += [CurrentLayout()]

		wl += [self.separator.bold_white()]
		wl += [TextBox(
			font = self.font.bold,
			text = ""
		)]
		wl += [CheckUpdates(
			distro = "Arch_checkupdates",
			display_format = "{updates}",
			update_interval = 900,
			colour_have_updates = self.color.white,
			colour_no_updates = self.color.white
		)]

		if tray:
			wl += [self.separator.bold_white()]
			wl += [Systray(
				padding = 3,
				icon_size = 19
			)]
		# if not tray:
		# 	wl += [self.separator.bold_white()]
		# wl += [CurrentLayoutIcon(
		# 	padding = 0,
		# 	custom_icon_paths = [expanduser("~/.config/qtile/icons")],
		# 	scale = 0.6
		# )]

		wl += [self.separator.bold_white()]
		wl += [TextBox(
			font = self.font.bold,
			text = ""
		)]
		wl += [Clock(
			format = "%a, %b %d - %H:%M"
		)]
		wl += [self.space.large_black()]

		return wl

	def init_top_double(self, tray = True):

		wl  = []

		wl += [self.space.large_black()]
		wl += [GroupBox(
			font = self.font.bold,
			fontsize = 9,
			margin_y = 0,
			margin_x = 0,
			# padding_y = 6,
			padding_x = 3,
			borderwidth = 2,
			# hide_unused = True,
			active = self.color.white,
			inactive = self.color.lightgrey,
			urgent_text = self.color.white,
			highlight_method = "line",
			highlight_color = ["2B303B", "14161B"],
			urgent_alert_method = "line",
			rounded = False,
			urgent_border = self.color.red,
			this_current_screen_border = self.color.blue,
			other_screen_border = self.color.magenta,
			this_screen_border = self.color.orange,
			other_current_screen_border = self.color.magenta,
			disable_drag = True,
			use_mouse_wheel = False
		)]

		wl += [Prompt(
			prompt = "λ : ",
			padding = 5,
			bell_style = "visual",
			foreground = self.color.magenta,
			background = self.color.black
		)]

		wl += [self.space.large_black()]

		wl += [WindowName(
			fontsize = 11,
			padding = 0,
			show_state = False,
			foreground = self.color.darkgreen
		)]

		wl += [self.space.large_black()]

		wl += [TextBox(
			fontsize = 16,
			text = ""
		)]
		wl += [Net(
			interface = "eth0"
		)]

		if tray:
			wl += [self.separator.bold_white()]
			wl += [Systray(
				padding = 3,
				icon_size = 19
			)]
		# if not tray:
		# 	wl += [self.separator.bold_white()]
		# wl += [CurrentLayoutIcon(
		# 	padding = 0,
		# 	custom_icon_paths = [expanduser("~/.config/qtile/icons")],
		# 	scale = 0.6
		# )]
		wl += [self.space.large_black()]

		return wl

	def init_bottom_double(self):

		wl  = []

		wl += [self.space.large_black()]
		wl += [TaskList(
			fontsize = 11,
			margin_x = 0,
			margin_y = 1,
			padding_x = 3,
			padding_y = 2.3,
			borderwidth = 1,
			# icon_size = 14,
			icon_size = 0,
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
			border = self.color.grey
		)]
		wl += [self.space.large_black()]

		wl += [TextBox(
			text = ""
		)]
		wl += [ThermalSensor(
			tag_sensor = "CPU",
			threshold = 85,
			update_interval = 1,
			foreground_alert = self.color.red,
			foreground = self.color.white
		)]

		wl += [self.separator.bold_white()]
		wl += [TextBox(
			text = ""
		)]
		wl += [Battery(
			format = "{char} {percent:0.1%}",
			update_interval = 5,
			low_percentage = 0.10,
			unknown_char = "",
			full_char = "",
			charge_char = "+",
			discharge_char = "-",
			empty_char = "",
			low_foreground = self.color.red
		)]

		wl += [self.separator.bold_white()]
		wl += [TextBox(
			font = self.font.bold,
			text = ""
		)]
		wl += [Memory(
			# fmt = "{MemUsed}M/{MemTotal}M - {SwapUsed}M",
			fmt = "{MemUsed}M - {SwapUsed}M",
			update_interval = 1
		)]

		wl += [self.separator.bold_white()]
		wl += [TextBox(
			font = self.font.bold,
			text = ""
		)]
		wl += [CurrentLayout()]

		wl += [self.separator.bold_white()]
		wl += [TextBox(
			font = self.font.bold,
			text = ""
		)]
		wl += [CheckUpdates(
			distro = "Arch_checkupdates",
			display_format = "{updates}",
			update_interval = 900,
			colour_have_updates = self.color.white,
			colour_no_updates = self.color.white
		)]

		wl += [self.separator.bold_white()]
		wl += [TextBox(
			font = self.font.bold,
			text = ""
		)]
		wl += [Clock(
			format = "%a, %b %d - %H:%M"
		)]
		wl += [self.space.large_black()]

		return wl

# vim: tabstop=4 shiftwidth=4 noexpandtab

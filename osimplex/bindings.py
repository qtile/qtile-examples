from libqtile.config import Key, Drag, Click
from libqtile.command import lazy

from functions import Function

class Keys(object):

	##### GENERAL KEYBINDINGS #####

	def init_keys(self):

		# Key alias
		mod =	"mod4"
		alt =	"mod1"
		altgr =	"mod5"

		return [
			# On root

			Key([mod, altgr], "Insert",
				lazy.restart()),							# Restart Qtile
			Key([mod, altgr], "Delete",
				lazy.shutdown()),							# Shutdown Qtile

			Key([mod, altgr], "p", lazy.spawncmd()),		# Launch Qtile prompt

			# On window

			Key([mod], "Home",
				lazy.window.bring_to_front()),				# Bring window to front

			Key([mod], "End",
				lazy.group[""].toscreen()),					# Go to minimized windows gruop
			Key([mod, "shift"], "End",
				lazy.window.togroup("")),					# Move to minimized windows group
			Key([mod, "control"], "End",
				lazy.window.togroup(""),
				lazy.group[""].toscreen()),					# Move with to minimized windows group
			# Key([mod, alt], "End",
			# 	lazy.window.toggle_minimize()),				# Toogle minimize

			Key([mod], "j", lazy.layout.down()),			# Switch to next window
			Key([mod], "k", lazy.layout.up()),				# Switch to previous window

			Key([mod, "shift"], "j",
				lazy.layout.shuffle_down()),				# Move windows down in current stack
			Key([mod, "shift"], "k",
				lazy.layout.shuffle_up()),					# Move windows up in current stack

			Key([mod, "control"], "j",
				lazy.layout.client_to_previous()),			# Move window to previous stack side
			Key([mod, "control"], "k",
				lazy.layout.client_to_next()),				# Move window to next stack side

			Key([alt], "Tab",
				lazy.group.next_window()),					# Switch focus to other window
			Key([alt, "shift"], "Tab",
				lazy.group.prev_window()),					# Switch focus to other window

			Key([mod, altgr], "Tab",
				lazy.group.next_window(),
				lazy.window.bring_to_front()),				# Switch focus to other window + front
			Key([mod, altgr, "shift"], "Tab",
				lazy.group.prev_window(),
				lazy.window.bring_to_front()),				# Switch focus to other window + front

			Key([mod], "w",
				lazy.window.kill()),						# Kill active window
			Key([mod, alt], "w",
				lazy.spawn("xkill")),						# Terminate program
			Key([mod, "shift"], "w",
				Function.kill_all_windows_minus_current()),	# Kill all windows except current
			Key([mod, "control"], "w",
				Function.kill_all_windows()),				# Kill all windows

			Key([mod, "control"], "Return",
				lazy.window.toggle_floating()),				# Toggle floating

			# On layout

			Key([mod], "backslash",
				lazy.layout.swap_main()),					# Swap current window to main pane (Xmonad)

			Key([mod], "m",
				lazy.layout.next()),						# Move focus to another stack (Stack)

			Key([mod], "h", lazy.layout.shrink()),			# Shrink size of window (Xmonad)
			Key([mod], "l", lazy.layout.grow()),			# Grow size of window (Xmonad)

			Key([mod, "shift"], "h",
				# lazy.layout.decrease_nmaster(),			# Decrease number in master pane (Tile)
				lazy.layout.shrink_main()),					# Shrink size of main window (Xmonad)
			Key([mod, "shift"], "l",
				# lazy.layout.increase_nmaster(),			# Increase number in master pane (Tile)
				lazy.layout.grow_main()),					# Grow size of main window (Xmonad)

			Key([mod, "shift"], "n",
				lazy.layout.normalize()),					# Restore all windows to default size ratios
			Key([mod, "shift"], "m",
				lazy.layout.maximize()),					# Toggle a window between min and max sizes

			Key([mod, "shift"], "space",
				lazy.layout.rotate(),						# Swap panes of split stack (Stack)
				lazy.layout.flip()),						# Switch side main pane occupies (Xmonad)

			Key([mod, "shift"], "Return",
				lazy.layout.toggle_split()),				# Toggle between split and unsplit (Stack)

			Key([mod], "Up", lazy.prev_layout()),			# Toggle through layouts
			Key([mod], "Down", lazy.next_layout()),			# Toggle through layouts

			# On group

			Key([mod], "z",
				lazy.screen.togglegroup()),					# Move to previous visited group
			Key([mod, "shift"], "i",
				lazy.next_urgent()),						# Move to next urgent group

			Key([mod], "Left",
				lazy.screen.prev_group()),					# Move to previous group
			Key([mod], "Right",
				lazy.screen.next_group()),					# Move to next group

			Key([mod, "shift"], "Left",
				Function.window_to_prev_group()),			# Move window to previous group
			Key([mod, "shift"], "Right",
				Function.window_to_next_group()),			# Move window to next group

			Key([mod, "control"], "Left",
				Function.window_to_prev_group(),
				lazy.screen.prev_group()),					# Move with window to previous group
			Key([mod, "control"], "Right",
				Function.window_to_next_group(),
				lazy.screen.next_group()),					# Move with window to next group

			# On screen

			Key([mod], "Page_Up",
				lazy.prev_screen()),						# Switch to previous screen
			Key([mod], "Page_Down",
				lazy.next_screen()),						# Switch to next screen

			Key([mod, "shift"], "Page_Up",
				Function.window_to_prev_screen()),			# Move window to previous screen
			Key([mod, "shift"], "Page_Down",
				Function.window_to_next_screen()),			# Move window to next screen

			Key([mod, "control"], "Page_Up",
				Function.swap_prev_screen()),				# Swap active groups on screens
			Key([mod, "control"], "Page_Down",
				Function.swap_next_screen()),				# Swap active groups on screens

			# On bar

			Key([mod, alt], "slash",
				lazy.hide_show_bar("all")),					# Toggle all screen bars
			# Key([mod, "shift"], "slash",
			# 	lazy.hide_show_bar("top")),					# Toggle top screen bar
			# Key([mod, "control"], "slash",
			# 	lazy.hide_show_bar("bottom"))				# Toggle bottom screen bar
		]

	##### GROUPS KEYBINDINGS #####

	def init_group_keybindings(self, groups):

		# Key alias
		mod =	"mod4"
		alt =	"mod1"
		altgr =	"mod5"

		group_keys  = []
		group_keys += [str(i) for i in range(1, 10)]
		group_keys += ["0", "minus", "equal"]

		keys = []

		# For all, less the group for "minimized" windows
		for i, group in enumerate(groups[0:-1]):
			# Switch to another group
			keys.append(Key([mod], group_keys[i], lazy.group[group.name].toscreen()))

			# Move current window to another group
			keys.append(Key([mod, "shift"], group_keys[i], lazy.window.togroup(group.name)))

			# Move with current window to another group
			keys.append(Key([mod, "control"], group_keys[i],
				lazy.window.togroup(group.name),
				lazy.group[group.name].toscreen()))

		return keys

class Mouses(object):

	##### MOUSE #####

	def init_mouse(self):

		# Key alias
		mod =	"mod4"
		alt =	"mod1"
		altgr =	"mod5"

		return [
			# Move floating windows
			Drag(
				[mod], "Button1", lazy.window.set_position_floating(),
				start = lazy.window.get_position()
			),

			# Resize floating windows
			Drag(
				[mod], "Button3", lazy.window.set_size_floating(),
				start = lazy.window.get_size()
			),

			# Bring to front
			Click([mod, alt], "Button1", lazy.window.bring_to_front())
		]

# vim: tabstop=4 shiftwidth=4 noexpandtab

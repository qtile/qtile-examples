# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2015 M. Dietrich
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget

mod = "mod4"

keys = [
	# Switch between windows in current stack pane
	Key([mod, "control"], "Tab", lazy.layout.down()),
	Key([mod, "control", "shift"], "Tab", lazy.layout.up()),

	# Move windows up or down in current stack
	Key([mod, "mod1"], "Tab", lazy.layout.shuffle_down()),
	Key([mod, "mod1", "shift"], "Tab", lazy.layout.shuffle_up()),

	# Switch window focus to other pane(s) of stack
	Key([mod], "Tab", lazy.layout.next()),
	Key([mod, "shift"], "Tab", lazy.layout.prev()),

	# Swap panes of split stack
	#Key([mod, "shift"], "space", lazy.layout.rotate()),

	Key([mod], "k", lazy.layout.increase_ratio()),
	Key([mod], "j", lazy.layout.decrease_ratio()),

	# Toggle between split and unsplit sides of stack.
	# Split = all windows displayed
	# Unsplit = 1 window displayed, like Max layout, but still with
	# multiple stack panes
	#Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
	Key([mod], "Return", lazy.spawn("x-terminal-emulator")),
	Key([mod], "v", lazy.spawn("gvim")),
	Key([mod], "l", lazy.spawn("xlock")),
	Key([], "XF86Launch1", lazy.spawn("xlock")),
	Key([], "XF86AudioMute", lazy.spawn("amixer -D pulse set Master toggle")),
	#Key([], "XF86AudioMicMute", lazy.spawn("amixer -D pulse set Master toggle")),
	Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
	Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
	Key([], "XF86Back", lazy.screen.prev_group()),
	Key([], "XF86Forward", lazy.screen.next_group()),
	Key([mod], "XF86Back", lazy.screen.prev_group()),
	Key([mod], "XF86Forward", lazy.screen.next_group()),
	Key([mod], "Left", lazy.screen.prev_group()),
	Key([mod], "Right", lazy.screen.next_group()),
	Key([mod], "Escape", lazy.screen.togglegroup()),

	# Toggle between different layouts as defined below
	Key([mod], "space", lazy.next_layout()),
	Key([mod, 'shift'], "space", lazy.prev_layout()),
	# lazy.group.setlayout('...
	Key([mod, "shift"], "c", lazy.window.kill()),

	Key([mod, "shift"], "r", lazy.restart()),
	Key([mod, "shift"], "q", lazy.shutdown()),
	Key([mod], "r", lazy.spawncmd()),
	Key([mod], "f", lazy.window.toggle_floating()),
	Key([mod], "m", lazy.window.toggle_fullscreen()),
	]

groups = [Group(i) for i in "1234567890"]

for i in groups:
	# mod1 + letter of group = switch to group
	keys.append(
		Key([mod], i.name, lazy.group[i.name].toscreen())
	)

	# mod1 + shift + letter of group = switch to & move focused window to group
	keys.append(
		Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
	)

layouts = [
	layout.Max(),
	layout.Floating(),
	#layout.Matrix(),
	#layout.MonadTall(),
	#layout.RatioTile(),
	#layout.Slice(),
	#layout.Stack(num_stacks=2),
	layout.Tile(),
	#layout.TreeTab(),
	#layout.VerticalTile(),
	#layout.Zoomy(),
	]

widget_defaults = dict(
	font='Nimbus Sans L',
	fontsize=16,
	padding=3,
	)

screens = [
	Screen(
		top=bar.Bar(
			[
				widget.GroupBox(disable_drag=True, this_current_screen_border='808080', this_screen_border='808080', ),
				widget.Prompt(),
				widget.TaskList(font='Nimbus Sans L', border='404040', highlight_method='block', ),
				#widget.WindowName(),
				#widget.WindowTabs(),
				#widget.TextBox("default config", name="default"),
				widget.Systray(),
				widget.Backlight(),
				#widget.BatteryIcon(),
				widget.Battery(),
				widget.CurrentLayout(),
				#widget.ThermalSensor(),
				widget.Volume(),
				widget.Clock(format='%Y-%m-%d %I:%M %p'),
				],
			32,
			),
		),
	Screen(
		top=bar.Bar(
			[
				widget.GroupBox(disable_drag=True, this_current_screen_border='808080', this_screen_border='808080', ),
				widget.WindowName(),
				],
			28,
			),
		),
	]

# Drag floating layouts.
mouse = [
	Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
	Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
	Click([mod], "Button2", lazy.window.bring_to_front())
	]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

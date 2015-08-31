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
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, hook, bar, widget

mod = 'mod4'
color_alert = '#ee9900'
color_frame = '#808080'

# see http://docs.qtile.org/en/latest/manual/config/keys.html
keys = [
	# Switch between windows in current stack pane
	Key([mod, 'control'], 'Tab', lazy.layout.down()),
	Key([mod, 'control', 'shift'], 'Tab', lazy.layout.up()),

	# Move windows up or down in current stack
	Key([mod, 'mod1'], 'Tab', lazy.layout.shuffle_down()),
	Key([mod, 'mod1', 'shift'], 'Tab', lazy.layout.shuffle_up()),

	# Switch window focus to other pane(s) of stack
	Key([mod], 'Tab', lazy.layout.next()),
	Key([mod, 'shift'], 'Tab', lazy.layout.prev()),

	# Swap panes of split stack
	#Key([mod, 'shift'], 'space', lazy.layout.rotate()),

	Key([mod], 'k', lazy.layout.increase_ratio()),
	Key([mod], 'j', lazy.layout.decrease_ratio()),

	# Toggle between split and unsplit sides of stack.
	# Split = all windows displayed
	# Unsplit = 1 window displayed, like Max layout, but still with
	# multiple stack panes
	#Key([mod, 'shift'], 'Return', lazy.layout.toggle_split()),
	Key([mod], 'Return', lazy.spawn('x-terminal-emulator')),
	Key([mod], 'v', lazy.spawn('gvim')),
	Key([mod], 'l', lazy.spawn('xlock')),
	Key([], 'XF86Launch1', lazy.spawn('xlock')),
	Key([], 'XF86AudioMute', lazy.spawn('amixer -D pulse set Master toggle')),
	#Key([], 'XF86AudioMicMute', lazy.spawn('amixer -D pulse set Master toggle')),
	Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -c 0 -q set Master 2dB+')),
	Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -c 0 -q set Master 2dB-')),
	Key([], 'XF86Back', lazy.screen.prev_group(skip_managed=True, )),
	Key([], 'XF86Forward', lazy.screen.next_group(skip_managed=True, )),
	Key([mod], 'XF86Back', lazy.screen.prev_group(skip_managed=True, )),
	Key([mod], 'XF86Forward', lazy.screen.next_group(skip_managed=True, )),
	Key([mod], 'Left', lazy.screen.prev_group(skip_managed=True, )),
	Key([mod], 'Right', lazy.screen.next_group(skip_managed=True, )),
	Key([mod], 'Escape', lazy.screen.togglegroup()),

	# Toggle between different layouts as defined below
	Key([mod], 'space', lazy.next_layout()),
	Key([mod, 'shift'], 'space', lazy.prev_layout()),
	# lazy.group.setlayout('...
	Key([mod, 'shift'], 'c', lazy.window.kill()),

	Key([mod, 'shift'], 'r', lazy.restart()),
	Key([mod, 'shift'], 'q', lazy.shutdown()),
	Key([mod], 'r', lazy.spawncmd()),
	Key([mod], 'f', lazy.window.toggle_floating()),
	Key([mod], 'm', lazy.window.toggle_fullscreen()),

	#Key( [mod, 'shift'], '2', lazy.to_screen(1), lazy.group.toscreen(1)),
	]

groups = [Group(i) for i in '1234567890']

for i in groups:
	# mod1 + letter of group = switch to group
	keys.append(
		Key([mod], i.name, lazy.group[i.name].toscreen())
	)

	# mod1 + shift + letter of group = switch to & move focused window to group
	keys.append(
		Key([mod, 'shift'], i.name, lazy.window.togroup(i.name))
	)

try:
	# ugly hack to make my colors default:
	layout.Floating.defaults[0] = ("border_focus", color_alert, "Border colour for the focused window.")
	layout.Floating.defaults[1] = ("border_normal", color_frame, "Border colour for un-focused winows.")
except:
	pass

# see http://docs.qtile.org/en/latest/manual/ref/layouts.html
layouts = [
	layout.Max(),
	layout.Floating(border_focus=color_alert, border_normal=color_frame, ),
	#layout.Matrix(),
	#layout.MonadTall(),
	#layout.RatioTile(),
	#layout.Slice(),
	#layout.Stack(num_stacks=2),
	layout.Tile(border_focus=color_alert, border_normal=color_frame, ),
	#layout.TreeTab(),
	#layout.VerticalTile(),
	#layout.Zoomy(),
	]

widget_defaults = dict(
	font='Nimbus Sans L',
	fontsize=16,
	padding=3,
	)

# see http://docs.qtile.org/en/latest/manual/ref/widgets.html
# TODO how to detect if 1 or 2 are needed?
screens = [Screen(top=bar.Bar([
	widget.GroupBox(disable_drag=True, this_current_screen_border=color_frame, this_screen_border=color_frame, urgent_text=color_alert, ),
	widget.Prompt(),
	widget.TaskList(font='Nimbus Sans L', border=color_frame, highlight_method='block', ),
	#widget.WindowName(),
	#widget.WindowTabs(),
	#widget.TextBox('default config', name='default'),
	widget.Systray(),
	widget.Backlight(),
	#widget.BatteryIcon(),
	widget.Battery(
		charge_char = u'↑',
		discharge_char = u'↓',
		),
	widget.CurrentLayout(),
	widget.ThermalSensor(),
	widget.Volume(),
	widget.Clock(format='%Y-%m-%d %H:%M %p'),
	], 32, ), ), ]

def detect_screens(qtile):
	while len(screens) < len(qtile.conn.pseudoscreens):
		screens.append(Screen(
		top=bar.Bar([
			widget.GroupBox(disable_drag=True, this_current_screen_border=color_frame, this_screen_border=color_frame, ),
			widget.WindowName(),
			], 28, ), ))

# Drag floating layouts.
mouse = [
	Drag([mod], 'Button1', lazy.window.set_position_floating(), start=lazy.window.get_position()),
	Drag([mod], 'Button3', lazy.window.set_size_floating(), start=lazy.window.get_size()),
	Click([mod], 'Button2', lazy.window.bring_to_front())
	]

# subscribe for change of screen setup, just restart if called
@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
	# TODO only if numbers of screens changed
	qtile.cmd_restart()

def __x():
	import pyudev
	context = pyudev.Context()
	monitor = pyudev.Monitor.from_netlink(context)
	monitor.filter_by('drm')
	monitor.enable_receiving()
	observer = pyudev.MonitorObserver(monitor, setup_monitors)
	observer.start()

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
	dict(role='buddy_list', ),
	])
auto_fullscreen = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = 'LG3D'

def main(qtile):
	detect_screens(qtile)

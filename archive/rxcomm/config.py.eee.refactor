from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.dgroups import simple_key_binder

import platform
import sys

# TODO:
#  2. multi screen switching
#  3. better hotkeys for dgroups?

# Global mod key. I have mod3 bound to caps lock, it's great.
mod = "mod3"

# If we're running in debug mode, it's for development. Make sure the
# hotkeys don't clash, only start one window, etc.
if '-d' in sys.argv:
    hostname = 'xephyr'
    mod = "mod3"

# global font options
widget_defaults = dict(
    font = 'Anonymous Pro',
    fontsize = 18,
    padding = 3,
)

# 1 screen
screens = [Screen(top = bar.Bar([
    widget.GroupBox(urgent_alert_method='text'),
    widget.Prompt(),
#   widget.WindowName(**widget_defaults),
    widget.Spacer(),
    widget.TextBox(text="C"),
    widget.CPUGraph(samples=300, width=100),
    widget.TextBox(text="D"),
    widget.NetGraph(samples=300, width=100, interface="wlan2"),
    widget.TextBox(text="U"),
    widget.NetGraph(samples=300, width=100, interface="wlan2", bandwidth_type="up"),
    widget.Notify(foreground="FF0000", fontsize=14, font="Anonymous Pro"),
#   widget.Volume(**widget_defaults),
    widget.Sep(foreground="000000"),
    # 1 screen means this is a laptop, so let's render the battery
    widget.Battery(energy_now_file='charge_now',
	energy_full_file='charge_full',
	power_now_file='current_now',
    ),
    widget.Systray(),
    widget.Clock('%a %m/%d %I:%M'),
],30,),),
]


def app_or_group(group, app):
    """ Go to specified group if it exists. Otherwise, run the specified app.
    When used in conjunction with dgroups to auto-assign apps to specific
    groups, this can be used as a way to go to an app if it is already
    running. """
    def f(qtile):
        try:
            qtile.groupMap[group].cmd_toscreen()
        except KeyError:
            qtile.cmd_spawn(app)
    return f

keys = [
    # Log out; note that this doesn't use mod3: that's intentional in case mod3
    # gets hosed (which happens if you unplug and replug your usb keyboard
    # sometimes, or on ubuntu upgrades). This way you can still log back out
    # and in gracefully.
    Key(["shift", "mod1"], "q",  lazy.shutdown()),

    Key([mod], "k",              lazy.layout.down()),
    Key([mod], "j",              lazy.layout.up()),
    Key([mod], "h",              lazy.layout.previous()),
    Key([mod], "l",              lazy.layout.previous()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod, "shift"], "Return",lazy.layout.toggle_split()),
    Key(["mod1"], "Tab",         lazy.nextlayout()),
    Key([mod, "mod1"], "h",      lazy.to_screen(0)),
    Key([mod, "mod1"], "l",      lazy.to_screen(1)),
    Key([mod], "x",              lazy.window.kill()),

    # interact with prompts
    Key([mod], "r",              lazy.spawncmd()),
    Key([mod], "g",              lazy.switchgroup()),

    # Control the notify widget
    Key([mod], "y",              lazy.widget['notify'].toggle()),
    Key([mod, "mod1"], "y",         lazy.widget['notify'].prev()),
    Key([mod, "mod1"], "u",         lazy.widget['notify'].next()),


    # start specific apps
    Key([mod], "n",              lazy.function(app_or_group("www", "firefox"))),
    Key([mod], "t",              lazy.function(app_or_group("music", "clementine"))),
    Key([mod], "c",              lazy.function(app_or_group("io", "pidgin"))),
    Key([mod], "Return",         lazy.spawn("urxvt -rv +sb -fn 'xft:Anonymous Pro:pixelsize=18'")),
    Key([mod], "z",              lazy.function(app_or_group("aam", "/home/k0rx/Applications/aamf.sh"))),
    Key([mod], "v",              lazy.function(app_or_group("nx", "/usr/NX/bin/nxclient -name NXClient"))),
    Key([mod], "m",              lazy.function(app_or_group('mail', 'urxvt -rv +sb -fn "xft:Anonymous Pro:pixelsize=18" -e /usr/bin/mutt'))),

    # Change the volume if our keyboard has keys
    Key(
        [], "XF86AudioRaiseVolume",
        lazy.spawn("amixer -c 0 -q set Master 2dB+")
    ),
    Key(
        [], "XF86AudioLowerVolume",
        lazy.spawn("amixer -c 0 -q set Master 2dB-")
    ),
    Key(
        [], "XF86AudioMute",
        lazy.spawn("amixer -c 0 -q set Master toggle")
    ),
    Key(
        [], "XF86AudioPlay",
        lazy.spawn("clementine --play-pause")
    ),
    Key(
        [], "XF86AudioNext",
        lazy.spawn("clementine --next")
    ),
    Key(
        [], "XF86AudioPrev",
        lazy.spawn("clementine --prev")
    ),

    # also allow changing volume the old fashioned way
    Key([mod], "equal", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([mod], "minus", lazy.spawn("amixer -c 0 -q set Master 2dB-")),

    # allow play pause as well
    Key([mod], "p",     lazy.spawn("vif.py play_pause")),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groups = []

# throwaway groups for random stuff
for i in ['a', 's', 'd', 'f']:
    if i == 'a':
        groups.append(Group(i, spawn='urxvt -rv +sb -fn "xft:Anonymous Pro:pixelsize=18"'))
    else:
        groups.append(Group(i))
    keys.append(
        Key([mod], i, lazy.group[i].toscreen())
    )
    keys.append(
        Key([mod, "mod1"], i, lazy.window.togroup(i))
    )

# groups with special jobs. I usually navigate to these via my app_or_group
# function.
groups.extend([
    Group('music', layout='max', persist=False, init=False,
          matches=[Match(wm_class=['Clementine', 'Viridian'])]),
    Group('www', spawn='firefox', layout='max', persist=False,
          matches=[Match(wm_class=['Firefox', 'TorBrowser', 'google-chrome', 'Google-chrome'])]),
    Group('io', layout='pidgin', persist=False, init=False,
          matches=[Match(wm_class=['Pidgin'], role=['Buddy List'])]),
    Group('nx', persist=False, layout='max', init=False,
          matches=[Match(wm_class=['NXClient'])]),
    Group('mail', persist=False, layout='max',
          spawn='urxvt -rv +sb -fn "xft:Anonymous Pro:pixelsize=18" -e /usr/bin/mutt',
          matches=[Match(title=['mutt'])]),
    Group('aam', persist=False, layout='stack', init=False,
          matches=[Match(wm_class=['AAMClient'])]),
    Group('socks', persist=False, layout='max', init=False,
          matches=[Match(wm_class=['socks'])]),
])

border_args = dict(
    border_width=1,
)

layouts = [
    layout.Max(),
    layout.Stack(stacks=2, **border_args),

    # a layout just for gimp
    layout.Slice('left', 192, name='gimp', role='gimp-toolbox',
         fallback=layout.Slice('right', 256, role='gimp-dock',
         fallback=layout.Stack(stacks=1, **border_args))),

    # a layout for pidgin
    layout.Slice('right', 256, name='pidgin', role='buddy_list',
         fallback=layout.Stack(stacks=1, **border_args)),
]

# Automatically float these types. This overrides the default behavior (which
# is to also float utility types), but the default behavior breaks our fancy
# gimp slice layout specified later on.
floating_layout = layout.Floating(auto_float_types=[
  "notification",
  "toolbar",
  "splash",
  "dialog",
])

# vim: tabstop=4 shiftwidth=4 expandtab

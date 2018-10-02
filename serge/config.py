# -*- coding: utf-8 -*-
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.dgroups import simple_key_binder

from libqtile.log_utils import logger

import platform
import os
import sys

from libqtile.widget import base

def winstash(qtile):
    w = qtile.currentWindow
    if w is None:
        return
    w.togroup("X")

def winunstash(qtile):
    g = qtile.currentGroup
    for w in qtile.groupMap["X"].windows:
        w.togroup(g.name)

class MyBright(base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(self, update_interval=10)

    def poll(self):
        dirname = "/sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-LVDS-1/intel_backlight"
        curf = "{0}/brightness".format(dirname)
        maxf = "{0}/max_brightness".format(dirname)
        with open(curf) as f:
            cur = int(f.read().strip())
        with open(maxf) as f:
            maxb = int(f.read().strip())
        pcnt = int(cur * 100 / maxb)
        txtb = "Bright: {0}%".format(pcnt)
        return "{0} | ".format(txtb)

class MyBatt(base.InLoopPollText):

    def __init__(self):
        base.InLoopPollText.__init__(self, update_interval=10)

    def poll(self):
        dirname = "/sys/bus/acpi/drivers/battery/PNP0C0A:00/power_supply/BAT1"
        nowf = "{0}/energy_now".format(dirname)
        fullf = "{0}/energy_full".format(dirname)
        statusf = "{0}/status".format(dirname)
        with open(statusf) as f:
            status = f.read().strip()[0:3]
        if status[0] == 'C':
            charge_char = '▲'
        elif status[0] == 'D':
            charge_char = '▼'
        else:
            charge_char = status[0:3]
        with open(nowf) as f:
            now = int(f.read().strip())
        with open(fullf) as f:
            full = int(f.read().strip())
        pcnt = int(now * 100 / full)
        if pcnt < 45:
            self.background = "#ff0000"
        elif pcnt > 80:
            self.background = "#00ff00"
        txta = "Batt: {0} {1}%".format(charge_char, pcnt)
        return "{0} |".format(txta)

hostname = platform.node()
sound_card = 0

mod = "mod4"

GREY = "#444444"
DARK_GREY = "#333333"
BLUE = "#007fcf"
DARK_BLUE = "#005083"
ORANGE = "#dd6600"
DARK_ORANGE = "#582c00"

# global font options
widget_defaults = dict(
    font = 'Consolas',
    fontsize = 14,
    padding = 3,
    foreground = "#000000",
    background = "#ffffff",
)

screens = [Screen(top = bar.Bar([
    widget.GroupBox(urgent_alert_method='text',
        disable_drag=True,
        active = "#00226f",
        inactive = "#bbbbbb",
        hilight_color = "#4488ff",
        this_screen_border = ORANGE,
        other_current_screen_border = ORANGE,
        other_screen_border = "#444444",
        urgent_screen_border = "#ff4444",
        hilight_method="block",
        **widget_defaults),
    widget.Prompt(**widget_defaults),
    widget.Clipboard(timeout=None, width=bar.STRETCH, max_width=None),
    MyBatt(),
    MyBright(),
    widget.Systray(**widget_defaults),
    widget.Clock(format='%Y-%m-%d %a %I:%M %p', **widget_defaults),
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
    Key([mod], "i", lazy.function(winstash)),
    Key([mod, "shift"], "i", lazy.function(winunstash)),
    # Log out; note that this doesn't use mod3: that's intentional in case mod3
    # gets hosed (which happens if you unplug and replug your usb keyboard
    # sometimes, or on ubuntu upgrades). This way you can still log back out
    # and in gracefully.
    Key(["shift", "mod1"], "q",  lazy.shutdown()),

    # I don't ever use floating, but sometimes it is handy to toggle to
    # floating for debugging, so I use the "out of band" mnemonic for this as
    # well.
    Key(["shift", "mod1"], "f",  lazy.window.toggle_floating()),

    Key([mod], "k",              lazy.layout.up()),
    Key([mod], "j",              lazy.layout.down()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod, "shift"], "Return",lazy.layout.toggle_split()),
    Key(["mod1"], "Tab",         lazy.next_layout()),
    Key([mod, "mod1"], "h",      lazy.to_screen(0)),
    Key([mod, "mod1"], "l",      lazy.to_screen(1)),
    Key([mod, "shift"], "l",     lazy.layout.swap_left()),
    # serge
    Key([mod], "h",              lazy.layout.left()),
    Key([mod], "l",              lazy.layout.right()),
    Key([mod], "s",              lazy.layout.toggle_split()),
    Key([mod, "shift", "control"], "l", lazy.layout.grow_right()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift", "control"], "h", lazy.layout.grow_left()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod], "s", lazy.layout.toggle_split()),

    # interact with prompts
    Key([mod], "r",              lazy.spawncmd()),
    Key([mod], "g",              lazy.togroup()),

    # start specific apps
    Key([mod], "n",              lazy.function(app_or_group("www", "firefox"))),
    Key([mod], "m",              lazy.function(app_or_group("music", "clementine"))),
    Key([mod, "shift"], "x",     lazy.window.kill()),
    Key([mod, "control"], "Return", lazy.spawn("tabbed vimprobable -e")),
    Key([mod], "Return",         lazy.spawn("st")),

    # Change the volume if our keyboard has keys
    Key(
        [], "XF86AudioRaiseVolume",
        lazy.spawn("amixer -c %d -q set Master 2dB+" % sound_card)
    ),
    Key(
        [], "XF86AudioLowerVolume",
        lazy.spawn("amixer -c %d -q set Master 2dB-" % sound_card)
    ),
    Key(
        [], "XF86AudioMute",
        lazy.spawn("amixer -D pulse set Master toggle")
    ),

    # also allow changing volume, tracks the old fashioned way
    Key([mod], "equal", lazy.spawn("amixer -c %d -q set Master 2dB+" % sound_card)),
    Key([mod], "minus", lazy.spawn("amixer -c %d -q set Master 2dB-" % sound_card)),

    # poor man's middle click
    Key([mod], "v",     lazy.spawn("xdotool click 2")),

    # backlight controls
    Key([], "XF86KbdBrightnessUp", lazy.spawn("maclight keyboard up")),
    Key([], "XF86KbdBrightnessDown", lazy.spawn("maclight keyboard down")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("maclight screen up")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("maclight screen down")),
]

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groups = []

# throwaway groups for random stuff
for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
    groups.append(Group(i))
    keys.append(
        Key([mod], i, lazy.group[i].toscreen())
    )
    keys.append(
        Key([mod, "shift"], i, lazy.window.togroup(i))
    )

groups.append(Group("X"))

# groups with special jobs. I usually navigate to these via my app_or_group
# function.
groups.extend([
    Group('music', spawn='clementine', layout='max', persist=False,
          matches=[Match(wm_class=['Clementine', 'Viridian'])]),
    Group('www', spawn='google-chrome', layout='max', persist=False,
          matches=[Match(wm_class=['Firefox', 'google-chrome', 'Google-chrome'])]),
])

border_args = dict(
    border_width=1,
)

layouts = [
    layout.Wmii(),
    layout.Stack(num_stacks=2, **border_args),
    layout.Max(),

    # a layout just for gimp
    layout.Slice(side='left', width=192, name='gimp', role='gimp-toolbox',
         fallback=layout.Slice(side='right', width=256, role='gimp-dock',
         fallback=layout.Stack(num_stacks=1, **border_args))),

    layout.MonadTall(ratio=0.65, **border_args),
]

no_utility = layout.floating.DEFAULT_FLOAT_WM_TYPES - {'utility'}
floating_layout = layout.Floating(auto_float_types=no_utility)

cursor_warp = True
follow_mouse_focus = True

focus_on_window_activation = "never"
os.system("xmodmap ~/.xmodmaprc")

# vim: tabstop=4 shiftwidth=4 expandtab

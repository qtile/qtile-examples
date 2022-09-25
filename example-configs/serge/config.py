# -*- coding: utf-8 -*-
from libqtile.config import Key, Screen, Group, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget
from libqtile.dgroups import simple_key_binder


#def warp(x, y):
    #qtile.root.warp_pointer(x, y)
#
#Key(..., lazy.function(warp))

from libqtile.log_utils import logger

import platform
import os

from libqtile.widget import base

def winstash(qtile):
    w = qtile.current_window
    if w is None:
        return
    w.togroup("X")

def winunstash(qtile):
    g = qtile.current_group
    for w in qtile.groups_map["X"].windows:
        w.togroup(g.name)

hostname = platform.node()
sound_card = 0

mod = "mod4"

GREY = "#444444"
DARK_GREY = "#333333"
BLUE = "#007fcf"
DARK_BLUE = "#005083"
ORANGE = "#dd6600"
DARK_ORANGE = "#582c00"

class MyCheckinState(base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(self, update_interval=10)

    def poll(self):
        with open("/home/serge/checkinstate") as f:
            cur = f.read().strip()
        return "GTD: " + cur

class MyBright(base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(self, update_interval=10)

    def poll(self):
        if hostname == "honeybadger":
            dirname = "/sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-LVDS-1/intel_backlight"
        else:
            dirname = "/sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-eDP-1/intel_backlight"
        curf = "{0}/brightness".format(dirname)
        maxf = "{0}/max_brightness".format(dirname)
        with open(curf) as f:
            cur = int(f.read().strip())
        with open(maxf) as f:
            maxb = int(f.read().strip())
        pcnt = int(cur * 100 / maxb)
        txtb = "Bright: {0}%".format(pcnt)
        return "{0} | ".format(txtb)


# global font options
if os.path.exists("/home/serge/bright"):
    widget_defaults = dict(
        font = 'Consolas',
        fontsize = 14,
        padding = 3,
        foreground = "#000000",
        background = "#ffffff",
    )
    active = "#00226f"
    inactive = "#bbbbbb"
    hilight_color = "#4488ff"
else:
    widget_defaults = dict(
        font = 'Consolas',
        fontsize = 14,
        padding = 3,
        foreground = ORANGE,
        background = DARK_GREY,
    )
    active = "#666666"
    inactive = DARK_ORANGE
    hilight_color = "#4488ff"

bat0 = widget.Battery(energy_now_file='energy_now',
                    battery_name='BAT0',
                    update_delay=60,
                    energy_full_file='energy_full',
                    power_now_file='current_now',
                    **widget_defaults)

screens = [Screen(top = bar.Bar([
    widget.GroupBox(urgent_alert_method='text',
        disable_drag=True,
        active = active,
        inactive = inactive,
        hilight_color = hilight_color,
        this_screen_border = ORANGE,
        other_current_screen_border = ORANGE,
        other_screen_border = "#444444",
        urgent_screen_border = "#ff4444",
        hilight_method="block",
        **widget_defaults),
    widget.Prompt(**widget_defaults),
    #widget.Clipboard(timeout=None, width=bar.STRETCH, max_width=None),
    #widget.TextBox("serge@hallyn.com", name="ident", width=bar.STRETCH, max_width=None),
    #widget.WindowCount(),
    widget.TextBox("serge@hallyn.com", name="ident", max_width=None),
    widget.WindowCount(width=bar.STRETCH, foreground="#5b447a", text_format="|w:{num}"),
    widget.KhalCalendar(foreground="#5b447a", max_width=25),
    widget.TextBox("B0:"),
    bat0,
    MyBright(),
    MyCheckinState(),
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
            qtile.groups_map[group].cmd_toscreen(toggle=False)
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
    #Key(["shift", "control"], "l", warp(100, 0)),
    #Key(["shift", "control"], "h", warp(-100, 0)),
    #Key(["shift", "control"], "j", warp(0, 100)),
    #Key(["shift", "control"], "k", warp(0, -100)),

    # interact with prompts
    Key([mod], "r",              lazy.spawncmd()),
    Key([mod], "g",              lazy.togroup()),

    Key([mod, "control"], "v",   lazy.spawn("/home/serge/bin/urlimg.xclip")),

    # start specific apps
    Key([mod], "n",              lazy.function(app_or_group("www", "firefox"))),
    Key([mod, "shift"], "n",     lazy.window.togroup("www")),
    Key([mod], "m",              lazy.function(app_or_group("music", "clementine"))),
    Key([mod, "shift"], "x",     lazy.window.kill()),
    Key([mod, "control"], "Return", lazy.spawn("tabbed vimprobable -e")),
    Key([mod], "Return",         lazy.spawn("st")),
    Key([mod, "shift"], "Return",         lazy.spawn("alacritty")),
    #Key([mod], "Return",         lazy.spawn("urxvt")),
    Key([mod], "F10",            lazy.spawn("/home/serge/bin/touchpad")),
    Key([mod], "F12",            lazy.spawn("/home/serge/bin/screengrab")),

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
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightness up")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightness down")),
]

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groups = []

# throwaway groups for random stuff
for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
    groups.append(Group(i))
    keys.append(
        Key([mod], i, lazy.group[i].toscreen(toggle=False))
    )
    keys.append(
        Key([mod, "shift"], i, lazy.window.togroup(i))
    )

groups.append(Group("X"))

# groups with special jobs. I usually navigate to these via my app_or_group
# function.
groups.extend([
    Group('music', spawn='clementine', layout='columns', persist=False,
          matches=[Match(wm_class=['Clementine', 'Viridian'])]),
    Group('www', spawn='firefox', layout='columns', persist=False,
          matches=[Match(wm_class=['Firefox', 'google-chrome', 'Google-chrome'])]),
])

border_args = dict(
    border_width=1,
)

layout_style = {
    'font': 'ubuntu',
    'border_normal_stack': '#000022',
    'border_focus_stack': '#0000ff',
    'wrap_focus_columns': False,
    'wrap_focus_rows': False,
    'focus_window_move': True
}

layouts = [
    layout.Columns(num_columns=1, insert_position=1, **layout_style),
    layout.Stack(num_stacks=2, **border_args),
    layout.Max(),

    # a layout just for gimp
    layout.Slice(side='left', width=192, name='gimp', role='gimp-toolbox',
         fallback=layout.Slice(side='right', width=256, role='gimp-dock',
         fallback=layout.Stack(num_stacks=1, **border_args))),

    layout.MonadTall(ratio=0.65, **border_args),
]

#no_utility = layout.floating.DEFAULT_FLOAT_WM_TYPES - {'utility'}
#floating_layout = layout.Floating(auto_float_types=no_utility)

cursor_warp = True
follow_mouse_focus = True
mouse = []

focus_on_window_activation = "never"
os.system("xmodmap ~/.xmodmaprc")
os.system("xrdb -merge ~/.Xresources")
os.system("synclient VertEdgeScroll=0")
#os.system("feh --bg-max ~/catherines_landing.jpg")
os.system("pidof xplanet || xplanet -longitude -95.358 -latitude 29.749 -fork")
os.system("synclient TouchpadOff=1")
os.system("pidof syndaemon || syndaemon  -R -k -K -d")
os.system("killall autocutsel")
os.system("autocutsel -selection PRIMARY -fork")
os.system("autocutsel -selection CLIPBOARD -fork")
os.system('xinput --set-prop "TPPS/2 Elan TrackPoint" "libinput Accel Speed" 1')

# vim: tabstop=4 shiftwidth=4 expandtab

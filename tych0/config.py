# -*- coding: utf-8 -*-
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.dgroups import simple_key_binder

from libqtile.log_utils import logger

import platform
import sys

# TODO:
#  2. multi screen switching

# Number of screens on machines I use regularly. I wish there was a good way to
# query this from qtile...
hostname = platform.node()
num_screens = {
    'tanders-ubuntu': 2,
    'smitten': 2,
    'hopstrocity': 1,
    'xephyr': 1,
}

sound_card = {
    'hopstrocity': 1,
    'smitten': 0,
}.get(hostname, 0)

# Global mod key. I have mod3 bound to caps lock, it's great.
mod = "mod3"

# If we're running in debug mode, it's for development. Make sure the
# hotkeys don't clash, only start one window, etc.
if '-d' in sys.argv:
    hostname = 'xephyr'
    mod = "mod4"

# global font options
widget_defaults = dict(
    font = 'Consolas',
    fontsize = 18,
    padding = 3,
)

inoffensive_green = '339966'

if num_screens[hostname] == 2:
    screens = [
        Screen(top = bar.Bar([
                widget.GroupBox(
                    urgent_alert_method='text',
                    this_current_screen_border=inoffensive_green,
                    disable_drag=True,
                    **widget_defaults
                ),
                widget.Prompt(**widget_defaults),
                widget.Spacer(),
                widget.Mpris(name='clementine', stop_pause_text='', **widget_defaults),
                widget.IdleRPG(url='http://xethron.lolhosting.net/xml.php?player=pants', **widget_defaults),
                widget.Mpris2(
                    name='spotify',
                    objname="org.mpris.MediaPlayer2.spotify",
                    display_metadata=['xesam:title', 'xesam:artist'],
                    scroll_chars=None,
                    stop_pause_text='',
                    **widget_defaults
                ),
                widget.Volume(**widget_defaults),
            ], 30,),
        ),
        Screen(top = bar.Bar([
                widget.GroupBox(
                    urgent_alert_method='text',
                    disable_drag=True,
                    this_current_screen_border=inoffensive_green,
                    **widget_defaults
                ),
                widget.Clipboard(timeout=None, width=bar.STRETCH, max_width=None),
                widget.BitcoinTicker(format="BTC: {avg}", **widget_defaults),
                widget.BitcoinTicker(format="LTC: {avg}", source_currency='ltc'),
                widget.BitcoinTicker(format="BTC: ฿{avg}", source_currency='ltc', currency='btc', round=False),
                widget.Systray(**widget_defaults),
                widget.Clock(format='%H:%M MSK', timezone='Europe/Moscow', **widget_defaults),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p', **widget_defaults),
            ], 30,),
        ),
    ]
else:
    # 1 screen
    screens = [Screen(top = bar.Bar([
            widget.GroupBox(urgent_alert_method='text', disable_drag=True, **widget_defaults),
            widget.Prompt(**widget_defaults),
            widget.Clipboard(timeout=None, width=bar.STRETCH, max_width=None),
            widget.BitcoinTicker(format="BTC: {avg}", **widget_defaults),
            widget.Mpris2(
                name='spotify',
                objname="org.mpris.MediaPlayer2.spotify",
                display_metadata=['xesam:title', 'xesam:artist'],
                scroll_chars=None,
                stop_pause_text='',
                **widget_defaults
            ),
            widget.Mpris(name='clementine', stop_pause_text='', **widget_defaults),
            # this pollutes ~/.qtile.log and i don't really use it, so drop it for now
            # widget.Volume(cardid=sound_card, **widget_defaults),
            # 1 screen means this is a laptop, so let's render the battery
            widget.Battery(energy_now_file='charge_now',
                energy_full_file='charge_full',
                power_now_file='current_now',
                **widget_defaults
            ),
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

last_playing = 'spotify'

def playpause(qtile):
    global last_playing
    if qtile.widgetMap['clementine'].is_playing() or last_playing == 'clementine':
        qtile.cmd_spawn("clementine --play-pause")
        last_playing = 'clementine'
    if qtile.widgetMap['spotify'].is_playing or last_playing == 'spotify':
        qtile.cmd_spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause")
        last_playing = 'spotify'

def next_prev(state):
    def f(qtile):
        if qtile.widgetMap['clementine'].is_playing():
            qtile.cmd_spawn("clementine --%s" % state)
        if qtile.widgetMap['spotify'].is_playing:
            cmd = "Next" if state == "next" else "Previous"
            qtile.cmd_spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.%s" % cmd)
    return f

keys = [
    # Log out; note that this doesn't use mod3: that's intentional in case mod3
    # gets hosed (which happens if you unplug and replug your usb keyboard
    # sometimes, or on ubuntu upgrades). This way you can still log back out
    # and in gracefully.
    Key(["shift", "mod1"], "q",  lazy.shutdown()),

    # I don't ever use floating, but sometimes it is handy to toggle to
    # floating for debugging, so I use the "out of band" mnemonic for this as
    # well.
    Key(["shift", "mod1"], "f",  lazy.window.toggle_floating()),

    Key([mod], "k",              lazy.layout.down()),
    Key([mod], "j",              lazy.layout.up()),
    Key([mod], "h",              lazy.layout.previous()),
    Key([mod], "l",              lazy.layout.next()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod, "shift"], "Return",lazy.layout.toggle_split()),
    Key(["mod1"], "Tab",         lazy.next_layout()),
    Key([mod, "mod1"], "h",      lazy.to_screen(0)),
    Key([mod, "mod1"], "l",      lazy.to_screen(1)),
    Key([mod], "x",              lazy.window.kill()),
    Key([mod, "shift"], "l",          lazy.layout.swap_left()),

    # interact with prompts
    Key([mod], "r",              lazy.spawncmd()),
    Key([mod], "g",              lazy.togroup()),

    # start specific apps
    Key([mod], "n",              lazy.function(app_or_group("www", "google-chrome"))),
    Key([mod], "m",              lazy.function(app_or_group("music", "clementine"))),
    Key([mod], "c",              lazy.function(app_or_group("io", "pidgin"))),
    Key([mod], "Return",         lazy.spawn("urxvt")),

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
    Key(
        [], "XF86AudioPlay",
        lazy.function(playpause)
    ),
    Key(
        [], "XF86AudioNext",
        lazy.function(next_prev("next"))
    ),
    Key(
        [], "XF86AudioPrev",
        lazy.function(next_prev("prev"))
    ),

    # also allow changing volume, tracks the old fashioned way
    Key([mod], "equal", lazy.spawn("amixer -c %d -q set Master 2dB+" % sound_card)),
    Key([mod], "minus", lazy.spawn("amixer -c %d -q set Master 2dB-" % sound_card)),
    Key([mod], "bracketleft", lazy.function(next_prev("prev"))),
    Key([mod], "bracketright", lazy.function(next_prev("next"))),

    # poor man's middle click
    Key([mod], "v",     lazy.spawn("xdotool click 2")),

    # backlight controls
    Key([], "XF86KbdBrightnessUp", lazy.spawn("maclight keyboard up")),
    Key([], "XF86KbdBrightnessDown", lazy.spawn("maclight keyboard down")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("maclight screen up")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("maclight screen down")),
]

host_specific_mouse = {
    'hopstrocity': [
        Click([mod], "Button1", lazy.spawn("xdotool click 3")),
    ],
}

mouse = host_specific_mouse.get(hostname, [])

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groups = []

# throwaway groups for random stuff
for i in ['a', 's', 'd', 'f', 'u', 'i', 'o', 'p']:
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
    Group('music', spawn='clementine', layout='max', persist=False,
          matches=[Match(wm_class=['Clementine', 'Viridian'])]),
    Group('www', spawn='google-chrome', layout='max', persist=False,
          matches=[Match(wm_class=['Firefox', 'google-chrome', 'Google-chrome'])]),
    Group('io', layout='pidgin', persist=False, init=False,
          matches=[Match(wm_class=['Pidgin'], role=['Buddy List'])]),
    Group('java', persist=False, init=False,
          matches=[Match(wm_class=['sun-awt-X11-XFramePeer', 'GroupWise'])]),
])

border_args = dict(
    border_width=1,
)

layouts = [
    layout.Stack(num_stacks=2, **border_args),
    layout.Max(),

    # a layout just for gimp
    layout.Slice(side='left', width=192, name='gimp', role='gimp-toolbox',
         fallback=layout.Slice(side='right', width=256, role='gimp-dock',
         fallback=layout.Stack(num_stacks=1, **border_args))),

    # a layout for pidgin
    layout.Slice(side='right', width=256, name='pidgin', role='buddy_list',
         fallback=layout.Stack(num_stacks=2, **border_args)),

    layout.MonadTall(ratio=0.65, **border_args),
]

no_utility = layout.floating.DEFAULT_FLOAT_WM_TYPES - {'utility'}
floating_layout = layout.Floating(auto_float_types=no_utility)

cursor_warp = True
follow_mouse_focus = True

focus_on_window_activation = "never"

# vim: tabstop=4 shiftwidth=4 expandtab

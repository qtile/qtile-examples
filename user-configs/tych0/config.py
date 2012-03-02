from libqtile.manager import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

import platform

# TODO:
#  1. better multi screen switching
#  2. better hotkeys for dgroups
#  3. perhaps make it so you don't have to pass font_options everywhere?

# Number of screens on machines I use regularly.
hostname = platform.node()
num_screens = {
    'tanders-ubuntu': 2,
    'smitten': 2,
    'smalls': 1,
}

# global font options
font_options = dict(
    font = 'Consolas',
    fontsize = 18,
    padding = 3,
)

if num_screens[hostname] == 2:
    screens = [
        Screen(top = bar.Bar([
                widget.GroupBox(urgent_alert_method='text', **font_options),
                widget.Prompt(**font_options),
                widget.WindowName(**font_options),
                widget.Mpris(**font_options),
                widget.Volume(**font_options),
            ], 30,),
        ),
        Screen(top = bar.Bar([
                widget.GroupBox(urgent_alert_method='text', **font_options),
                widget.WindowName(**font_options),
                widget.Systray(),
                widget.Clock('%Y-%m-%d %a %I:%M %p', **font_options),
            ], 30,),
        ),
    ]
else:
    # 1 screen
    screens = [Screen(top = bar.Bar([
            widget.GroupBox(urgent_alert_method='text', **font_options),
            widget.Prompt(**font_options),
            widget.WindowName(**font_options),
            widget.Volume(**font_options),
            # 1 screen means this is a laptop, so let's render the battery
            widget.Battery(energy_now_file='charge_now',
                energy_full_file='charge_full',
                power_now_file='current_now',
                **font_options),
            widget.Systray(),
            widget.Clock('%Y-%m-%d %a %I:%M %p', **font_options),
        ],30,),),
    ]

keys = [
    # Log out; note that this doesn't use mod3: that's intentional in case mod3
    # gets hosed (which happens if you unplug and replug your usb keyboard
    # sometimes, or on ubuntu upgrades). This way you can still log back out
    # and in gracefully.
    Key(["shift", "mod1"], "q",     lazy.shutdown()),

    Key(["mod3"], "k",              lazy.layout.down()),
    Key(["mod3"], "j",              lazy.layout.up()),
    Key(["mod3"], "h",              lazy.layout.previous()),
    Key(["mod3"], "l",              lazy.layout.previous()),
    Key(["mod3", "shift"], "space", lazy.layout.rotate()),
    Key(["mod3", "shift"], "Return",lazy.layout.toggle_split()),
    Key(["mod1"], "Tab",            lazy.nextlayout()),
    Key(["mod3", "mod1"], "h",      lazy.to_screen(0)),
    Key(["mod3", "mod1"], "l",      lazy.to_screen(1)),
    Key(["mod3"], "x",              lazy.window.kill()),

    # interact with prompts
    Key(["mod3"], "r",              lazy.spawncmd()),
    Key(["mod3"], "g",              lazy.switchgroup()),

    # start specific apps
    Key(["mod3"], "n",              lazy.spawn("firefox")),
    Key(["mod3"], "m",              lazy.spawn("clementine")),
    Key(["mod3"], "Return",         lazy.spawn("xterm")),

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

    # also allow changing volume the old fashioned way
    Key(["mod3"], "equal", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key(["mod3"], "minus", lazy.spawn("amixer -c 0 -q set Master 2dB-")),

    # allow play pause as well
    Key(["mod3"], "p",     lazy.spawn("vif.py play_pause")),
]

# Drag floating layouts.
mouse = [
    Drag(["mod3"], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag(["mod3"], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click(["mod3"], "Button2", lazy.window.bring_to_front())
]

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
static_groups = ['a', 's', 'd', 'f']
groups = []
for i in static_groups:
    groups.append(Group(i))
    keys.append(
        Key(["mod3"], i, lazy.group[i].toscreen())
    )
    keys.append(
        Key(["mod3", "mod1"], i, lazy.window.togroup(i))
    )

border_args = dict(
    border_width=1,
)

layouts = [
    layout.Stack(stacks=2, **border_args),
    layout.Max(),

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

def main(qtile):
    from dgroups import DGroups, Match, simple_key_binder

    dynamic_groups = {
        'music': {'exclusive': False, 'spawn': 'clementine'},
        'www': {'exclusive': False, 'layout': 'max'},
        'io': {'exclusive': False, 'layout': 'pidgin'},
        'java': {'exclusive': False, 'layout': 'stack'},
    }

    # persist any already set up groups
    global static_groups
    for group in static_groups:
        dynamic_groups[group] = {'persist': True}

    apps = [
        {'match': Match(wm_class=['Firefox', 'google-chrome', 'Google-chrome']),
         'group': 'www'},
        {'match': Match(wm_class=['Pidgin'], role=['Buddy List']),
         'group': 'io'},
        {'match': Match(wm_class=['Clementine', 'Viridian']),
         'group': 'music'},
        {'match': Match(wm_class=['sun-awt-X11-XFramePeer', 'GroupWise']),
         'group': 'java'},
    ]

    dgroups = DGroups(qtile, dynamic_groups, apps, simple_key_binder('mod3'))

# vim: tabstop=4 shiftwidth=4 expandtab

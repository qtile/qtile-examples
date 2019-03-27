#!/usr/bin/env python
# coding=utf-8

from libqtile.config import Key, Drag, Click
from libqtile.command import lazy

from groups import groups
from platforms import num_screens, hostname

mod = "mod4"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "Tab", lazy.layout.down()),
    # Switch window focus to other pane(s) of stack
    Key([mod], "h", lazy.layout.next()),
    Key([mod], "l", lazy.layout.next()),

    # Move windows up or down in current stack
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # Resize
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod], "n", lazy.layout.normalize()),

    # Close window
    Key([mod, "shift"], "c", lazy.window.kill()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("urxvt")),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    # toggle visibiliy of above defined DropDown named "term"
    Key([mod], 'z', lazy.group['scratchpad'].dropdown_toggle('term')),

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
]


# Depending on how many screens I have, state which group goes on which screen
# Just a static list, nothing fancy
# k is the key/group
# g is which screen it should go on
if num_screens[hostname] == 4:
    k = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "minus", "equal"]
    g = [3, 3, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2]
else:
    k = ["1", "2", "3", "4", "equal"]
    g = [0, 0, 0, 0, 0]
# Loop over the groups, and setup keys for each group to move groups to screens
# and move focus to screens/groups
for index, i in enumerate(groups):
    keys.extend([
        # mod1 + number of group (starting with 1) = switch to group
        Key([mod], k[index],
            lazy.group[i.name].toscreen(g[index]),
            lazy.to_screen(g[index])),

        # mod1 + shift + number of group (starting with 1) = switch to & move focused window to group
        Key([mod, "shift"], k[index], lazy.window.togroup(i.name)),
    ])

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

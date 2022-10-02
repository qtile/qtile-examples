#!/usr/bin/env python
# coding=utf-8

import os
import subprocess

from libqtile.config import Key, Drag, Click
from libqtile.command import lazy

from groups import groups
from platforms import num_screens, hostname
from timelogger import *  # NOQA
from KeyChain import KeyNode


mod3 = "Hyper_L"
mod4 = "mod4"
returnkey = "Escape"

# Lock the screensaver (password)
def lock(data):
    log_text("xscreensaver|manual lock")
    os.system("xscreensaver-command -lock")

# Call xmodmap (which remaps CapsLock to Hyper to mod3)
@hook.subscribe.startup_once
def set_keymap():
    subprocess.run(['xmodmap', '~/.Xmodmap'])

# Create home (default) mode keys
home = KeyNode([], returnkey, [], ishome=True, name="Home")

# Set the extra mode
extra = KeyNode([], mod3, [], name="Extra")

# Add the extra node, and any default keys to the home node
home.addchildren(
    extra,
    
    # Switch between windows in current stack pane
    KeyNode([mod4], "k", [], lazy.layout.down()),
    KeyNode([mod4], "j", [], lazy.layout.up()),
    KeyNode([mod4], "Tab", [], lazy.layout.down()),

    # Switch window focus to other pane(s) of stack
    KeyNode([mod4], "h", [], lazy.layout.next()),
    KeyNode([mod4], "l", [], lazy.layout.next()),

    # Move windows up or down in current stack
    KeyNode([mod4, "shift"], "j", [], lazy.layout.shuffle_down()),
    KeyNode([mod4, "shift"], "k", [], lazy.layout.shuffle_up()),
    KeyNode([mod4, "shift"], "h", [], lazy.layout.shuffle_left()),
    KeyNode([mod4, "shift"], "l", [], lazy.layout.shuffle_right()),

    # Resize
    KeyNode([mod4, "control"], "j", [], lazy.layout.grow_down()),
    KeyNode([mod4, "control"], "k", [], lazy.layout.grow_up()),
    KeyNode([mod4, "control"], "h", [], lazy.layout.grow_left()),
    KeyNode([mod4, "control"], "l", [], lazy.layout.grow_right()),

    KeyNode([mod4], "m", [], lazy.layout.maximize()),
    KeyNode([mod4], "n", [], lazy.layout.normalize()),
    KeyNode([mod4], "f", [], lazy.window.toggle_floating()),

    # Close window
    KeyNode([mod4, "shift"], "c", [], lazy.window.kill()),

    # Swap panes of split stack
    KeyNode([mod4, "shift"], "space", [], lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    KeyNode([mod4, "shift"], "Return", [], lazy.layout.toggle_split()),
    KeyNode([mod4], "Return", [], lazy.spawn("urxvt")),

    # Toggle between different layouts as defined below
    KeyNode([mod4], "space", [], lazy.next_layout()),

    # Restart or quit qtile
    KeyNode([mod4, "control"], "r", [], lazy.restart()),
    KeyNode([mod4, "control"], "q", [], lazy.shutdown()),

    # Launch a command
    KeyNode([mod4], "r", [], lazy.spawncmd()),

    # toggle visibiliy of above defined DropDown named "term"
    KeyNode([mod4], 'z', [], lazy.group['scratchpad'].dropdown_toggle('term')),

    # Lock the screensaver (password)
    KeyNode([mod4], "F12", [], lazy.function(lock)),

    # Change the volume if our keyboard has keys
    KeyNode(
        [], "XF86AudioRaiseVolume", [],
        lazy.spawn("amixer -c 0 -q set Master 2dB+")
    ),
    KeyNode(
        [], "XF86AudioLowerVolume", [],
        lazy.spawn("amixer -c 0 -q set Master 2dB-")
    ),
    KeyNode(
        [], "XF86AudioMute", [],
        lazy.spawn("amixer -c 0 -q set Master toggle")
    ),
)

# Set the home of the extra node
extra.sethome(home)
# set the main qtile keys variable to the children of the home node.
keys = home.children

# Make a new qtile_keys node, with children
qtile_keys = KeyNode([], "q", [
    KeyNode([], 'r', [], lazy.restart()),
    KeyNode(["shift"], 'q', [], lazy.shutdown()),
    KeyNode([], "space", [], lazy.next_layout()),
    KeyNode([], 'e', [], lazy.spawn('gvim ~/configs/qtile/keys.py')),
], name="qtile")

# Make a new open_keys node, with children
open_keys = KeyNode([], 'o', [
    KeyNode([], 'c', [], lazy.spawn("google-chrome")),
    KeyNode([], 'v', [], lazy.spawn("code")),
    KeyNode([], 'g', [], lazy.spawn("gvim")),
    KeyNode([], 'o', [], lazy.spawn('rofi -show run')),
], name='open')

# Add the other modes to the root
extra.addchildren(
    open_keys, # o
    qtile_keys, # q
)


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
    home.addchildren(
        # mod1 + number of group (starting with 1) = switch to group
        KeyNode([mod4], k[index], [], lazy.group[i.name].toscreen(g[index]), lazy.to_screen(g[index])),

        # mod1 + shift + number of group (starting with 1) = switch to & move focused window to group
        KeyNode([mod4, "shift"], k[index], [], lazy.window.togroup(i.name)),
    )

# Drag floating layouts.
mouse = [
    Drag([mod4], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod4], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod4], "Button2", lazy.window.bring_to_front())
]

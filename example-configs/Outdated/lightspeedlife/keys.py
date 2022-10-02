"""Static Key Definitions"""
# import pudb
import logging

from libqtile.config import Key, Drag, Click
from libqtile.command import lazy

from groups import init_groups
from layman import layMan

import os, datetime

HOME = os.path.expanduser('~/')
DATETIME = datetime.datetime.now().strftime('%Y%m%d.%H%M:%S')
TERMUX = "termite -e tmux"

# KEY DEFINITIONS
# 
mod = "mod4"
shift = "shift"
alt = "mod1"
ctrl = "control"
#not needed since ctrl+shift grabs keys in Xephyr
# if '-l' in sys.argv:
#     hostname = 'xephyr'
#     mod = 'mod1'
#     alt = 'f1'

def init_ambig_keys():
    """For layMan key-switcher (WIP): ambiguous layout keys"""
    return []

def init_groups_keys():
    available_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'F1', 'F2', 'F3', 'F4' ]
    keys = []
    for key, group in enumerate(init_groups()):
        if key < len(available_keys):
            keys.extend([
                #switch to group
                Key([mod], available_keys[key], lazy.group[group.name].toscreen()),

                #send to group
                Key([mod, shift], available_keys[key], lazy.window.togroup(group.name)),
            ])
        else: 
            logging.info('groups to bind exceeds available keys')
            break
    # TODO: fix this hacky, ugly nonsense.
    keys.extend([
        Key([mod, shift], 'F1', lazy.group['scratch'].dropdown_toggle('term')),
        ])
    return keys

def init_const_keys():
    """For layMan key-switcher (WIP): non-layout, consistent keys"""
    keys = [
        # Switch window focus to other pane(s) of stack
        Key([mod], "Tab", lazy.layout.next()),
        Key([mod, shift], 'Tab', lazy.layout.previous()),

        # Toggle between split and unsplit sides of stack.
        # Split = all windows displayed
        # Unsplit = 1 window displayed, like Max layout, but still with
        # multiple stack panes

        Key([mod], 'w', lazy.window.toggle_minimize()),
        Key([mod, shift], 'w', lazy.window.toggle_minimize()),

        # Toggle between different layouts as defined below
        Key([mod], "space", lazy.next_layout()),
        Key([mod, shift], "space", lazy.prev_layout()),

        Key([mod, shift], "q", lazy.restart()),
        Key([mod, ctrl], "q", lazy.shutdown()),
        Key([mod, shift], "semicolon", lazy.spawncmd()),

        # Scrotter
        Key([mod, shift], 'a', lazy.spawn([
        	'scrot', '-q', '100',
        	'%Y%m%d.%H%M:%S_qtile.png',
            '-e', 'mv $f ~/Screenshots/',
        	])),
        Key([mod, shift], 'u', lazy.spawn([
        	'scrot', '-ubq', '100',
            '%Y%m%d.%H%M:%S_window.png',
            '-e', 'mv $f ~/Screenshots',
        	])),
        # TODO: grab mouse for this
        Key([mod, shift], 's', lazy.spawn([
        	'scrot', '-sq', '100',
            '%Y%m%d.%H%M:%S_selection.png',
            '-e', 'mv $f ~/Screenshots',
        	])),

        # Window Ops
        Key([mod], "x", lazy.window.kill()),
        Key([mod], "t", lazy.window.toggle_floating()),
        Key([mod, shift], "e", lazy.window.toggle_fullscreen()),
        Key([mod], "semicolon", lazy.spawn(TERMUX)),

        #movement
        Key([mod], "g", lazy.togroup()),

        Key([mod], "slash", lazy.findwindow()),

        # Sound and Mpd
        Key([], "XF86AudioRaiseVolume",
            lazy.spawn("amixer sset Master 5%+")),
        Key([], "XF86AudioLowerVolume",
            lazy.spawn("amixer sset Master 5%-")),
        Key([], "XF86AudioMute",
            lazy.spawn("amixer sset Master toggle")),

        Key([], "XF86AudioNext",
            # lazy.function(lambda q: fipc_jango("next"))),
            lazy.spawn("mpc next")),
        Key([], "XF86AudioPrev",
            # lazy.function(lambda q: fipc_jango("prev"))),
            lazy.spawn("mpc prev")),
        # No mute key @notebook
        Key([shift], "XF86AudioMute"),

        # Key([], "F12", lazy.function(SwapGroup('h4x'))), #qtile-examples/roger/
        # Key(['shift'], "F12", lazy.function(to_urgent)), #qtile-examples/roger/
    ]
    keys.extend(init_groups_keys())
    return keys
    
def init_const_mouse():
    # Mouse bindings
    # TODO: raise/lower windows w/ scroll-wheel
    return [
        Drag([mod], "Button1", lazy.window.set_position_floating(),
             start=lazy.window.get_position()),
        Drag([mod], "Button3", lazy.window.set_size_floating(),
             start=lazy.window.get_size()),
        Click([mod], "Button2", lazy.window.bring_to_front())
    ]

def init_layout_specials():
    """TODO: This needs some sort of conflict checking. Many commands are
    common to different layouts. In a future patch, I would consider 
    assigning these commands in reverse: a list of commands with one or more
    (layout, key) combinations that use it."""
    return {
        'ambiguous': [
         ],
         'bsp': [
            Key([mod], "j", lazy.layout.down()),
            Key([mod], "k", lazy.layout.up()),
            Key([mod], 'h', lazy.layout.left()),
            Key([mod], 'l', lazy.layout.right()),

            # resize windows, also in bsp
            Key([mod], "o", lazy.layout.grow_down()),
            Key([mod, shift], "o", lazy.layout.grow_up()),
            Key([mod, shift], "i", lazy.layout.grow_left()),

            Key([mod], "i", lazy.layout.grow_right()),
            Key([mod, "mod1"], "j", lazy.layout.flip_down()),
            Key([mod, "mod1"], "k", lazy.layout.flip_up()),
            Key([mod, "mod1"], "h", lazy.layout.flip_left()),
            Key([mod, "mod1"], "l", lazy.layout.flip_right()),
            Key([mod, shift], "n", lazy.layout.normalize()),
         ],
         'columns': [
            Key([mod], "j", lazy.layout.down()),
            Key([mod], "k", lazy.layout.up()),
            Key([mod], 'h', lazy.layout.left()),
            Key([mod], 'l', lazy.layout.right()),


            # shuffle windows
            Key([mod, shift], 'k', lazy.layout.shuffle_up()),
            Key([mod, shift], 'j', lazy.layout.shuffle_down()),
            Key([mod, shift], 'h', lazy.layout.shuffle_left()),
            Key([mod, shift], 'l', lazy.layout.shuffle_right()),

            # resize windows, also in bsp
            Key([mod], "o", lazy.layout.grow_down()),
            Key([mod, shift], "o", lazy.layout.grow_up()),
            Key([mod, shift], "i", lazy.layout.grow_left()),
            Key([mod], "i", lazy.layout.grow_right()),

            Key([mod], "backslash", lazy.layout.toggle_split()),

            # Swap panes of split stack
            Key([mod, shift], "Return", lazy.layout.rotate()),

            Key([mod, shift], "n", lazy.layout.normalize()),
         ],
         'monadtall': [
            Key([mod], "j", lazy.layout.down()),
            Key([mod], "k", lazy.layout.up()),
            Key([mod], 'h', lazy.layout.left()),
            Key([mod], 'l', lazy.layout.right()),

            Key([mod, shift], 'k', lazy.layout.shuffle_up()),
            Key([mod, shift], 'j', lazy.layout.shuffle_down()),

            # Grow/Shrink windows
            Key([mod], 'o', lazy.layout.grow()),
            Key([mod, shift], 'o', lazy.layout.shrink()),

            Key([mod], 'Return', lazy.layout.swap_left()),
            Key([mod, shift], 'Return', lazy.layout.swap_right()),

            Key([mod], 'apostrophe', lazy.layout.flip()),
            Key([mod], "m", lazy.layout.maximize()),
            Key([mod, shift], "n", lazy.layout.normalize()),
         ],
        'plasma': [
            # Move windows around in current stack
            Key([mod], 'k', lazy.layout.move_up()),
            Key([mod], 'j', lazy.layout.move_down()),
            Key([mod], 'h', lazy.layout.move_let()),
            Key([mod], 'l', lazy.layout.move_right()),

            # Inset windows into different leaves of the tree
            Key([mod, shift], "k", lazy.layout.integrate_down()),
            Key([mod, shift], "j", lazy.layout.integrate_up()),
            Key([mod, shift], "h", lazy.layout.integrate_left()),
            Key([mod, shift], "l", lazy.layout.integrate_right()),

            Key([mod], 's', lazy.layout.mode_vertical_split()),
            Key([mod, shift], 's', lazy.layout.mode_horizontal_split()),


            # Grow/Shrink sizing
            Key([mod], "o", lazy.layout.grow_height(30)),
            Key([mod, shift], "o", lazy.layout.grow_height(-30)),
            Key([mod], "i", lazy.layout.grow_width(30)),
            Key([mod, shift], "i", lazy.layout.grow_width(-30)),

            # Reset sizing
            Key([mod], 'Escape', lazy.layout.reset_size()),

            # Key([mod], 'hyphen', lazy.layout.mode_horizontal()),
            # Key([mod], 'backslash', lazy.layout.mode_vertical()),
        ]
    }

def init_groups_specials():
    """similarly unused"""
    return {}

def init_binds():
    inputs = layMan(init_const_keys(), init_const_mouse(),
        init_layout_specials(), init_groups_specials())
    inputs.configure()
    return inputs
    

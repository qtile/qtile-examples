#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import bar, hook, layout, widget
from subprocess import call

# reconfigure screens
call("setup_screens")

# monadtall extention to follow maximized window if we have only two
@lazy.function
def z_maximize(qtile):
    l = qtile.currentLayout
    g = qtile.currentGroup
    l.cmd_maximize()
    if len(g.windows) == 2:
        fw = qtile.currentWindow
        ow = None
        # get other window
        for w in g.windows:
            if w != fw:
                ow = w

        if ow and fw.info()['width'] < ow.info()['width']:
            l.cmd_next()


##-> Commands to spawn
class Commands(object):
    dmenu = 'dmenu_run -i -b -p ">>>" -fn "Open Sans-10" -nb "#000" -nf "#fff" -sb "#00BF32" -sf "#fff"'
    screenshot = 'scrot_s'
    volume_up = 'amixer -q -c 0 sset Master 5dB+'
    volume_down = 'amixer -q -c 0 sset Master 5dB-'
    volume_toggle = 'amixer -q set Master toggle'
    dmenu_session = 'dmenu-session'
    dmenu_mocp = 'dmenu-mocp'
    dmenu_windows = 'dmenu-qtile-windowlist.py'
    terminal = 'urxvt -e bash -c "tmux -q has-session && exec tmux attach-session -d || exec tmux new-session -n$USER -s$USER@$HOSTNAME"'
    pacman = 'urxvt -e bash -c "yaourt -Syua"'


##-> Theme + widget options
class Theme(object):
    bar = {
        'size': 24,
        'background': '15181a',
        }
    widget = {
        'font': 'Andika',
        'fontsize': 11,
        'background': bar['background'],
        'foreground': '00ff00',
        }
    graph = {
        'background': '000000',
        'border_width': 0,
        'border_color': '000000',
        'line_width': 1,
        'margin_x': 0,
        'margin_y': 0,
        'width': 50,
        }
    groupbox = widget.copy()
    groupbox.update({
        'padding': 2,
        'borderwidth': 3,
        })
    sep = {
        'background': bar['background'],
        'foreground': '444444',
        'height_percent': 75,
        }
    systray = widget.copy()
    systray.update({
        'icon_size': 16,
        'padding': 3,
        })
    pacman = widget.copy()
    pacman.update({
        'foreground': 'ff0000',
        'unavailable': '00ff00',
        })
    battery = widget.copy()
    battery_text = battery.copy()
    battery_text.update({
        'low_foreground': 'FF0000',
        'charge_char': "↑ ",
        'discharge_char': "↓ ",
        'format': '{char}{hour:d}:{min:02d}',
        })


##-> Keybindings
mod = 'mod4'
keys = [
    ## Window Manager Controls
    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'q', lazy.spawn(Commands.dmenu_session)),
    Key([mod, "shift"], "x", lazy.hide_show_bar("top")),
    Key([mod, 'shift'], 'w', lazy.window.kill()),
    Key([mod, 'shift'], "Tab", lazy.next_screen()),

    ## Window Controls
    Key([mod], "n", lazy.layout.reset()), # normalize is useless
    Key([mod], "o", z_maximize),
    Key([mod, "shift"], "space", lazy.layout.flip()),
    # Switch window focus to other pane(s) of stack
    Key( [mod], "space", lazy.layout.next()),
    Key( [mod], "k", lazy.layout.down()),
    Key( [mod], "j", lazy.layout.up()),
    # Move windows up or down in current stack
    Key( [mod, "control"], "k", lazy.layout.shuffle_down()),
    Key( [mod, "control"], "j", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "l", lazy.layout.grow()),
    Key([mod, "shift"], "h", lazy.layout.shrink()),
    Key([mod], "Tab",    lazy.nextlayout()),

    ## Volume Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(Commands.volume_up)),
    Key([], 'XF86AudioLowerVolume', lazy.spawn(Commands.volume_down)),
    Key([], 'XF86AudioMute', lazy.spawn(Commands.volume_toggle)),

    Key([], 'Print', lazy.spawn(Commands.screenshot)),
    Key([mod], 'm', lazy.spawn(Commands.dmenu_mocp)),
    Key([mod], 'l', lazy.spawn(Commands.dmenu_windows)),

    Key([mod], "Return", lazy.spawn(Commands.terminal)),

    Key([mod], 'r', lazy.spawn(Commands.dmenu)),
]

groups = [
    Group("a"),
    Group("s"),
    Group("d"),
    Group("f"),
    Group("g"),
]
for i in groups:
    # mod + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )


##-> Mouse
mouse = (
    Drag([mod], 'Button1', lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.toggle_floating())
)



layouts = [
    layout.Max(),
    layout.MonadTall(follow_max=True),
]

screens = [
    Screen(
        top=bar.Bar(widgets=[
            widget.GroupBox(urgent_alert_method='text', **Theme.groupbox),
            widget.CurrentLayout(**Theme.widget),
            widget.WindowName(**Theme.widget),
            widget.Clipboard(timeout=10, **Theme.systray),
            widget.Systray(**Theme.systray),
            widget.Battery(**Theme.battery_text),
            widget.Pacman(execute=Commands.pacman, **Theme.pacman),
            widget.GmailChecker(fmt=u"✉ %s", username='XXX',
                password='XXX', status_only_unseen=True, **Theme.battery_text),
            widget.KeyboardLayout(configured_keyboards=['us', 'lt'], **Theme.widget),

            widget.Volume(emoji=True,
                mute_command=[
                    'amixer',
                    '-q',
                    'set',
                    'Master',
                    'toggle'],
                **Theme.widget),

            widget.Clock(fmt='⏰ %Y-%m-%d %H:%M', **Theme.widget),

            widget.CPUGraph(graph_color="#FF0000",
                    border_color="#FF0000"),

            widget.NetGraph(graph_color="#086FA1",
                    border_color="#086FA1",
                    interface="wlp4s0",
                    bandwidth_type="down"),
            
            ], **Theme.bar),
    ),
]

##-> Floating windows
floating_layout = layout.floating.Floating(float_rules=[{'wmclass': x} for x in (
    'Download',
    'dropbox',
    'file_progress',
    "notification",
    "toolbar",
    "splash",
    "dialog",
    )])


import subprocess, re, os

@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    popup = window.window.get_wm_type() == 'popup'
    transient = window.window.get_wm_transient_for()
    if (dialog or transient) or popup:
        window.floating = True


# start the applications at Qtile startup
@hook.subscribe.startup
def startup():
    pass


# look for new monitor
@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    call("setup_screens")
    qtile.cmd_restart()


main = None
follow_mouse_focus = True
cursor_warp = False
auto_fullscreen = True
widget_defaults = {}
wmname = "LG3D"

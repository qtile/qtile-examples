# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, re, socket, subprocess
from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Rule, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401
from libqtile.widget import Spacer

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
#mod2 = "control"
#mod3 = "shift"
home = os.path.expanduser('~')

#terminal = guess_terminal()
terminal = "st"

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod], "r", lazy.spawncmd(),
        #desc="Spawn a command using a prompt widget"),

    # Keybindings to launch user defined programs
    Key(["mod1"], "w", lazy.spawn("brave-browser"), desc="Launch brave-browser"),
    Key(["mod1"], "r", lazy.spawn("rofi -show run"), desc="Launch rofi"),
    Key(["mod1"], "d", lazy.spawn("dmenu_run"), desc="Launch dmenu"),
    Key(["mod1"], "f", lazy.spawn('thunar'), desc="Launch thunar"),
    Key(["mod1"], "t", lazy.spawn('urxvtc'), desc="Launch rxvt-unicode"),
    Key(["mod1"], "n", lazy.spawn('nitrogen'), desc="Launch nitrogen"),
]

groups = []

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

#group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
group_labels = ["web", "irc", "mail", "net", "doc", "gfx", "media", "sys", "dev", "misc",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "treetab", "floating",]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
            )
        )

for i in groups:
    keys.extend([
        #Change workspaces
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key(["mod1"], "space", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        # Move window to selected workspace 1-10 and stay on workspace
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
        # Move window to selected workspace 1-10 and follow moved window to workspace
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

def init_layout_theme():
    return {"margin": 4,
            "border_width": 2,
            "border_focus": '#5e81ac',
            "border_normal": '#4c566a'
            }

layout_theme = init_layout_theme()

layouts = [
    layout.Columns(border_focus_stack=['#d75f5f', '#8f3d3d'], border_width=4),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.MonadTall(margin=4, border_width=2, border_focus='#5e81ac', border_normal='#4c566a'),
    layout.MonadWide(margin=4, border_width=2, border_focus='#5e81ac', border_normal='#4c566a'),
    layout.RatioTile(**layout_theme),
    # layout.Tile(),
    # layout.TreeTab(),
    layout.VerticalTile(**layout_theme),
    # layout.Zoomy(),
]

#Colors for the bar
def init_colors():
    return [["#2E3440", "#2E3440"], # color 0 bg
            ["#2E3440", "#2E3440"], # color 1 bg
            ["#D8DEE9", "#D8DEE9"], # color 2 fg
            ["#EBCB8B", "#EBCB8B"], # color 3 yellow
            ["#5E81AC", "#5E81AC"], # color 4 deep blue
            ["#E5E9F0", "#E5E9F0"], # color 5 bright
            ["#BF616A", "#BF616A"], # color 6 deep red
            ["#A3BE8C", "#A3BE8C"], # color 7 light yellow
            ["#81A1C1", "#81A1C1"], # color 8 light blue
            ["#B48EAD", "#B48EAD"]] # color 9 deep grey

colors = init_colors()

#Widgets for the bar
def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize = 12,
                padding = 3,
                background=colors[1])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
        widget.Image(
            filename = "~/.config/qtile/icons/qtilelogo.png",
            iconsize = 10,
            background = colors[1],
            mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn('rofi -show run')}
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            foreground = colors[2],
            background = colors[1]
            ),
        widget.GroupBox(
            active=colors[9],
            inactive=colors[5],
            highlight_method='line',
            this_current_screen_border=colors[3],
            foreground = colors[2],
            background = colors[1]
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            foreground = colors[2],
            background = colors[1]
            ),
        widget.WindowName(font="Noto Sans",
            fontsize = 12,
            foreground = colors[5],
            background = colors[1],
            ),
        #widget.Spacer(),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            foreground = colors[2],
            background = colors[1]
            ),
        widget.Systray(
            background=colors[1],
            icon_size=20,
            padding = 4
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            foreground = colors[2],
            background = colors[1]),
        widget.CPUGraph(
            border_color = colors[2],
            fill_color = colors[3],
            graph_color = colors[3],
            background=colors[1],
            border_width = 1,
            line_width = 1,
            core = "all",
            type = "box"
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            foreground = colors[2],
            background = colors[1]
            ),
        widget.NetGraph(
            font="Noto Sans",
            fontsize=12,
            bandwidth="down",
            interface="auto",
            fill_color = colors[3],
            foreground=colors[2],
            background=colors[1],
            graph_color = colors[3],
            border_color = colors[2],
            padding = 0,
            border_width = 1,
            line_width = 1,
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            foreground = colors[2],
            background = colors[1]
            ),
        widget.Memory(
            font="Noto Sans",
            format='{MemUsed:.0f}{mm}',
            update_interval = 1,
            fontsize = 12,
            foreground = colors[5],
            background = colors[1],
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            foreground = colors[2],
            background = colors[1]
            ),
        widget.Clock(
            foreground = colors[5],
            background = colors[1],
            fontsize = 12,
            format="%Y-%m-%d %H:%M"
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            foreground = colors[2],
            background = colors[1]
            ),
        widget.CurrentLayout(
            font = "Noto Sans Bold",
            foreground = colors[5],
            background = colors[1]
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            foreground = colors[2],
            background = colors[1]
            ),
        widget.CurrentLayoutIcon(
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            foreground = colors[8],
            background = colors[1],
            padding = 0,
            scale = 0.7
            ),
        ]
    return widgets_list

widgets_list = init_widgets_list()

def init_widgets_screen():
    widgets_screen = init_widgets_list()
    return widgets_screen

widgets_screen = init_widgets_screen()

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen(), size=24, opacity=0.8))]
screens = init_screens()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

#floating_types = ["notification", "toolbar", "splash", "dialog"]

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

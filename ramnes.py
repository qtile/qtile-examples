# -*- coding: utf-8 -*-
# Configuration repository: https://github.com/ramnes/qtile-config/
import os
import socket

from libqtile import bar, hook, layout
from libqtile.command import lazy
from libqtile.config import Drag, Group, Key, Screen
from libqtile.widget import (Battery, Clock, CurrentLayout, CurrentLayoutIcon,
                             GroupBox, Notify, Prompt, Sep, Systray, TaskList,
                             TextBox)

DEBUG = os.environ.get("DEBUG")
HOME = os.path.expanduser("~") + "/"

GREY = "#444444"
DARK_GREY = "#333333"
BLUE = "#007fcf"
DARK_BLUE = "#005083"
ORANGE = "#dd6600"
DARK_ORANGE = "#582c00"


def window_to_prev_group():
    @lazy.function
    def __inner(qtile):
        i = qtile.groups.index(qtile.currentGroup)
        if qtile.currentWindow and i != 0:
            group = qtile.groups[i - 1].name
            qtile.currentWindow.togroup(group)
    return __inner


def window_to_next_group():
    @lazy.function
    def __inner(qtile):
        i = qtile.groups.index(qtile.currentGroup)
        if qtile.currentWindow and i != len(qtile.groups):
            group = qtile.groups[i + 1].name
            qtile.currentWindow.togroup(group)
    return __inner


def window_to_prev_screen():
    @lazy.function
    def __inner(qtile):
        i = qtile.screens.index(qtile.currentScreen)
        if i != 0:
            group = qtile.screens[i - 1].group.name
            qtile.currentWindow.togroup(group)
    return __inner


def window_to_next_screen():
    @lazy.function
    def __inner(qtile):
        i = qtile.screens.index(qtile.currentScreen)
        if i != len(qtile.screens):
            group = qtile.screens[i + 1].group.name
            qtile.currentWindow.togroup(group)
    return __inner


def switch_screens():
    @lazy.function
    def __inner(qtile):
        i = qtile.screens.index(qtile.currentScreen)
        group = qtile.screens[i - 1].group
        qtile.currentScreen.setGroup(group)
    return __inner


@hook.subscribe.client_new
def set_floating(window):
    floating_types = ["notification", "toolbar", "splash", "dialog"]
    floating_roles = ["EventDialog", "Msgcompose", "Preferences"]
    floating_names = ["Terminator Preferences"]

    if (window.window.get_wm_type() in floating_types
        or window.window.get_wm_window_role() in floating_roles
        or window.window.get_name() in floating_names
        or window.window.get_wm_transient_for()):
        window.floating = True


def init_keys():
    keys = [
        Key([mod], "Left", lazy.screen.prev_group(skip_managed=True)),
        Key([mod], "Right", lazy.screen.next_group(skip_managed=True)),

        Key([mod, "shift"], "Left", window_to_prev_group()),
        Key([mod, "shift"], "Right", window_to_next_group()),

        Key([mod, "mod1"], "Left", lazy.prev_screen()),
        Key([mod, "mod1"], "Right", lazy.next_screen()),

        Key([mod, "shift", "mod1"], "Left", window_to_prev_screen()),
        Key([mod, "shift", "mod1"], "Right", window_to_next_screen()),

        Key([mod], "t", switch_screens()),

        Key([mod], "Up", lazy.group.next_window()),
        Key([mod], "Down", lazy.group.prev_window()),

        Key([mod], "space", lazy.next_layout()),

        Key([mod], "j", lazy.layout.up()),
        Key([mod], "k", lazy.layout.down()),

        Key([mod], "f", lazy.window.toggle_floating()),

        Key([mod], "r", lazy.spawncmd()),
        Key([mod], "u", lazy.spawn(browser)),
        Key([mod], "Return", lazy.spawn(terminal)),
        Key([mod], "BackSpace", lazy.window.kill()),

        Key([mod, "shift"], "r", lazy.restart()),
        Key([mod, "shift"], "q", lazy.shutdown()),

        Key([], "Print", lazy.spawn("scrot")),
        Key([], "Scroll_Lock", lazy.spawn(HOME + ".local/bin/i3lock -d")),
        Key([mod], "Delete", lazy.spawn("amixer set Master toggle")),
        Key([mod], "Prior", lazy.spawn("amixer set Master 5+")),
        Key([mod], "Next", lazy.spawn("amixer set Master 5-")),
        Key([mod], "Insert", lazy.spawn(HOME + ".local/bin/spotify-dbus playpause")),
        Key([mod], "End", lazy.spawn(HOME + ".local/bin/spotify-dbus next")),
        Key([mod], "Home", lazy.spawn(HOME + ".local/bin/spotify-dbus previous")),
    ]
    if DEBUG:
        keys += [Key(["mod1"], "Tab", lazy.layout.next()),
                 Key(["mod1", "shift"], "Tab", lazy.layout.previous())]
    return keys


def init_mouse():
    return [Drag([mod], "Button1", lazy.window.set_position_floating(),
                 start=lazy.window.get_position()),
            Drag([mod], "Button3", lazy.window.set_size_floating(),
                 start=lazy.window.get_size())]


def init_groups():
    def _inner(key, name):
        keys.append(Key([mod], key, lazy.group[name].toscreen()))
        keys.append(Key([mod, "shift"], key, lazy.window.togroup(name)))
        return Group(name)

    groups = [("dead_grave", "00")]
    groups += [(str(i), "0" + str(i)) for i in range(1, 10)]
    groups += [("0", "10"), ("minus", "11"), ("equal", "12")]
    return [_inner(*i) for i in groups]


def init_floating_layout():
    return layout.Floating(border_focus=BLUE)


def init_widgets():
    prompt = "{0}@{1}: ".format(os.environ["USER"], hostname)
    widgets = [
        Prompt(prompt=prompt, font="DejaVu Sans Mono", padding=10,
               background=GREY),

        TextBox(text="◤ ", fontsize=45, padding=-8, foreground=GREY,
                background=DARK_GREY),
        CurrentLayoutIcon(scale=0.6, padding=-4),

        TextBox(text=" ", padding=2),
        GroupBox(fontsize=8, padding=4, borderwidth=1, urgent_border=DARK_BLUE,
                 disable_drag=True, highlight_method="block",
                 this_screen_border=DARK_BLUE, other_screen_border=DARK_ORANGE,
                 this_current_screen_border=BLUE,
                 other_current_screen_border=ORANGE),

        TextBox(text="◤", fontsize=45, padding=-1, foreground=DARK_GREY,
                background=GREY),

        TaskList(borderwidth=0, highlight_method="block", background=GREY,
                 border=DARK_GREY, urgent_border=DARK_BLUE),

        Systray(background=GREY),
        TextBox(text="◤", fontsize=45, padding=-1,
                foreground=GREY, background=DARK_GREY),

        TextBox(text=" ⚠", foreground=BLUE, fontsize=18),
        Notify(),

        TextBox(text=" ⌚", foreground=BLUE, fontsize=18),
        Clock(format="%A %d-%m-%Y %H:%M")
    ]
    if hostname in ("spud", "saiga"):
        widgets[-2:-2] = [
            TextBox(text=" ↯", foreground=BLUE, fontsize=14),
            Battery(update_delay=2)
        ]
    if DEBUG:
        widgets += [Sep(), CurrentLayout()]
    return widgets


def init_top_bar():
    return bar.Bar(widgets=init_widgets(), size=22, opacity=1)


def init_widgets_defaults():
    return dict(font="DejaVu", fontsize=11, padding=2, background=DARK_GREY)


def init_screens(num_screens):
    for _ in range(num_screens - 1):
        screens.insert(0, Screen())


def init_layouts(num_screens):
    margin = 0
    if num_screens > 1:
        margin = 8
    layouts.extend([layout.Tile(ratio=0.5, margin=margin, border_width=1,
                                border_normal="#111111", border_focus=BLUE)])


# very hacky, much ugly
def main(qtile):
    num_screens = len(qtile.conn.pseudoscreens)
    init_screens(num_screens)
    init_layouts(num_screens)


if __name__ in ["config", "__main__"]:
    if HOME + ".local/bin" not in os.environ["PATH"]:
        os.environ["PATH"] = HOME + ".local/bin:{}".format(os.environ["PATH"])

    mod = "mod4"
    browser = "chromium-browser"
    terminal = "roxterm"
    hostname = socket.gethostname()
    cursor_warp = False

    keys = init_keys()
    mouse = init_mouse()
    groups = init_groups()
    floating_layout = init_floating_layout()
    layouts = [layout.Max()]
    screens = [Screen(top=init_top_bar())]
    widget_defaults = init_widgets_defaults()

    if DEBUG:
        layouts += [
            floating_layout, layout.Stack(), layout.Zoomy(), layout.Matrix(),
            layout.TreeTab(), layout.MonadTall(), layout.RatioTile(),
            layout.Slice('left', 192, name='slice-test', role='gnome-terminal',
                         fallback=layout.Slice('right', 256, role='gimp-dock',
                                               fallback=layout.Stack(stacks=1)))]

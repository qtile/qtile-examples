# -*- coding: utf-8 -*-
# Configuration repository: https://github.com/ramnes/qtile-config/
import os
import socket

from libqtile import bar, hook, layout
from libqtile.command import lazy
from libqtile.config import Drag, Group, Key, Screen
from libqtile.widget import (Battery, Clock, CurrentLayout, CurrentLayoutIcon,
                             GroupBox, Notify, Prompt, Sep, Spacer, Systray,
                             TaskList, TextBox)

DEBUG = os.environ.get("DEBUG")

GREY = "#222222"
DARK_GREY = "#111111"
BLUE = "#007fdf"
DARK_BLUE = "#002a4a"
ORANGE = "#dd6600"
DARK_ORANGE = "#371900"


def window_to_previous_column_or_group():
    @lazy.function
    def __inner(qtile):
        layout = qtile.current_group.layout
        group_index = qtile.groups.index(qtile.current_group)
        previous_group_name = qtile.current_group.get_previous_group().name

        if layout.name != "columns":
            qtile.current_window.togroup(previous_group_name)
        elif layout.current == 0 and len(layout.cc) == 1:
            if group_index != 0:
                qtile.current_window.togroup(previous_group_name)
        else:
            layout.cmd_shuffle_left()
    return __inner


def window_to_next_column_or_group():
    @lazy.function
    def __inner(qtile):
        layout = qtile.current_group.layout
        group_index = qtile.groups.index(qtile.current_group)
        next_group_name = qtile.current_group.get_next_group().name

        if layout.name != "columns":
            qtile.current_window.togroup(next_group_name)
        elif layout.current + 1 == len(layout.columns) and len(layout.cc) == 1:
            if group_index + 1 != len(qtile.groups):
                qtile.current_window.togroup(next_group_name)
        else:
            layout.cmd_shuffle_right()
    return __inner


def window_to_previous_screen():
    @lazy.function
    def __inner(qtile):
        i = qtile.screens.index(qtile.current_screen)
        if i != 0:
            group = qtile.screens[i - 1].group.name
            qtile.current_window.togroup(group)
    return __inner


def window_to_next_screen():
    @lazy.function
    def __inner(qtile):
        i = qtile.screens.index(qtile.current_screen)
        if i + 1 != len(qtile.screens):
            group = qtile.screens[i + 1].group.name
            qtile.current_window.togroup(group)
    return __inner


def switch_screens():
    @lazy.function
    def __inner(qtile):
        i = qtile.screens.index(qtile.current_screen)
        group = qtile.screens[i - 1].group
        qtile.current_screen.set_group(group)
    return __inner


@hook.subscribe.client_new
def set_floating(window):
    floating_types = ["notification", "toolbar", "splash", "dialog"]
    floating_roles = ["EventDialog", "Msgcompose", "Preferences"]
    floating_names = ["Terminator Preferences"]
    floating_classes = ["gcr-prompter", "gnome-screenshot",
                        "nm-connection-editor"]

    if (window.window.get_wm_type() in floating_types
        or window.window.get_wm_window_role() in floating_roles
        or window.window.get_name() in floating_names
        or window.window.get_wm_transient_for()):
        window.floating = True
        return

    try:
        if window.window.get_wm_class()[0] in floating_classes:
            window.floating = True
    except IndexError:
        pass


def init_keys():
    keys = [
        Key([mod], "Left", lazy.screen.prev_group(skip_managed=True)),
        Key([mod], "Right", lazy.screen.next_group(skip_managed=True)),

        Key([mod, "shift"], "Left", window_to_previous_column_or_group()),
        Key([mod, "shift"], "Right", window_to_next_column_or_group()),

        Key([mod, "control"], "Up", lazy.layout.grow_up()),
        Key([mod, "control"], "Down", lazy.layout.grow_down()),
        Key([mod, "control"], "Left", lazy.layout.grow_left()),
        Key([mod, "control"], "Right", lazy.layout.grow_right()),

        Key([mod, "mod1"], "Left", lazy.prev_screen()),
        Key([mod, "mod1"], "Right", lazy.next_screen()),

        Key([mod, "shift", "mod1"], "Left", window_to_previous_screen()),
        Key([mod, "shift", "mod1"], "Right", window_to_next_screen()),

        Key([mod], "t", switch_screens()),

        Key([mod], "Up", lazy.group.prev_window()),
        Key([mod], "Down", lazy.group.next_window()),

        Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
        Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),

        Key([mod], "space", lazy.next_layout()),

        Key([mod], "f", lazy.window.toggle_floating()),
        Key([mod], "s", lazy.layout.toggle_split()),

        Key([mod], "r", lazy.spawncmd()),
        Key([mod], "u", lazy.spawn(browser)),
        Key([mod], "Return", lazy.spawn(terminal)),
        Key([mod], "BackSpace", lazy.window.kill()),

        Key([mod, "shift"], "r", lazy.restart()),
        Key([mod, "shift"], "q", lazy.shutdown()),

        Key([], "Print", lazy.spawn("gnome-screenshot -i")),
        Key([mod], "Print", lazy.spawn("gnome-screenshot -p")),
        Key([], "Scroll_Lock", lazy.spawn(screenlocker)),
        Key([mod], "Delete", lazy.spawn("amixer set Master toggle")),
        Key([mod], "Prior", lazy.spawn("amixer set Master 5+")),
        Key([mod], "Next", lazy.spawn("amixer set Master 5-")),
        Key([mod], "Insert", lazy.spawn("spotify-dbus playpause")),
        Key([mod], "End", lazy.spawn("spotify-dbus next")),
        Key([mod], "Home", lazy.spawn("spotify-dbus previous")),
    ]
    if DEBUG:
        keys += [
            Key([mod], "Tab", lazy.layout.next()),
            Key([mod, "shift"], "Tab", lazy.layout.previous()),
            Key([mod, "shift"], "f", lazy.layout.flip()),
            Key([mod, "shift"], "s", lazy.group["scratch"].dropdown_toggle("term"))
        ]
    return keys


def init_mouse():
    mouse = [Drag([mod], "Button1", lazy.window.set_position_floating(),
                  start=lazy.window.get_position()),
             Drag([mod], "Button3", lazy.window.set_size_floating(),
                  start=lazy.window.get_size())]
    if DEBUG:
        mouse += [Drag([mod, "shift"], "Button1", lazy.window.set_position(),
                       start=lazy.window.get_position())]
    return mouse


def init_groups():
    def _inner(key, name):
        keys.append(Key([mod], key, lazy.group[name].toscreen()))
        keys.append(Key([mod, "shift"], key, lazy.window.togroup(name)))
        return Group(name)

    groups = [("dead_grave", "00")]
    groups += [(str(i), "0" + str(i)) for i in range(1, 10)]
    groups += [("0", "10"), ("minus", "11"), ("equal", "12")]
    groups = [_inner(*i) for i in groups]

    if DEBUG:
        from libqtile.config import DropDown, ScratchPad
        dropdowns = [DropDown("term", terminal, x=0.125, y=0.25,
                              width=0.75, height=0.5, opacity=0.8,
                              on_focus_lost_hide=True)]
        groups.append(ScratchPad("scratch", dropdowns))
    return groups


def init_floating_layout():
    return layout.Floating(border_focus=ORANGE)


def init_widgets():
    prompt = "{0}@{1}: ".format(os.environ["USER"], hostname)
    widgets = [
        Prompt(prompt=prompt, font="DejaVu Sans Mono", padding=10,
               background=GREY),

        TextBox(text="◤ ", fontsize=45, padding=-8, foreground=GREY,
                background=DARK_GREY),
        CurrentLayoutIcon(scale=0.6, padding=-4),

        Spacer(width=10),
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
        Notify(fmt=" 🔥 {}"),
        Clock(fmt=" ⌚ {}", format="%A %d-%m-%Y %H:%M")
    ]
    if os.path.isdir("/sys/module/battery"):
        widgets.insert(-1, Battery(fmt=" ⚡️ {}", update_delay=2))
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
    kwargs = dict(margin=margin, border_width=1, border_normal="#111111",
                  border_focus=BLUE, border_focus_stack=ORANGE)
    layouts.extend([
        layout.Columns(num_columns=2, grow_amount=5, **kwargs)
    ])


# very hacky, much ugly
def main(qtile):
    num_screens = len(qtile.conn.pseudoscreens)
    init_screens(num_screens)
    init_layouts(num_screens)


if __name__ in ["config", "__main__"]:
    local_bin = os.path.expanduser("~") + "/.local/bin"
    if local_bin not in os.environ["PATH"]:
        os.environ["PATH"] = "{}:{}".format(local_bin, os.environ["PATH"])

    mod = "mod4"
    browser = "google-chrome"
    terminal = "roxterm"
    screenlocker = "i3lock -d"
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
            floating_layout, layout.Zoomy(), layout.Tile(), layout.Matrix(),
            layout.TreeTab(), layout.MonadTall(margin=10), layout.RatioTile(),
            layout.Stack()
        ]

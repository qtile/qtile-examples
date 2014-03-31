# -*- coding: utf-8 -*-
import os
import socket

from libqtile.config import Key, Screen, Group
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook


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


def init_keys():
    return [Key([mod], "Left", lazy.screen.prevgroup()),
            Key([mod], "Right", lazy.screen.nextgroup()),

            Key([mod, "shift"], "Left", window_to_prev_group),
            Key([mod, "shift"], "Right", window_to_next_group),

            Key([mod], "Tab", lazy.layout.previous()),
            Key([mod, "shift"], "Tab", lazy.layout.next()),

            Key([mod], "space", lazy.nextlayout()),
            Key([mod, "shift"], "space", lazy.prevlayout()),

            Key([mod], "j", lazy.layout.up()),
            Key([mod], "k", lazy.layout.down()),

            Key([mod], "r", lazy.spawncmd()),
            Key([mod, "shift"], "c", lazy.window.kill()),
            Key([mod], "Return", lazy.spawn(term)),
            Key([mod], "l", lazy.spawn(lock)),
            Key([mod, "control"], "r", lazy.restart())]


def init_colors():
    return ["c52929",
            "ded401",
            "3a3a3a",
            "282828"]


def init_groups():
    def _inner(number):
        keys.append(Key([mod], number, lazy.group[number].toscreen()))
        keys.append(Key([mod, "shift"], number, lazy.window.togroup(number)))
        return Group(number)
    return [_inner(str(i)) for i in range(1, 10)]


def init_layouts():
    return [layout.Max(),
            layout.Tile(ratio=0.5),
            layout.Floating()]


def init_widgets():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    return [widget.Prompt(prompt=prompt, font="DejaVu Sans Mono",
                    padding=10, background=colors[2]),

            widget.TextBox(text="◤ ", fontsize=45, padding=-8,
                    foreground=colors[2], background=colors[3]),

            widget.GroupBox(fontsize=8, padding=4, borderwidth=1,
                    this_current_screen_border=colors[0]),

            widget.TextBox(text="◤", fontsize=45, padding=-1,
                    foreground=colors[3], background=colors[2]),

            widget.TaskList(borderwidth=1, background=colors[2],
                    border=colors[0], urgent_border=colors[1]),

            widget.TextBox(text="◤", fontsize=45, padding=-1,
                    foreground=colors[2], background=colors[3]),

            widget.Systray(),
            widget.TextBox(text=" (", foreground=colors[0]),
            widget.TextBox(text="↯", foreground=colors[1], fontsize=14),
            widget.Battery(update_delay=5),
            widget.TextBox(text="|", foreground=colors[0]),
            widget.TextBox(text="⌚", foreground=colors[1], fontsize=18),
            widget.Clock(fmt="%a %d-%m-%Y %H:%M"),
            widget.TextBox(text=") ", foreground=colors[0])]


def init_top_bar():
    return bar.Bar(widgets=init_widgets(), size=25)


def init_screens():
    return [Screen(top=init_top_bar())]


def init_widgets_defaults():
    return dict(font="DejaVu",
                fontsize=12,
                padding=2,
                background=colors[3])


@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True


if __name__ in ["config", "__main__"]:
    mod = "mod4"
    lock = "i3lock -d -c000000"
    term = "gnome-terminal"

    colors = init_colors()
    keys = init_keys()
    groups = init_groups()
    layouts = init_layouts()
    screens = init_screens()
    widget_defaults = init_widgets_defaults()

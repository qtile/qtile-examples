# -*- coding: utf-8 -*-
import os
import socket

from libqtile.config import Key, Screen, Group, Drag
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook


DEBUG = os.environ.get("DEBUG")


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
    keys = [Key([mod], "Left", lazy.screen.prevgroup()),
            Key([mod], "Right", lazy.screen.nextgroup()),

            Key([mod, "shift"], "Left", window_to_prev_group),
            Key([mod, "shift"], "Right", window_to_next_group),

            Key([mod], "Tab", lazy.group.next_window()),
            Key([mod, "shift"], "Tab", lazy.group.prev_window()),

            Key([mod], "space", lazy.nextlayout()),
            Key([mod, "shift"], "space", lazy.prevlayout()),

            Key([mod], "j", lazy.layout.up()),
            Key([mod], "k", lazy.layout.down()),
            Key([mod], "f", lazy.window.toggle_floating()),

            Key([mod], "r", lazy.spawncmd()),
            Key([mod], "Return", lazy.spawn(term)),
            Key([mod], "l", lazy.spawn(lock)),

            Key([mod, "shift"], "c", lazy.window.kill()),
            Key([mod, "shift"], "r", lazy.restart()),
            Key([mod, "shift"], "q", lazy.shutdown())]
    if DEBUG:
        keys += [Key(["mod1"], "Tab", lazy.layout.next()),
                 Key(["mod1", "shift"], "Tab", lazy.layout.previous())]
    return keys


def init_mouse():
    return [Drag([mod], "Button1", lazy.window.set_position_floating(),
                 start=lazy.window.get_position()),
            Drag([mod], "Button3", lazy.window.set_size_floating(),
                 start=lazy.window.get_size())]


def init_colors():
    return [["#7cfcff", "#00afff"], # cyan gradiant
            ["#323335", "#525355"], # grey gradiant
            ["#040404", "#111113"]] # darker grey gradiant


def init_groups():
    def _inner(number):
        keys.append(Key([mod], number, lazy.group[number].toscreen()))
        keys.append(Key([mod, "shift"], number, lazy.window.togroup(number)))
        return Group(number)
    return [_inner(str(i)) for i in range(1, 10)]


def init_floating_layout():
    return layout.Floating(border_focus="#7cfcff")


def init_layouts():
    return [layout.Max(),
            layout.Tile(ratio=0.5, border_focus="#00afff"),
            floating_layout]


def init_widgets():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets = [widget.Prompt(prompt=prompt, font="DejaVu Sans Mono",
                             padding=10, background=colors[1]),

               widget.TextBox(text="◤ ", fontsize=45, padding=-8,
                              foreground=colors[1], background=colors[2]),

               widget.GroupBox(fontsize=8, padding=4, borderwidth=1,
                               this_current_screen_border=colors[0]),

               widget.TextBox(text="◤", fontsize=45, padding=-1,
                              foreground=colors[2], background=colors[1]),

               widget.TaskList(borderwidth=1, background=colors[1],
                               border=colors[0], urgent_border=colors[0]),

               widget.Systray(background=colors[1]),

               widget.TextBox(text="◤", fontsize=45, padding=-1,
                              foreground=colors[1], background=colors[2]),

               widget.TextBox(text=" ↯", foreground=colors[0], fontsize=14),
               widget.Battery(update_delay=5),

               widget.TextBox(text=" ⌚", foreground=colors[0], fontsize=18),
               widget.Clock(fmt="%a %d-%m-%Y %H:%M")]
    if DEBUG:
        widgets += [widget.Sep(), widget.CurrentLayout()]
    return widgets


def init_top_bar():
    return bar.Bar(widgets=init_widgets(), size=25, opacity=0.96)


def init_screens():
    return [Screen(top=init_top_bar())]


def init_widgets_defaults():
    return dict(font="DejaVu",
                fontsize=11,
                padding=2,
                background=colors[2])


@hook.subscribe.client_new
def floating(window):
    floating_types = ['notification', 'toolbar', 'splash', 'dialog']
    transient = window.window.get_wm_transient_for()
    if window.window.get_wm_type() in floating_types or transient:
        window.floating = True


if __name__ in ["config", "__main__"]:
    mod = "mod4"
    lock = "i3lock -d -c000000"
    term = "gnome-terminal"

    colors = init_colors()
    keys = init_keys()
    mouse = init_mouse()
    groups = init_groups()
    floating_layout = init_floating_layout()
    layouts = init_layouts()
    screens = init_screens()
    widget_defaults = init_widgets_defaults()

    if DEBUG:
        layouts += [
            layout.Stack(), layout.Zoomy(), layout.Matrix(), layout.TreeTab(),
            layout.MonadTall(), layout.RatioTile(),
            layout.Slice('left', 192, name='slice-test', role='gnome-terminal',
                         fallback=layout.Slice('right', 256, role='gimp-dock',
                                            fallback=layout.Stack(stacks=1)))]

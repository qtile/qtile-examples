try:
    from libqtile.manager import Key, Group
except ImportError:
    from libqtile.config import Key, Group

from libqtile.manager import Click, Drag, Screen
from libqtile.manager import Screen, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
import os

sup = "mod4"
alt = "mod1"

keys = [
    Key(
        [alt], "Tab",
        lazy.layout.down()
    ),
    Key(
        [alt, "shift"], "Tab",
        lazy.layout.up()
    ),
    Key(
        [sup, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [sup, "control"], "j",
        lazy.layout.shuffle_up()
    ),
    Key(
        [sup], "space",
        lazy.layout.next()
    ),
    Key(
        [sup, "shift"], "space",
        lazy.layout.rotate()
    ),
    Key(
        [sup, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([sup], "Return", lazy.spawn("terminator")),
    Key([sup], "i", lazy.spawn("icedove")),
    Key([sup], "x", lazy.spawn("xchat")),
    Key([sup], "f", lazy.spawn("iceweasel")),
    Key([sup], "a", lazy.spawn("gajim")),
    Key([sup], "p", lazy.spawn("pidgin")),
    Key([sup], "d", lazy.spawn("setxkbmap -layout es -variant dvorak")),
    Key([sup], "q", lazy.spawn("setxkbmap -layout latan")),
    Key([sup], "w",      lazy.window.kill()),
    Key(
            [], "XF86AudioRaiseVolume",
            lazy.spawn("amixer -c 0 -q set Master 2dB+")
    ),
    Key(
            [], "XF86AudioLowerVolume",
            lazy.spawn("amixer -c 0 -q set Master 2dB-")
    ),

    Key([sup, "control"], "r", lazy.restart()),
    # cycle to previous group
    Key([sup], "Left", lazy.group.prevgroup()),
    # cycle to next group
    Key([sup], "Right", lazy.group.nextgroup()),

    # windows style alt-tab/alt-shift-tab
    Key([sup], "Tab", lazy.nextlayout()),
    Key([sup, "shift"], "Tab", lazy.previouslayout()),
    # PRINT SCREEN
    Key([sup], "F10", lazy.spawn("import -window root ~/screenshot.png")),
    Key([alt], "t", lazy.window.toggle_floating()),
]

groups = [
    Group("1"),
    Group("2"),
    Group("3"),
    Group("4"),
    Group("5"),
    Group("6"),
    Group("7"),
    Group("8"),
]
for i in groups:
    keys.append(
        Key([sup], i.name, lazy.group[i.name].toscreen())
    )
    keys.append(
        Key([sup, "shift"], i.name, lazy.window.togroup(i.name))
    )

# This allows you to drag windows around with the mouse if you want.
mouse = [
            Drag([sup], "Button1", lazy.window.set_position_floating(),
                         start=lazy.window.get_position()),
            Drag([sup], "Button3", lazy.window.set_size_floating(),
                         start=lazy.window.get_size()),
            Click([sup], "Button2", lazy.window.bring_to_front())
]

layouts = [
    layout.Max(),
    layout.TreeTab(sections=['Work', 'Messaging', 'Docs', 'Util', 'Other']),
    # a layout for pidgin
    layout.Slice('right', 256, name='pidgin', role='buddy_list',
         fallback=layout.Stack(stacks=2, border_width=1)),
    layout.Tile(ratio=0.35, borderwidth=1),
]

screens = [
    Screen(
        bottom = bar.Bar(
                    [
                        widget.GroupBox(fontsize=10),
                        widget.WindowName(),
                        widget.Sep(),
                        widget.CPUGraph(samples=50, line_width=1, width=50,
                                        graph_color='FF2020',
                                        fill_color='C01010'),
                        widget.MemoryGraph(samples=50, line_width=1, width=50,
                                           graph_color='0066FF',
                                           fill_color='001188'),
                        widget.NetGraph(samples=50, line_width=1,
                                        width=50, interface="eth0",
                                        graph_color='22FF44',
                                        fill_color='11AA11'),
                        widget.Systray(),
                        widget.Prompt(),
                        widget.Clock('%Y-%m-%d %a %I:%M %p', fontsize=12),
                    ],
                    25,
                ),
    ),
]


@hook.subscribe.startup
def dvorak():
    os.system("setxkbmap -layout es -variant dvorak")


def show_shortcuts():
    key_map = {"mod1": "alt", "mod4": "super"}
    shortcuts_path = "{0}/{1}".format(os.environ["HOME"], "qtile_shortcuts")
    shortcuts = open("{0}".format(shortcuts_path), 'w')
    shortcuts.write("{0:30}| {1:50}\n".format("KEYS COMBINATION", "COMMAND"))
    shortcuts.write("{0:80}\n".format("=" * 80))
    for key in keys:
        key_comb = ""
        for modifier in key.modifiers:
            key_comb += key_map.get(modifier, modifier) + "+"
        key_comb += key.key
        shortcuts.write("{0:30}| ".format(key_comb))
        cmd_str = ""
        for command in key.commands:
            cmd_str += command.name + " "
            for arg in command.args:
                cmd_str += "{0} ".format(repr(arg))
        shortcuts.write("{0:50}\n".format(cmd_str))
        shortcuts.write("{0:80}\n".format("-" * 80))
    shortcuts.close()
    return lazy.spawn("xterm -wf -e less {0}".format(shortcuts_path))


def window_sorter(win):
    patterns = (
        ('Gajim', 'Messaging'),
        ('XChat', 'Messaging'),
        ('Icedove', 'Messaging'),
        ('pidgin', 'Messaging'),
        ('Vimperator', 'Util'),
        ('Krusader', 'Util'),
        ('playout', 'Work'),
        ('lifia', 'Work'),
        )
    for k, v in patterns:
        if k in win.name:
            return v
    return 'Other'


@hook.subscribe.client_new
def dialogs(window):
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True

# More shortcuts
keys.append(Key([alt], "r", lazy.layout.sort_windows(window_sorter)))
keys.append(Key([sup], "h", show_shortcuts()))
keys.append(Key([sup], "l", lazy.spawn("xscreensaver-command -lock")))
keys.append(Key([sup], "s", lazy.spawn("xscreensaver -no-splash")))

main = None
follow_mouse_focus = True
cursor_warp = False
floating_layout = layout.Floating()
mouse = ()

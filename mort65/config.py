# coding=utf-8
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

from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.config import ScratchPad, DropDown
from libqtile.command import lazy, Client
from libqtile import layout, bar, widget, hook
import os
import re
import subprocess

mod = "mod4"
term = "/usr/bin/urxvt"
home = os.path.expanduser('~')
client = Client()

cls_grp_dict = {
    "luakit": "2", "Firefox": "2", "Opera": "2", "Google-chrome": "2",
    "Chromium": "2", "Vivaldi-stable": "2", "Midori": "2", "Dillo": "2",
    "Netsurf-gtk3": "2", "QupZilla": "2", "Uget-gtk": "2", "Tor Browser": "2",
    "Waterfox": "2", "UXTerm": "3", "URxvt": "3", "Terminator": "3",
    "Urxvt-tabbed": "3", "Urxvt": "3", "mlterm": "3", "Lxterminal": "3",
    "XTerm": "3", "Pcmanfm": "4", "Thunar": "4", "dolphin": "4", "Caja": "4",
    "Catfish": "4", "Zathura": "5", "libreoffice-writer": "5", "libreoffice": "5",
    "Leafpad": "5", "kate": "5", "Pluma": "5", "Mousepad": "5",
    "kwrite": "5", "Geany": "5", "Gedit": "5", "Code": "5",
    "Atom": "5", "Gimp": "6", "Gthumb": "6", "org.kde.gwenview": "6",
    "Ristretto": "6", "lximage-qt": "6", "Eom": "6", "Gpicview": "6",
    "vlc": "7", "xv/mplayer": "7", "Clementine": "7", "MPlayer": "7",
    "smplayer": "7", "mpv": "7", "Gnome-mpv": "7", "Rhythmbox": "7",
    "Pragha": "7", "Steam": "8", "Wine": "8", "Zenity": "8",
    "PlayOnLinux": "8", "VirtualBox": "9", "okular": "9", "calibre": "9",
    "octopi": "9", "Pamac-updater": "9", "Pamac-manager": "9", "Lxtask": "9",
    "Dukto": "9", "QuiteRss": "9", "Filezilla": "9",
}
role_grp_dict = {
    "browser": "2", "gimp-image-window": "5",
}

group_labels = [
    "🏠", "🌎", "🐚",
    "📁", "📃", "📷",
    "📺", "🎮", "🌸",
    "🌑",
]

group_names = [
    "1", "2", "3",
    "4", "5", "6",
    "7", "8", "9",
    "0",
]

group_exclusives = [
    False, False, False,
    False, False, False,
    False, False, False,
    False,
]
group_persists = [
    True, True, True,
    True, True, True,
    True, True, True,
    True,
]
group_inits = [
    True, True, True,
    True, True, True,
    True, True, True,
    True,
]

group_layouts = [
    "tile", "max", "monadwide",
    "monadtall", "stack", "zoomy",
    "max", "max", "columns",
    "bsp",
]

group_matches = [
    None,
    [Match(wm_class=[
        "luakit", "Firefox", "Opera", "Google-chrome",
        "Chromium", "Vivaldi-stable", "Midori",
        "Dillo", "Netsurf-gtk3", "QupZilla",
        "Uget-gtk", "Tor Browser", "Waterfox",
    ], role=["browser"]), ],

    [Match(wm_class=[
        "UXTerm", "URxvt", "Terminator",
        "Urxvt-tabbed", "Urxvt",
        "XTerm", "mlterm", "Lxterminal",
    ]), ],

    [Match(wm_class=[
        "Pcmanfm", "Thunar", "dolphin",
        "Caja", "Catfish",
    ]), ],

    [Match(wm_class=[
        "Zathura", "libreoffice-writer", "libreoffice",
        "Leafpad", "kate", "Pluma", "Mousepad", "kwrite",
        "Geany", "Gedit", "Code", "Atom",
    ], ), ],

    [Match(wm_class=[
        "Gimp", "Gthumb", "org.kde.gwenview",
        "Ristretto", "lximage-qt", "Eom",
        "Gpicview",
    ], role=["gimp-image-window"]), ],

    [Match(wm_class=[
        "vlc", "xv/mplayer", "Clementine",
        "MPlayer", "smplayer", "mpv",
        "Gnome-mpv", "Rhythmbox", "Pragha",
    ]), ],

    [Match(wm_class=[
        "Steam", "Wine", "Zenity",
        "PlayOnLinux",
    ]), ],

    [Match(wm_class=[
        "VirtualBox", "okular", "calibre",
        "octopi", "Pamac-updater",
        "Pamac-manager", "Lxtask",
        "Dukto", "QuiteRss",
        "Filezilla",
    ]), ],
    None,
]


def regex(name):
    return r'.*(^|\s|\t|\/)' + name + r'(\s|\t|$).*'


def window_to_prev_group():
    @lazy.function
    def __inner(qtile):
        if qtile.currentWindow is not None:
            index = qtile.groups.index(qtile.currentGroup)
            if index > 0:
                qtile.currentWindow.togroup(qtile.groups[index - 1].name)
            else:
                qtile.currentWindow.togroup(qtile.groups[len(qtile.groups) - 2].name)

    return __inner


def window_to_next_group():
    @lazy.function
    def __inner(qtile):
        if qtile.currentWindow is not None:
            index = qtile.groups.index(qtile.currentGroup)
            if index < len(qtile.groups) - 2:
                qtile.currentWindow.togroup(qtile.groups[index + 1].name)
            else:
                qtile.currentWindow.togroup(qtile.groups[0].name)

    return __inner


def window_to_prev_screen():
    @lazy.function
    def __inner(qtile):
        if qtile.currentWindow is not None:
            index = qtile.screens.index(qtile.currentScreen)
            if index > 0:
                qtile.currentWindow.togroup(qtile.screens[index - 1].group.name)
            else:
                qtile.currentWindow.togroup(qtile.screens[len(qtile.screens) - 1].group.name)

    return __inner


def window_to_next_screen():
    @lazy.function
    def __inner(qtile):
        if qtile.currentWindow is not None:
            index = qtile.screens.index(qtile.currentScreen)
            if index < len(qtile.screens) - 1:
                qtile.currentWindow.togroup(qtile.screens[index + 1].group.name)
            else:
                qtile.currentWindow.togroup(qtile.screens[0].group.name)

    return __inner


def go_to_next_group():
    @lazy.function
    def __inner(qtile):
        index = qtile.groups.index(qtile.currentGroup)
        if index < len(qtile.groups) - 2:
            qtile.groups[index + 1].cmd_toscreen()
        else:
            qtile.groups[0].cmd_toscreen()

    return __inner


def go_to_prev_group():
    @lazy.function
    def __inner(qtile):
        index = qtile.groups.index(qtile.currentGroup)
        if index > 0:
            qtile.groups[index - 1].cmd_toscreen()
        else:
            qtile.groups[len(qtile.groups) - 2].cmd_toscreen()

    return __inner


def find_or_run(app, classes=(), group="", processes=()):
    if not processes:
        processes = [regex(app.split('/')[-1])]

    def __inner(qtile):
        if classes:
            for window in qtile.windowMap.values():
                for c in classes:
                    if window.group and window.match(wmclass=c):
                        qtile.currentScreen.setGroup(window.group)
                        window.group.focus(window, False)
                        return
        if group:
            lines = subprocess.check_output(["/usr/bin/ps", "axw"]).decode("utf-8").splitlines()
            ls = [line.split()[4:] for line in lines][1:]
            ps = [' '.join(l) for l in ls]
            for p in ps:
                for process in processes:
                    if re.match(process, p):
                        qtile.groupMap[group].cmd_toscreen()
                        return
        subprocess.Popen(app.split())

    return __inner


def to_urgent():
    def __inner(qtile):
        cg = qtile.currentGroup
        for group in qtile.groupMap.values():
            if group == cg:
                continue
            if len([w for w in group.windows if w.urgent]) > 0:
                qtile.currentScreen.setGroup(group)
                break

    return __inner


def get_cur_grp_name():
    return client.group.info()['name']


date_command = ["/usr/bin/date", "+%a %D"]


def get_date():
    return '📆 ' + subprocess.check_output(date_command).decode('utf-8').strip()


def get_time():
    return ' ⏰ ' + subprocess.check_output(['/usr/bin/date', '+%I:%M %p']).decode('utf-8').strip()


def get_datetime():
    return get_date() + get_time()


keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "h", lazy.layout.left()),

    # Move windows up or down in current stack
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),

    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),

    # Switch window focus to other pane(s) of stack
    Key(["mod1"], "Tab", lazy.layout.next()),
    Key(["mod1"], "space", lazy.layout.previous()),

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "shift"], "f", lazy.window.toggle_floating()),

    Key([mod, "shift"], "Left", window_to_prev_group()),
    Key([mod, "shift"], "Right", window_to_next_group()),

    Key([mod], "Left", go_to_prev_group()),
    Key([mod], "Right", go_to_next_group()),

    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),

    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),

    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),

    Key([mod], "m",
        lazy.layout.maximize(),
        ),

    Key([mod], "n",
        lazy.layout.normalize(),
        ),

    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),

    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

    # Swap panes of split stack
    Key([mod, "shift"], "space",
        lazy.layout.rotate()
        ),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(term)),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "space", lazy.prev_layout()),
    Key([mod], "x", lazy.window.kill()),

    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "Pause", lazy.shutdown()),
    Key([mod, "shift"], "Scroll_Lock", lazy.spawn("/usr/bin/slock")),
    Key([mod, "shift", "control"], "Print", lazy.spawn("/usr/bin/systemctl -i suspend")),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "g", lazy.switchgroup()),

    # Applications
    Key([mod], "d", lazy.spawn("/usr/bin/rofi -modi run,drun -show drun run")),
    Key([mod], "Delete", lazy.function(find_or_run("/usr/bin/lxtask", ("Lxtask",),
                                                   cls_grp_dict["Lxtask"]))),
    Key([mod], "f", lazy.function(find_or_run("/usr/bin/catfish", ("Catfish",),
                                              cls_grp_dict["Catfish"], ("^/usr/bin/python /usr/bin/catfish$",)))),
    Key([mod], "e", lazy.function(find_or_run("/usr/bin/leafpad",
                                              ("Leafpad", "Mousepad", "Pluma"), cls_grp_dict["Leafpad"],
                                              (regex("leafpad"),
                                               regex("mousepad"), regex("pluma"))))),
    Key([mod, "shift"], "e", lazy.function(find_or_run("/usr/bin/geany", ("Geany", "kate"),
                                                       cls_grp_dict["Geany"], (regex("geany"), regex("kate"))))),
    Key([mod], "Home", lazy.function(find_or_run("/usr/bin/pcmanfm", ("Pcmanfm", "Thunar", "dolphin"),
                                                 cls_grp_dict["Pcmanfm"],
                                                 (regex("pcmanfm"), regex("thunar"), regex("dolphin"))))),
    Key([mod, "shift"], "Home", lazy.function(find_or_run(term + " -e /usr/bin/ranger", (),
                                                          cls_grp_dict["Urxvt"]))),
    Key([mod], "p", lazy.function(find_or_run("/usr/bin/pragha", ("Pragha", "Clementine"),
                                              cls_grp_dict["Pragha"], [regex("pragha"), regex("clementine")]))),
    Key([mod], "c", lazy.function(find_or_run(term + " -e /usr/bin/cmus", (),
                                              cls_grp_dict["Urxvt"]))),
    Key([mod], "w", lazy.function(find_or_run("/usr/bin/firefox", ("Firefox", "Chromium", "Vivaldi-stable"),
                                              cls_grp_dict["Firefox"],
                                              ("/usr/lib/firefox/firefox", "/usr/lib/chromium/chromium",
                                               "/opt/vivaldi/vivaldi-bin")))),
    Key([mod, "shift"], "w", lazy.function(find_or_run(home +
                                                       "/Apps/Internet/tor-browser_en-US/Browser/start-tor-browser "
                                                       "--detach ", ("Tor Browser",), cls_grp_dict["Tor Browser"],
                                                       ("\./firefox",)))),
    Key([mod], "i", lazy.function(find_or_run("/usr/bin/pamac-manager", ["Pamac-manager"],
                                              cls_grp_dict["Pamac-manager"]))),
    Key([], "F10", lazy.function(to_urgent())),

    # Media player controls
    Key([], "XF86AudioPlay", lazy.spawn("/usr/bin/playerctl play")),
    Key([], "XF86AudioPause", lazy.spawn("/usr/bin/playerctl pause")),
    Key([], "XF86AudioNext", lazy.spawn("/usr/bin/playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("/usr/bin/playerctl previous")),

    # Screenshot
    Key([], "Print", lazy.spawn("/usr/bin/scrot " + home + "/Pictures/Screenshots/screenshot_%Y_%m_%d_%H_%M_%S.png")),

    # Pulse Audio controls
    Key([], "XF86AudioMute",
        lazy.spawn("/usr/bin/pactl set-sink-mute alsa_output.pci-0000_00_1b.0.analog-stereo toggle")),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("/usr/bin/pactl set-sink-volume alsa_output.pci-0000_00_1b.0.analog-stereo -5%")),
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("/usr/bin/pactl set-sink-volume alsa_output.pci-0000_00_1b.0.analog-stereo +5%"))
]

layout_style = {
    'font': 'ubuntu',
    'margin': 0,
    'border_width': 1,
    'border_normal': '000000',
    'border_focus': '0000FF',

}

layouts = [
    layout.Tile(**layout_style),
    layout.Columns(num_columns=2, autosplit=True, **layout_style),
    layout.Stack(num_stacks=1, **layout_style),
    layout.MonadTall(**layout_style),
    layout.MonadWide(**layout_style),
    layout.Bsp(**layout_style),
    # layout.Matrix(**layout_style),
    layout.Zoomy(**layout_style),
    layout.Max(**layout_style),
    # layout.Floating(**layout_style),
]

groups = []

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            matches=group_matches[i],
            exclusive=group_exclusives[i],
            layout=group_layouts[i].lower(),
            persist=group_persists[i],
            init=group_inits[i],
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

groups.append(
    ScratchPad("scratchpad", [
        # define a drop down terminal.
        # it is placed in the upper third of screen by default.
        DropDown("term", "/usr/bin/termite", opacity=0.88, height=0.55, width=0.80, ),

        # define another terminal exclusively for qshell at different position
        DropDown("qshell", "/usr/bin/termite -e qshell",
                 x=0.05, y=0.4, width=0.9, height=0.6, opacity=0.9,
                 on_focus_lost_hide=True)
    ]), )

keys.extend([
    # Scratchpad
    # toggle visibiliy of above defined DropDown named "term"
    Key([], 'F12', lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([], 'F11', lazy.group['scratchpad'].dropdown_toggle('qshell')),
])

widget_defaults = dict(
    font='ubuntu bold',
    fontsize=11,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.9, foreground="EFEFEF", ),
                widget.GenPollText(func=get_cur_grp_name, update_interval=0.5, foreground='EFEFEF', padding=1, ),
                widget.GroupBox(active='F6F6F6', inactive='968F92',
                                this_current_screen_border='00BCD4',
                                this_screen_border='00BCD4',
                                highlight_method='line',
                                highlight_color=['1A2024', '060A0F'],
                                fontsize=12,
                                ),
                widget.Prompt(fontsize=12, cursor_color='FFFFFF', foreground='FDF3A9', background='271B1B'),
                widget.WindowName(foreground='7AA0BC', ),
                widget.GenPollText(func=get_datetime, update_interval=1, foreground='B1D0FF', ),
                widget.Systray(),
            ],
            20,
            background=['1A2024', '060A0F'],
            opacity=0.96,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

floating_layout = layout.Floating(float_rules=[
    {"role": "EventDialog"},
    {"role": "Msgcompose"},
    {"role": "Preferences"},
    {"role": "pop-up"},
    {"role": "prefwindow"},
    {"role": "task_dialog"},
    {"role": "browser"},
    {"wname": "Module"},
    {"wname": "Terminator Preferences"},
    {"wname": "Search Dialog"},
    {"wname": "Goto"},
    {"wname": "IDLE Preferences"},
    {"wname": "Sozi"},
    {"wname": "Create new database"},
    {"wname": "Preferences"},
    {"wname": "File Transfer"},
    {"wname": 'branchdialog'},
    {"wname": 'pinentry'},
    {"wname": 'confirm'},
    {"wmclass": 'dialog'},
    {"wmclass": 'download'},
    {"wmclass": 'error'},
    {"wmclass": 'file_progress'},
    {"wmclass": 'notification'},
    {"wmclass": 'splash'},
    {"wmclass": 'toolbar'},
    {"wmclass": 'confirmreset'},
    {"wmclass": 'makebranch'},
    {"wmclass": 'maketag'},
    {"wmclass": 'Dukto'},
    {"wmclass": 'Guake'},
    {"wmclass": 'Tilda'},
    {"wmclass": 'yakuake'},
    {"wmclass": 'Xfce4-appfinder'},
    {"wmclass": "GoldenDict"},
    {"wmclass": "Synapse"},
    {"wmclass": "Pamac-updater"},
    {"wmclass": "TelegramDesktop"},
    {"wmclass": "Galculator"},
    {"wmclass": "notify"},
    {"wmclass": "Lxappearance"},
    {"wmclass": "Nitrogen"},
    {"wmclass": "Oblogout"},
    {"wmclass": "Pavucontrol"},
    {"wmclass": "VirtualBox"},
    {"wmclass": "Skype"},
    {"wmclass": "Steam"},
    {"wmclass": "nvidia-settings"},
    {"wmclass": "Eog"},
    {"wmclass": "Rhythmbox"},
    {"wmclass": "obs"},
    {"wmclass": "Gufw.py"},
    {"wmclass": "Catfish"},
    {"wmclass": "libreoffice-calc"},
    {"wmclass": "LibreOffice 3.4"},
    {"wmclass": 'ssh-askpass'},
    {"wmclass": "Mlconfig"},
    {"wmclass": "Termite"},
])
auto_fullscreen = True
focus_on_window_activation = "smart"

floating_types = ["notification", "toolbar", "splash", "dialog",
                  "utility", "menu", "dropdown_menu", "popup_menu", "tooltip,dock",
                  ]


@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True


@hook.subscribe.client_managed
def go_to_group(window):
    if (window.window.get_wm_class()[1] in cls_grp_dict.keys()
            or window.window.get_wm_window_role() in role_grp_dict.keys()):
        window.group.cmd_toscreen()


# Qtile startup commands, not repeated at qtile restart
@hook.subscribe.startup_once
def autostart():
    from datetime import datetime
    try:
        subprocess.call([home + '/.config/qtile/autostart.sh'])
    except Exception as e:
        with open('qtile_log', 'a+') as f:
            f.write(
                datetime.now().strftime('%Y-%m-%dT%H:%M') +
                + ' ' + str(e) + '\n')

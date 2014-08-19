# -*- coding: utf-8 -*-

import re
import json
import socket

from datetime import datetime

from libqtile.config import Key, Click, Drag, Screen, Group, Match, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget  # , hook
from subprocess import call

from libqtile.dgroups import simple_key_binder
from libqtile import hook

# reconfigure screens
call("setup_screens")


# Utils
# ------

def to_urgent(qtile):
    cg = qtile.currentGroup
    for group in qtile.groupMap.values():
        if group == cg:
            continue
        if len([w for w in group.windows if w.urgent]) > 0:
            qtile.currentScreen.setGroup(group)
            return


def switch_to(name):
    def callback(qtile):
        for window in qtile.windowMap.values():
            if window.group and window.match(wname=name):
                qtile.currentScreen.setGroup(window.group)
                window.group.focus(window, False)
                break
    return callback


class SwapGroup(object):
    def __init__(self, group):
        self.group = group
        self.last_group = None

    def group_by_name(self, groups, name):
        for group in groups:
            if group.name == name:
                return group

    def __call__(self, qtile):
        group = self.group_by_name(qtile.groups, self.group)
        cg = qtile.currentGroup
        if cg != group:
            qtile.currentScreen.setGroup(group)
            self.last_group = cg
        elif self.last_group:
            qtile.currentScreen.setGroup(self.last_group)


# fireipc jango helper
# https://github.com/Roger/FireIPC/
def fipc_jango(command):
    sock = socket.socket()
    sock.connect(("localhost", 61155))
    # data = json.loads(sock.recv(1024))
    # print data
    msg = json.dumps({"to": "fireipc/fijango", "command": command})
    sock.send(msg + "\n0")
    sock.close()

#   Key Bindings
# ----------------

mod = 'mod4'
keys = [
    # Movement
    Key([mod], "h", lazy.screen.prevgroup(skip_managed=True)),
    Key([mod], "l", lazy.screen.nextgroup(skip_managed=True)),
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    Key([mod, "shift"], "k", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up()),

    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),

    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),

    Key([mod, "shift"], "space", lazy.layout.flip()),
    # Key([mod, "shift"], "space", lazy.layout.rotate()),


    Key([mod], "Tab", lazy.layout.previous()),
    Key([mod, "shift"], "Tab", lazy.layout.next()),

    Key([mod], "f", lazy.window.toggle_floating()),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen()),

    Key([mod], "space", lazy.nextlayout()),

    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    # add/remove layout parts
    Key([mod, "shift"], "v", lazy.layout.add()),
    Key([mod, "control"], "v", lazy.layout.remove()),

    # size
    Key([mod, "shift"], "Right", lazy.layout.increase_ratio()),
    Key([mod, "shift"], "Left", lazy.layout.decrease_ratio()),

    Key([mod], "w", lazy.window.kill()),
    Key([mod], "F2", lazy.spawn(
        "dmenu_run -p run -fn 'terminous-13' -nb '#202020' -nf '#ffffff'")),
    Key([mod], "r", lazy.spawncmd("Run")),

    # Key([mod], "c", lazy.widget.CLIPBOARD.toggle_clipboard()),


    # imgbin/pastebin
    Key([mod], "s", lazy.spawn("imgurscropt all edit")),
    Key([mod, 'shift'], "s", lazy.spawn("imgurscropt window edit")),
    Key([mod], "p", lazy.spawn("paste_clipboard")),
    Key([mod, 'shift'], "p", lazy.spawn("paste_clipboard bash")),
    Key([mod], "z", lazy.spawn("scroting")),
    # Key([mod, 'shift'], "z", lazy.spawn("scroting window")),

    # suspend
    Key([mod, 'shift'], "z", lazy.spawn(
        "dbus-send --dest=org.freedesktop.PowerManagement "
        "/org/freedesktop/PowerManagement "
        "org.freedesktop.PowerManagement.Suspend")),

    # move to
    Key([mod], "g", lazy.togroup()),

    Key([mod], "q", lazy.findwindow()),

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
    # Key(["shift"], "XF86AudioMute",
    Key([mod], "p",
        # lazy.function(lambda q: fipc_jango("pause"))),
        lazy.spawn("mpc toggle")),

    # replace qtile with awesome, only to test stuff
    Key([mod, "control"], "a", lazy.execute("/usr/bin/awesome", ("awesome",))),
    # restart qtile
    Key([mod, "control"], "r", lazy.restart()),

    # fast switches
    Key([mod], "t", lazy.function(switch_to("Gajim"))),

    Key([], "F12", lazy.function(SwapGroup('h4x'))),
    Key(['shift'], "F12", lazy.function(to_urgent)),
]

#   Floating Drag
# ------------------

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

#    Groups
# -------------

groups = [
    Group('im', init=False, persist=False,
          matches=[Match(wm_instance_class=['im'])],
          position=2, exclusive=True),

    # first group that hold the terminals
    Group('h4x', exclusive=True,
          matches=[Match(wm_class=['URxvt', 'Qterminal', 'st-256color'])],
          position=1
          ),

    # the next groups do not auto start, only appears if the rule is matched
    Group('design', persist=False, init=False,  # layout='gimp',
          matches=[Match(wm_class=['Gimp'])]
          ),

    # Max Groups
    # --------------
    Group('www', init=False, persist=False, exclusive=True, matches=[
        Match(wm_class=['Chromium-browser', 'Minefield', 'Firefox'],
              role=['browser'])
        ], position=3),
    Group('mail', init=False, persist=False,
          matches=[Match(wm_class=['Claws-mail', 'Thunderbird'])]
          ),
    Group('kp', init=False, persist=False,
          matches=[Match(wm_class=['Keepassx'])]
          ),

    # Group('anim', init=False, persist=False, exclusive=True, matches=[
    #     Match(wm_class=['Synfigstudio'])
    #     ], position=9),

    # starts mplayer in the second screen if exists, else current
    Group("Mplayer", persist=False, init=False, screen_affinity=1,
          matches=[Match(wm_class=["MPlayer"])]
          ),

    # persist this group to make qtile tests less painfull
    Group('Xephyr', init=False,
          matches=[Match(wm_class=['Xephyr'])]
          ),

    # Tile Groups
    # --------------
    Group('emesene', init=False, persist=False, layout='tile',
          matches=[Match(wm_class=['emesene'])],
          layout_opts={"ratio": 0.25, "master_match": Match(role=['main'])},
          ),
    Group('steam', init=False, persist=False, layout='tile',
          matches=[Match(wm_class=['Steam'])],
          # set the Friends window as master and ratio 0.20
          layout_opts={"ratio": 0.20,
                       "master_match": Match(title=['Friends'])},
          position=4, exclusive=True,
          ),
    # Group('im', init=False, persist=False, layout='tile',
    #     matches=[Match(wm_class=['Gajim.py'])],
    #     # set the roster as master window and ratio 0.20
    #     layout_opts={"ratio": 0.20, "master_match": Match(role=['roster'])},
    #     position=2, exclusive=True,
    #     ),
    ]

# dgroup rules that not belongs to any group
dgroups_app_rules = [
    # Everything i want to be float, but don't want to change group
    Rule(Match(title=['nested', 'gscreenshot'],
               wm_class=['Guake.py', 'Exe', 'Onboard', 'Florence',
                         'Plugin-container', 'Terminal', 'Gpaint',
                         'Kolourpaint', 'Wrapper', 'Gcr-prompter',
                         'Ghost', 'feh', 'Gnuplot', 'Pinta',
                         re.compile('Gnome-keyring-prompt.*?')],
               ),
         float=True, intrusive=True),

    # floating windows
    Rule(Match(wm_class=['Synfigstudio', 'Wine', 'Xephyr', 'postal2-bin'],
               # title=[re.compile('[a-zA-Z]*? Steam'),
               #        re.compile('Steam - [a-zA-Z]*?')]
               ),
         float=True),

    # static windows (unmanaged)
    # Rule(Match(wm_class=["XTerm"]), static=True),
    # Rule(Match(net_wm_pid=["XTerm"]), float=True),
    ]

# auto bind keys to dgroups mod+1 to 9
dgroups_key_binder = simple_key_binder(mod)


#   Layouts Config
# -------------------

# Layout Theme
layout_theme = {
    "border_width": 2,
    "margin": 3,
    "border_focus": "#005F0C",
    "border_normal": "#555555"
    }

layouts = [
    layout.Max(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Stack(stacks=2, **layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
]

floating_layout = layout.Floating(**layout_theme)

#   Screens Config
# ------------------
flat_theme = {"bg_dark": ["#606060", "#000000"],
              "bg_light": ["#707070", "#303030"],
              "font_color": ["#ffffff", "#cacaca"],

              # groupbox
              "gb_selected": ["#7BA1BA", "#215578"],
              "gb_urgent": ["#ff0000", "#820202"]
              }

gloss_theme = {"bg_dark": ["#505050",
                           "#303030",
                           "#202020",
                           "#101010",
                           "#202020",
                           "#303030",
                           "#505050"],
               "bg_light": ["#707070",
                            "#505050",
                            "#505050",
                            "#505050",
                            "#505050",
                            "#707070"],
               "font_color": ["#ffffff", "#ffffff", "#cacaca", "#707070"],

               # groupbox
               "gb_selected": ["#707070",
                               "#505050",
                               "#404040",
                               "#303030",
                               "#404040",
                               "#505050",
                               "#707070"],
               "gb_urgent": ["#ff0000",
                             "#820202",
                             "#820202",
                             "#820202",
                             "#820202",
                             "#ff0000"
                             ]
               }
theme = gloss_theme

# Widgets Theme
widget_defaults = dict(background=theme["bg_light"],
                       opacity=0.9,
                       border_color="#6f6f6f",
                       fontshadow="#000000",
                       foreground=theme["font_color"],
                       fontsize=14,
                       font="Anonymous Pro",
                       )
top_bar = bar.Bar([
    widget.TextBox(text=u"◥", fontsize=40, padding=-1,
                   font="Arial",
                   foreground=theme["bg_dark"]),
    widget.GroupBox(borderwidth=0, padding=3, margin=0,
                    highlight_method="block", rounded=False,
                    this_current_screen_border=theme["gb_selected"],
                    urgent_border=theme["gb_urgent"],
                    active=theme["font_color"],
                    background=theme["bg_dark"],
                    ),
    widget.TextBox(text=u"◣", fontsize=40, padding=-1,
                   font="Arial",
                   foreground=theme["bg_dark"]),

    widget.DF(partition="/"),
    widget.Prompt(),
    widget.Clipboard(),
    widget.Clipboard(selection="PRIMARY"),

    widget.TextBox(text="", name="info"),

    widget.TextBox(text=u"◥", fontsize=40, padding=-1,
                   font="Arial",
                   foreground=theme["bg_dark"]),
    widget.TaskList(borderwidth=2, padding=2,
                    margin=2, highlight_method="border",
                    border=theme["gb_selected"],
                    background=theme["bg_dark"],
                    ),

    widget.Countdown(date=datetime(2014, 8, 22, 21, 0),
                     background=theme["bg_dark"],
                     final=False,
                     format="\xef\x84\x9b {D}d {H}h {M}m"),

    # system usage
    widget.CPUGraph(core=0, width=21, line_width=2,
                    graph_color='#0066FF',
                    fill_color=['#0066FF', '#001111'],
                    margin_x=0, border_width=1,
                    background=theme["bg_dark"],
                    ),
    widget.CPUGraph(core=1, width=21, line_width=2,
                    graph_color='#0066FF',
                    fill_color=['#0066FF', '#001111'],
                    margin_x=0, border_width=1,
                    background=theme["bg_dark"],
                    ),
    widget.MemoryGraph(width=42, line_width=2,
                       graph_color='#22BB44',
                       fill_color=['#11FF11', "#002200"],
                       border_width=1,
                       background=theme["bg_dark"],
                       ),
    widget.SwapGraph(width=42, line_width=2,
                     graph_color='#CC2020',
                     fill_color=['#FF1010', '#221010'],
                     border_width=1,
                     background=theme["bg_dark"],
                     ),

    widget.TextBox(text=u" ", background=theme["bg_dark"]),
    widget.TextBox(text=u"◣", fontsize=40, padding=-1,
                   font="Arial",
                   foreground=theme["bg_dark"]),

    widget.Volume(update_interval=0.2, emoji=True),

    widget.Systray(icon_size=14),
    widget.Clock('%d-%m-%y %H:%M', fontsize=13, padding=6),
    ], size=22, opacity=0.9)

screens = [
    Screen(top=top_bar),
]


def detect_screens(qtile):
    """
    Detect if a new screen is plugged and reconfigure/restart qtile
    """

    def setup_monitors(action=None, device=None):
        """
        Add 1 group per screen
        """

        if action == "change":
            # setup monitors with xrandr
            # call("setup_screens")
            lazy.restart()

        nbr_screens = len(qtile.conn.pseudoscreens)
        for i in xrange(0, nbr_screens-1):
            groups.append(Group('h%sx' % (i+5), persist=False))
    setup_monitors()

    import pyudev

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('drm')
    monitor.enable_receiving()

    # observe if the monitors change and reset monitors config
    observer = pyudev.MonitorObserver(monitor, setup_monitors)
    observer.start()


# import subprocess

# @hook.subscribe.client_urgent_hint_changed
# def on_urgent(client):
#     subprocess.Popen(["compton_invert", "%s" % client.window.wid])

@hook.subscribe.client_new
def new_client(client):
    if client.window.get_wm_class()[0] == "screenkey":
        client.static(0)


def main(qtile):
    detect_screens(qtile)

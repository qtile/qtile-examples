import re
import json
import socket
from subprocess import call

# reconfigure screens
call("setup_screens")

from libqtile.config import Key, Click, Drag, Screen, Group, Match, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget

from libqtile.dgroups import simple_key_binder

# Utils
#-------

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
    """
    Switch from/to current group to group
    """
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
def fipc_jango(command):
    sock = socket.socket()
    sock.connect(("localhost", 61155))
    #data = json.loads(sock.recv(1024))
    #print data
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
    #Key([mod, "shift"], "space", lazy.layout.rotate()),


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
    Key([mod], "r", lazy.spawncmd("Run:")),


    # imgbin/pastebin
    Key([mod], "s", lazy.spawn("imgurscropt all edit")),
    Key([mod, 'shift'], "s", lazy.spawn("imgurscropt window edit")),
    Key([mod], "p", lazy.spawn("paste_clipboard")),
    Key([mod, 'shift'], "p", lazy.spawn("paste_clipboard bash")),
    Key([mod], "z", lazy.spawn("scroting")),
    #Key([mod, 'shift'], "z", lazy.spawn("scroting window")),

    # suspend
    Key([mod, 'shift'], "z", lazy.spawn(
        "dbus-send --dest=org.freedesktop.PowerManagement "\
        "/org/freedesktop/PowerManagement "\
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
    Key(["shift"], "XF86AudioRaiseVolume",
        lazy.function(lambda q: fipc_jango("next"))),
    Key(["shift"], "XF86AudioLowerVolume",
        lazy.spawn("mpc prev")),
    # No mute key @notebook
    #Key(["shift"], "XF86AudioMute",
    Key([mod], "p",
        lazy.function(lambda q: fipc_jango("pause"))),

    # replace qtile with awesome, only to test stuff
    Key([mod, "control"], "a", lazy.execute("/usr/bin/awesome", ("awesome",))),
    # restart qtile
    Key([mod, "control"], "r", lazy.restart()),

    # fast switches
    Key([mod], "t", lazy.function(switch_to("Gajim"))),

    # use like a cheap guake replacement
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
      # first group that hold the terminals
      Group('h4x', exclusive=True,
          matches=[Match(wm_class=['Qterminal', 'Terminator'])]
          ),

      # the next groups do not auto start, only appears if the rule is matched
      Group('design', persist=False, init=False, layout='gimp',
          matches=[Match(wm_class=['Gimp'])]
          ),

      # Max Groups
      # --------------
      Group('www', init=False, persist=False, exclusive=True, matches=[
          Match(wm_class=['Chromium-browser', 'Minefield', 'Firefox'],
                role=['browser'])
          ]),
      Group('mail', init=False, persist=False,
          matches=[Match(wm_class=['Claws-mail', 'Thunderbird'])]
          ),
      Group('keepassx', init=False, persist=False, layout="stack",
          matches=[Match(wm_class=['Keepassx'])]
          ),

      # starts mplayer in the second screen if exists, else current
      Group("Mplayer", persist=False, init=False, screen_affinity=1,
          matches=[Match(wm_class=["MPlayer"])]
          ),

      # Persist this group to make qtile tests less painfull
      Group('Xephyr', init=False,
          matches=[Match(wm_class=['Xephyr'])]
          ),

      # Tile Groups
      # --------------
      Group('emesene', init=False, persist=False, layout='tile',
          matches=[Match(wm_class=['emesene'])],
          layout_opts={"ratio": 0.25, "master_match": Match(role=['main'])},
          ),
      Group('im', init=False, persist=False, layout='tile',
          matches=[Match(wm_class=['Gajim.py'])],
          # set the roster as master window and ratio 0.20
          layout_opts={"ratio": 0.20, "master_match": Match(role=['roster'])},
          ),
    ]

# dgroup rules that not belongs to any group
dgroups_app_rules = [
        # Everything i want to be float, but don't want to change group
        Rule(Match(title=['nested', 'gscreenshot'],
                   wm_class=['Guake.py', 'Exe', 'Onboard', 'Florence',
                        'Terminal', 'Gpaint', 'Kolourpaint', 'Wrapper',
                        'Gcr-prompter', 'Ghost',
                        re.compile('Gnome-keyring-prompt.*?')],
                   ),
            float=True, intrusive=True),

        # floating windows
        Rule(Match(wm_class=['Wine', 'Xephyr']),
            float=True),
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

    # a layout just for gimp(stolen from tych0's config)
    layout.Slice('left', 192, name='gimp', role='gimp-toolbox',
         fallback=layout.Slice('right', 256, role='gimp-dock',
         fallback=layout.Stack(stacks=1, **layout_theme))),
]

# Automatically float these types. This overrides the default behavior (which
# is to also float utility types), but the default behavior breaks our fancy
# gimp slice layout specified later on.
floating_layout = layout.Floating(auto_float_types=[
  "notification",
  "toolbar",
  "splash",
  "dialog",
], **layout_theme)


#   Screens Config
# ------------------

# Widgets Theme
widget_defaults = dict(background=["#5a5a5a", "#202020"],
                       opacity=0.9,
                       border_color="#6f6f6f",
                       fontshadow="#000000",
                       fontsize=12,
                       )

screens = [
    Screen(
        top = bar.Bar([
              widget.GroupBox(borderwidth=1, padding=1, margin_y=1),

              widget.Sep(),
              #widget.CurrentLayout(),
              widget.Prompt(),

              widget.Sep(),
              widget.TaskList(borderwidth=0, padding=2,
                  margin_y=0, highlight_method="block"),

              widget.Sep(),
              #widget.Mpd(),

              # system usage
              widget.CPUGraph(width=42, line_width=2,
                  graph_color='0066FF', fill_color='001188'),
              widget.MemoryGraph(width=42, line_width=2,
                  graph_color='22FF44', fill_color='11AA11'),
              widget.SwapGraph(width=42, line_width=2,
                  graph_color='FF2020', fill_color='C01010'),
              widget.Sep(),

              widget.Volume(update_interval=0.2, theme_path=\
                      '/usr/share/icons/gnome/48x48/status/'),

              widget.Systray(icon_size=14),
              widget.Clock('%d/%m/%y %H:%M',
                            fontsize=14, padding=6),
            ],
            size=20, opacity=0.9),
    ),
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
            call("setup_screens")
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

def main(qtile):
    detect_screens(qtile)

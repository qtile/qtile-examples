# Call python modules
from libqtile.config import EzKey, Key, Drag, Group, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import base # creating a widget instance for wifi
import subprocess, re # dealing with os & regex for parsing info from os

# Keybindings - Global declaration
# EzKey makes key assignment succint, MASC = mod, alt, shift & control
mod = "mod4"
alt = "mod1"

# widget setting
widget_defaults = dict(background='002b36',
                       foreground='ffffba',
                       font="IBM Plex Sans Medium",
                       fontsize=14,
                       markup=True,
                       padding=3, )

extension_defaults = widget_defaults.copy()

# Commonly used apps are collected in a dictionary declaration with
# 3-letter app identifier as key and the app's window label, launch key, and
# launch command values as tuple.
ap = { 'x': ('1:', 'A-x', 'terminator'),
       'b': ('2:', 'A-b', 'chromium'),
       't': ('3:', 'A-t', 'geany'),
       'f': ('4:', 'A-f', 'pcmanfm'),
       'o': ('5:', 'A-o', 'libreoffice'),
       'p': ('6:', 'A-p', '/home/shri/bin/FoxitReader'),
       'v': ('7:', 'A-v', 'vlc'),
       'u': ('8:', 'A-u', '/home/shri/bin/ugene') }

# Keys to manage desktop elements, system calls, and apps
keys = [
    # Window Manager Controls
    EzKey('M-C-r', lazy.restart()),
    EzKey('M-C-q', lazy.shutdown()),
    EzKey('M-r', lazy.spawncmd()),

    # Window Controls
    EzKey('M-C-k', lazy.window.kill()),
    EzKey('M-C-f', lazy.window.toggle_floating()),
    EzKey('M-<F11>', lazy.window.toggle_fullscreen()),

    # Layout, group, and screen modifiers
    EzKey('M-S-j', lazy.layout.shuffle_up()),
    EzKey('M-S-k', lazy.layout.shuffle_down()),
    EzKey('M-S-g', lazy.layout.grow()),
    EzKey('M-S-s', lazy.layout.shrink()),
    EzKey('M-S-n', lazy.layout.normalize()),
    EzKey('M-S-m', lazy.layout.maximize()),
    EzKey('M-S-<space>', lazy.layout.flip()),

    # Switch groups
    EzKey('M-<Left>', lazy.screen.prev_group()),
    EzKey('M-<Right>', lazy.screen.next_group()),
    EzKey('M-A-<Left>', lazy.screen.toggle_group()),

    # Cycle layouts in the same group
    EzKey('M-<Up>', lazy.next_layout()),
    EzKey('M-<Down>', lazy.prev_layout()),

    # Change window focus
    EzKey('M-<Tab>', lazy.layout.next()),
    EzKey('M-S-<Tab>', lazy.layout.previous()),

    # Switch focus to other screens
    EzKey('M-S-<Left>', lazy.to_screen(0)),  # left
    EzKey('M-S-<Right>', lazy.to_screen(1)),  # right

    # System: screenlock, reboot, and poweroff (calls a shell script)
    EzKey('A-C-<Delete>', lazy.spawn('/home/shri/.config/qtile/xit.sh')),

    # Launching applicatiions
    EzKey(ap['x'][1], lazy.spawn(ap['x'][2]),\
            lazy.group[ap['x'][0][:1]].toscreen()),
    EzKey(ap['b'][1], lazy.spawn(ap['b'][2]),\
            lazy.group[ap['b'][0][:1]].toscreen()),
    EzKey(ap['t'][1], lazy.spawn(ap['t'][2]),\
            lazy.group[ap['t'][0][:1]].toscreen()),
    EzKey(ap['f'][1], lazy.spawn(ap['f'][2]),\
            lazy.group[ap['f'][0][:1]].toscreen()),
    EzKey(ap['o'][1], lazy.spawn(ap['o'][2]),\
            lazy.group[ap['o'][0][:1]].toscreen()),
    EzKey(ap['p'][1], lazy.spawn(ap['p'][2]),\
            lazy.group[ap['p'][0][:1]].toscreen()),
    EzKey(ap['v'][1], lazy.spawn(ap['v'][2]),\
            lazy.group[ap['v'][0][:1]].toscreen()),
    EzKey(ap['u'][1], lazy.spawn(ap['u'][2]),\
            lazy.group[ap['u'][0][:1]].toscreen()), ]

# Create 8 groups, each group with a prototypical app
groups = []
for k in ap:
    grp = ap[k][0][:1]
    lbl = ap[k][0]
    groups.append(Group(grp, label=lbl))
    # Switching windows
    keys.append(Key([mod], grp, lazy.group[grp].toscreen())),
    keys.append(Key([mod, "shift"], grp, lazy.window.togroup(grp))),

# Mouse operations: moving (mod + left) or resizing (mod + right button)
mouse = (
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()), )

bring_front_click = False

# Some layout instances:
layouts = [
    layout.Max(),
    layout.Stack(stacks=2),
    layout.Floating(),
    layout.Tile() ]

# setup volume module
class Volume(widget.Volume):
    def update(self):
        vol = self.get_volume()
        if vol != self.volume:
            self.volume = vol
            if vol < 0:
                no = '0'
            else:
                no = int(vol)
            char = ' '
            self.text = '{}{}{}'.format(char, no, '%')

# Battery module
class Battery(widget.Battery):
    def _get_text(self):
        info = self._get_info()
        if info is False:
            return '---'
        if info['full']:
            no = int(info['now'] / info['full'] * 100)
        else:
            no = 0
        char = ' '
        return '{}{}{}'.format(char, no, '%')

# New widget instance: read wifi info from os, parse, and then report
class wifi(base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(self, update_interval=20)

    def poll(self):
        state = open('/sys/class/net/wlp2s0/operstate')
        if state.readline().strip() == 'down':
            return " DOWN!"
        else:
            essid = re.compile(r'(ESSID):"(.*)"')
            lqual = re.compile(r'(Link Quality)=(\d+)/(\d+)')
            out = str(subprocess.check_output(["iwconfig", "wlp2s0"]).decode('utf-8').strip())
            ssid = essid.search(out).group(2)
            quality = (int(lqual.search(out).group(2))+110)/int(lqual.search(out).group(3))*10
            return " {}% @{}".format(str(int(quality)), ssid)

# Screen: bar in the bottom; handling external display using xrandr separately.
screens = [Screen(bottom=bar.Bar([
    # Virtual desktops
    widget.GroupBox(),
    widget.Sep(padding=2, height=91),
    widget.Prompt(background='1e90ff',
                  prompt="run: ",
                  ignore_dups_history=True, ),
    widget.Sep(padding=2, height=91),
    widget.WindowName(),
    widget.Sep(padding=2, height=91),
    Battery(),
    widget.Sep(padding=2, height=91),
    Volume(update_interval=2),
    widget.Sep(padding=2, height=91),
    wifi(),
    widget.Sep(padding=2, height=91),
    widget.Systray(),
    widget.Sep(padding=2, height=91),
    widget.Clock(format='%a %D  %H:%M'), ], 30, ), ), ]  # bar is 30 px high

# Dealing with dialog windows
@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True
        window.bring_to_front()

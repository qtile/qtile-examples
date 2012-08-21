#!/usr/bin/env python
# coding: utf-8

import os

from libqtile import layout, widget, bar, manager, hook
from libqtile.widget import base
from libqtile.manager import Screen, Drag # , Click
from libqtile.command import lazy
try:
    from libqtile.manager import Key, Group
except ImportError:
    from libqtile.config import Key, Group


mod = 'mod4'

keys = [
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up()),
    Key([mod], "Tab", lazy.layout.next()),
    Key([mod, "shift"], "Tab", lazy.layout.client_to_next()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "space", lazy.nextlayout()),

    Key([mod], "t", lazy.window.toggle_floating()),

    # for MonadTall layout
    Key([mod], "l", lazy.layout.grow()),
    Key([mod], "h", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "m", lazy.layout.maximize()),

    Key([mod], "w", lazy.to_screen(0)),
    Key([mod], "e", lazy.to_screen(1)),

    Key([mod], "Return", lazy.spawn("urxvt")),
    Key([mod], "p", lazy.spawn("dmenu_run -fn 'DejaVu Sans Mono:pixelsize=11'")),

    Key([mod, "shift"], "c", lazy.window.kill()),

    Key([mod], "q", lazy.restart()),
    Key([mod, "shift"], "q", lazy.shutdown()),
]


mouse = [
    # XXX: Drag+Click on same button are not working!
    #Click([mod], "Button1", lazy.window.bring_to_front()),
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
]

group_names = [
    ("code1", {}),
    ("code2", {}),
    ("web", {'layout': 'max'}),
    ("email", {'layout': 'max'}),
    ("chat", {'layout': 'tile'}),
    ("music", {}),
    ("docs", {'layout': 'max'}),
    ("vbox", {}),
    ("gimp", {}),
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))

layouts = [
    layout.Stack(stacks=2, border_normal="#222222"),
    layout.MonadTall(border_normal="#222222"),
    layout.Tile(),
    layout.Max()
]

font = 'DejaVu Sans Mono'
foreground = '#BBBBBB'
alert = "#FFFF00"


def humanize_bytes(value):
    suff = ["B", "K", "M", "G", "T"]
    while value > 1024. and len(suff) > 1:
        value /= 1024.
        suff.pop(0)
    return "% 3s%s" % ('%.3s' % value, suff[0])


class Metrics(base._TextBox):

    defaults = [
        ("font", "Arial", "Metrics font"),
        ("fontsize", None, "Metrics pixel size. Calculated if None."),
        ("padding", None, "Metrics padding. Calculated if None."),
        ("background", "000000", "Background colour"),
        ("foreground", "ffffff", "Foreground colour")
    ]

    def __init__(self, **kwargs):
        base._TextBox.__init__(self, **kwargs)
        self.cpu_usage, self.cpu_total = self.get_cpu_stat()
        self.interfaces = {}
        self.idle_ifaces = {}

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        self.timeout_add(0, self._update)

    def get_cpu_stat(self):
        stat = [int(i) for i in open('/proc/stat').readline().split()[1:]]
        return sum(stat[:3]), sum(stat)

    def get_cpu_usage(self):
        new_cpu_usage, new_cpu_total = self.get_cpu_stat()
        cpu_usage = new_cpu_usage - self.cpu_usage
        cpu_total = new_cpu_total - self.cpu_total
        self.cpu_usage = new_cpu_usage
        self.cpu_total = new_cpu_total
        if cpu_total != 0:
            cpu_percents = "%d%%" % (float(cpu_usage) / float(cpu_total) * 100.)
        else:
            cpu_percents = "nan"
        return 'Cpu: %s' % cpu_percents

    def get_mem_usage(self):
        info = {}
        for line in open('/proc/meminfo'):
            key, val = line.split(':')
            info[key] = int(val.split()[0])
        mem = info['MemTotal']
        mem -= info['MemFree']
        mem -= info['Buffers']
        mem -= info['Cached']
        if int(info['MemTotal']) != 0:
            mem_percents = '%d%%' % (float(mem) / float(info['MemTotal']) * 100)
        else:
            mem_percents = 'nan'
        return 'Mem: %s' % mem_percents

    def get_net_usage(self):
        interfaces = []
        basedir = '/sys/class/net'
        for iface in os.listdir(basedir):
            j = os.path.join
            ifacedir = j(basedir, iface)
            statdir = j(ifacedir, 'statistics')
            idle = iface in self.idle_ifaces
            try:
                if int(open(j(ifacedir, 'carrier')).read()):
                    rx = int(open(j(statdir, 'rx_bytes')).read())
                    tx = int(open(j(statdir, 'tx_bytes')).read())
                    if iface not in self.interfaces:
                        self.interfaces[iface] = (rx, tx)
                    old_rx, old_tx = self.interfaces[iface]
                    self.interfaces[iface] = (rx, tx)
                    rx = rx - old_rx
                    tx = tx - old_tx
                    if rx or tx:
                        idle = False
                        self.idle_ifaces[iface] = 0
                        rx = humanize_bytes(rx)
                        tx = humanize_bytes(tx)
                        interfaces.append('%s: %s / %s' % (iface, rx, tx))
            except:
                pass
            if idle:
                interfaces.append(
                    '%s: %-11s' % (iface, ("%ds idle" % self.idle_ifaces[iface]))
                )
                self.idle_ifaces[iface] += 1
                if self.idle_ifaces[iface] > 30:
                    del self.idle_ifaces[iface]
        return " | ".join(interfaces)

    def _update(self):
        self.update()
        self.timeout_add(1, self.update)
        return False

    def update(self):
        stat = [self.get_cpu_usage(), self.get_mem_usage()]
        net = self.get_net_usage()
        if net:
            stat.append(net)
        self.text = " | ".join(stat)
        self.bar.draw()
        return True


#widget.CPUGraph(width=60, samples=60, margin_x=0, margin_y=0,
#                border_width=0, line_width=2, background="#222233",
#                type="line"),
#widget.MemoryGraph(width=60, samples=60, margin_x=0, margin_y=0,
#                   border_width=0, line_width=2, graph_color="#ebeb18",
#                   background="#282822", type="line"),


def get_bar():
    return bar.Bar([
        widget.GroupBox(font=font, fontsize=12, active=foreground,
                        urgent_border=alert, padding=1, borderwidth=3,
                        margin_x=3, margin_y=-2),
        widget.Sep(),
        widget.CurrentLayout(font=font, foreground=foreground),
        widget.Sep(),
        widget.WindowName(font=font, foreground=foreground),
        widget.Mpris(name='deadbeef', objname='org.mpris.deadbeef', font=font,
                     fontsize=12, foreground="#9090A0"),
        Metrics(font=font, fontsize=12, foreground="#A0A090"),
        widget.Systray(icon_size=15),
        widget.Clock(fmt="%c", font=font, foreground=foreground),
    ], 15)


screens = [
    Screen(top=get_bar()),
    Screen()
]


float_windows = set([
    "feh",
    "x11-ssh-askpass"
])


def should_be_floating(w):
    wm_class = w.get_wm_class()
    if wm_class is None:
        return True
    if isinstance(wm_class, tuple):
        for cls in wm_class:
            if cls.lower() in float_windows:
                return True
    else:
        if wm_class.lower() in float_windows:
            return True
    return w.get_wm_type() == 'dialog' or bool(w.get_wm_transient_for())


@hook.subscribe.client_new
def dialogs(window):
    if should_be_floating(window.window):
        window.floating = True

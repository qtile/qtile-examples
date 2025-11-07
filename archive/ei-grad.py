#!/usr/bin/env python
# coding: utf-8

from glob import glob
from random import choice
from time import sleep
import os
import subprocess

from libqtile import layout, widget, bar, hook
from libqtile.widget import base
from libqtile.manager import Screen, Drag, Click
from libqtile.command import lazy
from libqtile.config import Key, Group


mod = 'mod1'


def move_window_to_screen(screen):
    def cmd(qtile):
        w = qtile.currentWindow
        # XXX: strange behaviour - w.focus() doesn't work
        # if toScreen is called after togroup...
        qtile.toScreen(screen)
        if w is not None:
            w.togroup(qtile.screens[screen].group.name)
    return cmd


font = 'Ubuntu Mono'
foreground = '#BBBBBB'
alert = "#FFFF00"
fontsize = 16

font_params = {
    'font': font,
    'fontsize': fontsize,
    'foreground': foreground,
}


keys = [
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up()),
    Key([mod], "Tab", lazy.layout.next()),
    Key([mod, "shift"], "Tab", lazy.layout.client_to_next()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "space", lazy.next_layout()),

    Key([mod], "t", lazy.window.toggle_floating()),

    Key([mod], "w", lazy.to_screen(0)),
    Key([mod, "shift"], "w", lazy.function(move_window_to_screen(0))),
    Key([mod], "e", lazy.to_screen(1)),
    Key([mod, "shift"], "e", lazy.function(move_window_to_screen(1))),

    Key([mod], "Return", lazy.spawn("urxvt")),
    Key([mod], "p", lazy.spawn("dmenu_run -fn '%s:pixelsize=%d'" % (font, fontsize))),

    Key([mod, "shift"], "c", lazy.window.kill()),

    Key([mod], "q", lazy.restart()),
    Key([mod, "shift"], "q", lazy.shutdown()),
]


mouse = [
    Click([mod], "Button1", lazy.window.bring_to_front()),
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
    layout.Tile(),
    layout.Max(),
    layout.TreeTab(),
]


def humanize_bytes(value):
    suff = ["B", "K", "M", "G", "T"]
    while value > 1024. and len(suff) > 1:
        value /= 1024.
        suff.pop(0)
    return "%03d%s" % (value, suff[0])


class Metrics(base.InLoopPollText):

    def __init__(self, **config):
        self.cpu_usage, self.cpu_total = self.get_cpu_stat()
        self.interfaces = {}
        self.idle_ifaces = {}
        base.InLoopPollText.__init__(self, **config)
        self.update_interval = 1

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
        return 'cpu:%s' % cpu_percents

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
        return 'mem:%s' % mem_percents

    def get_net_usage(self):
        interfaces = []
        basedir = '/sys/class/net'
        for iface in os.listdir(basedir):
            if iface in ('lo', ):
                continue
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
                        interfaces.append('%s:%s/%s' % (iface, rx, tx))
            except:
                pass
            if idle:
                interfaces.append(
                    '%s:%-9s' % (iface, ("idle:%02d" % self.idle_ifaces[iface]))
                )
                self.idle_ifaces[iface] += 1
                if self.idle_ifaces[iface] > 30:
                    del self.idle_ifaces[iface]
        return " ".join(interfaces)

    def poll(self):
        stat = [self.get_cpu_usage(), self.get_mem_usage()]
        net = self.get_net_usage()
        if net:
            stat.append(net)
        return " ".join(stat)


def get_bar():
    return bar.Bar([
        widget.GroupBox(font=font, fontsize=fontsize, active=foreground,
                        urgent_border=alert, padding=0, borderwidth=3,
                        margin_x=3, margin_y=0),
        widget.Sep(),
        widget.CurrentLayout(**font_params),
        widget.Sep(),
        widget.WindowName(**font_params),
        Metrics(**font_params),
        widget.Systray(icon_size=15),
        widget.Sep(foreground="#000000"),
        widget.Clock(format="%c", **font_params),
    ], 20)


screens = [
    Screen(top=get_bar()),
    Screen()
]


@hook.subscribe.startup_once
def startup_once():
    subprocess.Popen(["nm-applet"])


def get_files():
    patterns = [
        '/usr/share/backgrounds/*.jpg',
        '/usr/share/backgrounds/*/*.jpg',
    ]
    files = []
    for i in patterns:
        files.extend(glob(i))
    return files


def wallpaper():
    while True:
        subprocess.call(["feh", "--bg-fill", choice(get_files())])
        sleep(300)


@hook.subscribe.startup
def startup():
    from threading import Thread
    Thread(target=wallpaper).start()

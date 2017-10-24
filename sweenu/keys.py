import subprocess
from time import time
from pathlib import Path

from libqtile.config import Key
from libqtile.command import lazy

from groups import groups

BROWSER = 'firefox'
TERM_EMULATOR = 'termite'
MUSIC_PLAYER = 'spotify'

mod = 'mod4'
alt = 'mod1'

# add 'PlayPause', 'Next' or 'Previous'
music_cmd = ('dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify '
             '/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.')


def screenshot(save=True, copy=True):
    def f(qtile):
        path = Path.home() / 'Pictures'
        path /= f'screenshot_{str(int(time() * 100))}.png'
        shot = subprocess.run(['maim'], stdout=subprocess.PIPE)

        if save:
            with open(path, 'wb') as sc:
                sc.write(shot.stdout)

        if copy:
            subprocess.run(['xclip', '-selection', 'clipboard', '-t',
                            'image/png'], input=shot.stdout)
    return f


def app_or_group(group, app):
    def f(qtile):
        if qtile.groupMap[group].windows:
            qtile.groupMap[group].cmd_toscreen()
        else:
            qtile.groupMap[group].cmd_toscreen()
            qtile.cmd_spawn(app)
    return f


def next_prev(action):
    def f(qtile):
        qtile.cmd_spawn(music_cmd + action)
    return f


def backlight(action):
    def f(qtile):
        brightness = int(subprocess.run(['xbacklight', '-get'],
                                        stdout=subprocess.PIPE).stdout)
        if brightness != 1 or action != 'dec':
            if (brightness > 49 and action == 'dec') \
                                or (brightness > 39 and action == 'inc'):
                subprocess.run(['xbacklight', f'-{action}', '10',
                                '-fps', '10'])
            else:
                subprocess.run(['xbacklight', f'-{action}', '1'])
    return f


keys = [
    Key([mod], 'k',     lazy.layout.down()),
    Key([mod], 'j',     lazy.layout.up()),
    Key([mod], 'space', lazy.layout.next()),
    Key([mod, 'control'], 'k',  lazy.layout.shuffle_down()),
    Key([mod, 'control'], 'j',  lazy.layout.shuffle_up()),
    Key([mod, 'shift'],   'h',  lazy.layout.client_to_previous()),
    Key([mod, 'shift'],   'l',  lazy.layout.client_to_next()),
    Key([mod, 'shift'], 'space', lazy.layout.rotate()),
    Key([mod, 'shift'], 'Return', lazy.layout.toggle_split()),

    Key([mod], '1',     lazy.to_screen(1)),
    Key([mod], '2',     lazy.to_screen(2)),


    Key([mod], 'Tab',   lazy.next_layout()),
    Key([mod], 'x',     lazy.window.kill()),
    Key([mod], 'r',     lazy.spawncmd()),

    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'q', lazy.shutdown()),

    # Screen
    Key([], 'F7', lazy.spawn('xset dpms force off')),
    Key([], 'XF86MonBrightnessUp',   lazy.function(backlight('inc'))),
    Key([], 'XF86MonBrightnessDown', lazy.function(backlight('dec'))),

    # Audio
    Key([], 'XF86AudioMute', lazy.spawn('ponymix toggle')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('ponymix increase 5')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('ponymix decrease 5')),
    Key([], 'XF86AudioPlay', lazy.spawn(music_cmd + 'PlayPause')),
    Key([], 'XF86AudioNext', lazy.function(next_prev('Next'))),
    Key([], 'XF86AudioPrev', lazy.function(next_prev('Previous'))),

    # Apps
    Key([mod], 'Return', lazy.spawn(TERM_EMULATOR)),
    Key([mod],  'b',     lazy.spawn(BROWSER)),
    Key([mod],  'g',     lazy.spawn('steam')),
    Key([mod],  'n',     lazy.spawn('discord')),
    Key([mod],  'm',     lazy.function(app_or_group('Music', MUSIC_PLAYER))),

    # Screenshots
    Key([], 'Print', lazy.function(screenshot())),
    Key(['control'], 'Print', lazy.spawn('deepin-screenshot'))
]

for i in groups:
    keys.append(Key([mod], i.name, lazy.group[i.name].toscreen()))
    keys.append(Key([mod, 'shift'], i.name,
                    lazy.window.togroup(i.name)))

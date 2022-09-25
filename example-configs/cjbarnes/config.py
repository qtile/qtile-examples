# -*- coding: utf-8 -*-

# I have configured the key bindings to be optimal on my 10" EeePC, so some may
# not be appropriate on regular keyboards.
# some of the widgets and layouts are not from the core Qtile distribution.

try:
    from libqtile.manager import Key, Group
except ImportError:
    from libqtile.config import Key, Group
from libqtile.manager import Screen, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from she_widget import She

follow_mouse_focus = False

mod = "mod4"
alt = "mod1"

keys = [
    Key(
        [mod, "control"],  "r",
        lazy.restart()
    ),
    Key(
        [mod], "w",
        lazy.window.kill()
    ),
    Key(
        [alt], "Tab",
        lazy.group.next_window()),
    # this is usefull when floating windows get buried
    Key(
        [alt], "grave",
        lazy.window.bring_to_front()
    ),
    Key(
        [mod, alt], "Tab",
        lazy.window.to_next_screen()
    ),
    Key(
        [mod, alt],  "1",
        lazy.to_screen(0),
        lazy.group.toscreen(0)
    ),
    Key(
        [mod, alt],  "2",
        lazy.to_screen(1),
        lazy.group.toscreen(1)
    ),
    Key(
        [mod], "Left",
        lazy.group.prevgroup()
    ),
    Key(
        [mod], "Right",
        lazy.group.nextgroup()
    ),
    Key(
        [mod], "m",
        lazy.group.setlayout('max')
    ),
    Key(
        [mod], "s",
        lazy.group.setlayout('stack')
    ),
    Key(
        [mod], "t",
        lazy.group.setlayout('tile')
    ),
    Key(
        [mod], "r",
        lazy.group.setlayout('ratiotile')
    ),
    Key(
        [mod], "x",
        lazy.group.setlayout('xmonad-tall')
    ),
    # Bindings to control the layouts
    Key(
        [mod], "h",
        lazy.layout.previous()
    ),
    Key(
        [mod], "l",
        lazy.layout.next()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "f",
        lazy.window.toggle_floating()
    ),
    Key(
        [mod], "F12",
        lazy.window.toggle_fullscreen()
    ),
    # These are unique to stack layout
    Key(
        [mod, "shift"], "l",
        lazy.layout.client_to_next()
    ),
    Key(
        [mod, "shift"], "h",
        lazy.layout.client_to_previous()
    ),
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    # Multiple function keys
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate(),
        lazy.layout.flip(),              # xmonad-tall
    ),
    Key(
        [mod, "shift"], "k",
        lazy.layout.shuffle_up(),         # Stack, xmonad-tall
       ),
    Key(
        [mod, "shift"], "j",
        lazy.layout.shuffle_down(),       # Stack, xmonad-tall
       ),
    Key(
        [mod, "control"], "l",
        lazy.layout.add(),                # Stack
        lazy.layout.increase_ratio(),     # Tile
        lazy.layout.maximize(),           # xmonad-tall
       ),
    Key(
        [mod, "control"], "h",
        lazy.layout.delete(),             # Stack
        lazy.layout.decrease_ratio(),     # Tile
        lazy.layout.normalize(),          # xmonad-tall
       ),
    Key(
        [mod, "control"], "k",
        lazy.layout.shrink(),             # xmonad-tall
        lazy.layout.decrease_nmaster(),   # Tile
       ),
    Key(
        [mod, "control"], "j",
        lazy.layout.grow(),               # xmonad-tall
        lazy.layout.increase_nmaster(),   # Tile
       ),
    # Launching applications
    # web browser
    Key(
         [mod], "n",
         lazy.spawn("firefox")
    ),
    # IRC Chat application
    Key(
        [mod], "i",
        lazy.spawn("~/bin/chat")
    ),
    # Terminal Application
    Key(
       [mod], "Return",
       lazy.spawn("~/bin/term")
    ),
    # Application Launcher
    Key(
        [mod], "space",
        lazy.spawn("dmenu_run -fn 'Terminus:size=8' -nb '#000000' -nf '#fefefe'")
    ),
    # Qtile application launcher
    Key(
        [mod], "F2",
        lazy.spawncmd(prompt=':')
    ),

    # Change the volume if our keyboard has keys
    Key(
        [], "XF86AudioRaiseVolume",
        lazy.spawn("amixer -c 0 -q set Master 2dB+")
    ),
    Key(
        [], "XF86AudioLowerVolume",
        lazy.spawn("amixer -c 0 -q set Master 2dB-")
    ),
    Key(
        [], "XF86AudioMute",
        lazy.spawn("amixer -c 0 -q set Master toggle")
    ),

    # also allow changing volume the old fashioned way
    Key(
        [mod], "equal",
        lazy.spawn("amixer -c 0 -q set Master 2dB+")
    ),
    Key(
        [mod], "minus",
        lazy.spawn("amixer -c 0 -q set Master 2dB-")
    ),
]

mouse = [
    Drag(
        [mod], "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position()
    ),
    Drag(
        [mod], "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size()
    ),
    Click(
        [mod], "Button2",
        lazy.window.bring_to_front()
    ),
]

# Next, we specify group names, and use the group name list to generate an
# appropriate set of bindings for group switching.
groups = [ Group(str(i)) for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)]
for i in groups:
    keys.append(Key([mod], i.name, lazy.group[i.name].toscreen()) )
    keys.append(Key([mod, "shift"], i.name, lazy.window.togroup(i.name), lazy.group[i.name].toscreen()) )

border = dict(
    border_normal='#808080',
    border_width=0,
)

# Layout instances:
layouts = [
    layout.Max(),
    layout.Stack(stacks=2, **border),
    layout.Tile(**border),
    layout.RatioTile(**border),
    layout.MonadTall(**border),
]

screens = [
    Screen(
        bottom = bar.Bar(
            [
                widget.GroupBox(margin_y = 1,
                                margin_x = 1,
                                borderwidth = 1,
                                padding = 1,),
                widget.Prompt(),
                widget.WindowName(foreground = "a0a0a0",),
                widget.Notify(),
                widget.Systray(),
                widget.CurrentLayout(),
                widget.Volume(foreground = "70ff70",),
                widget.Battery(energy_now_file = "charge_now",
                                energy_full_file = "charge_full",
                                power_now_file = "current_now",
                                update_delay = 5,
                                foreground = "7070ff",
                                charge_char = u'↑',
                                discharge_char = u'↓',),
                She(foreground='705030',),
                widget.Clock(foreground = "a0a0a0",
                             fmt = "%H:%M %d/%m/%Y",),
            ],
            18,
        ),
    ),
    Screen(), # Bar free screen for projector use.
]

def main(self):
    pass

@hook.subscribe.client_new
def dialogs(window):
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True

@hook.subscribe.client_new
def vue_tools(window):
    if((window.window.get_wm_class() == ('sun-awt-X11-XWindowPeer',
                                        'tufts-vue-VUE')
                and window.window.get_wm_hints()['window_group'] != 0)
                or (window.window.get_wm_class() == ('sun-awt-X11-XDialogPeer',
                                         'tufts-vue-VUE'))):
        window.floating = True

@hook.subscribe.client_new
def idle_dialogues(window):
    if((window.window.get_name() == 'Search Dialog') or
      (window.window.get_name() == 'Module') or
      (window.window.get_name() == 'Goto') or
      (window.window.get_name() == 'IDLE Preferences')):
        window.floating = True

@hook.subscribe.client_new
def libreoffice_dialogues(window):
    if((window.window.get_wm_class() == ('VCLSalFrame', 'libreoffice-calc')) or
    (window.window.get_wm_class() == ('VCLSalFrame', 'LibreOffice 3.4'))):
        window.floating = True

@hook.subscribe.client_new
def inkscape_dialogues(window):
   if(window.window.get_name() == 'Sozi'):
        window.floating = True

@hook.subscribe.client_new
def inkscape_dialogues(window):
   if((window.window.get_name() == 'Create new database')):
        window.floating = True

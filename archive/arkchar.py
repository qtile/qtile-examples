# Note that since qtile configs are just python scripts, you can check for
# syntax and runtime errors by just running this file as is from the command
# line, e.g.:
#
#    python config.py

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

# The screens variable contains information about what bars are drawn where on
# each screen. If you have multiple screens, you'll need to construct multiple
# Screen objects, each with whatever widgets you want.
#
# Below is a screen with a top bar that contains several basic qtile widgets.

screens = [Screen(top = bar.Bar([
        # This is a list of our virtual desktops.
        widget.GroupBox(urgent_alert_method='text',
                        fontsize=10, 
                        borderwidth=1),

        # A prompt for spawning processes or switching groups. This will be
        # invisible most of the time.
        widget.Prompt(),
        # Current window name.
        widget.WindowName(foreground = "a0a0a0",),
        widget.Notify(),
        widget.Systray(),
        widget.Volume(foreground = "70ff70"),
        widget.Battery(
            energy_now_file='charge_now',
            energy_full_file='charge_full',
            power_now_file='current_now',
            update_delay = 5,
            foreground = "7070ff",), 
        widget.Systray(),
        widget.Clock(foreground = "a0a0a0",
                    fmt = '%Y-%m-%d %a %I:%M %p'),
    ], 22)) # our bar is (xx)px high
]

@hook.subscribe.client_new
def dialogs(window):
    if(window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
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

# Super_L (the Windows key) is typically bound to mod4 by default, so we use
# that here.
mod = "mod4"
alt = "mod1"

# The keys variable contains a list of all of the keybindings that qtile will
# look through each time there is a key pressed.
keys = [
    # Log out; note that this doesn't use mod4: that's intentional in case mod4
    # gets hosed (which happens if you unplug and replug your usb keyboard
    # sometimes, or on system upgrades). This way you can still log back out
    # and in gracefully.
    Key([mod, "shift"], "q",
        lazy.shutdown()),
    Key([mod, "shift"],  "r",
        lazy.restart()),
    Key([mod], "c",
        lazy.window.kill()),
    Key([mod, "shift"], "m",
        lazy.group.setlayout('max')),
    Key([mod], "s",
        lazy.group.setlayout('stack')),
    Key([mod], "n",
        lazy.group.setlayout('xmonad-tall')),
    Key([mod], "x",
        lazy.group.setlayout('xmonad-tall')),

    # Key([mod], "m",
    #     lazy.window.toggle_maximize()), 
    Key([mod], "Tab",
        lazy.group.next_window()), 
    Key([mod, "shift"], "Tab",
        lazy.group.prev_window(),
        lazy.window.disable_floating()),
    # Bindings to control the layouts
    # Key([mod], "h",
    #     lazy.group.prev_window()), 
    # Key([mod], "l",
    #     lazy.group.next_window()),
    # Key([mod], "f",
    #     lazy.window.toggle_floating()), 
    Key([mod], "f",
        lazy.window.toggle_fullscreen()),
    Key([mod, alt], "j",
        lazy.window.opacity(0.5)), 
    Key([mod, alt], "k",
        lazy.window.opacity(1.0)), 
    # Key([mod, alt], "k",
    #     lazy.window.up_opacity()), 
    Key([mod], "h",
        lazy.layout.previous(), # Stack
        lazy.layout.left()),    # xmonad-tall
    Key([mod], "l",
        lazy.layout.next(),     # Stack
        lazy.layout.right()),   # xmonad-tall
    Key([mod], "k",
        lazy.layout.up()),
    Key([mod], "j",
        lazy.layout.down()),

    # These are unique to stack layout
    Key([mod, "shift"], "l",
        lazy.layout.client_to_next(), # Stack
        lazy.layout.swap_right()),    # xmonad-tall
    Key([mod, "shift"], "h",
        lazy.layout.client_to_previous(), # Stack
        lazy.layout.swap_left()),    # xmonad-tall
    Key([mod, "shift"], "Return",
        lazy.layout.toggle_split()),

    # Multiple function keys
    Key([mod, "shift"], "space",
        lazy.layout.rotate(),
        lazy.layout.flip()),              # xmonad-tall
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up()),       # Stack, xmonad-tall
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down()),         # Stack, xmonad-tall
    Key([mod], "m",
        lazy.layout.toggle_maximize()), # Stack
    Key([mod, "control"], "m",
        lazy.layout.maximize()),            # xmonad-tall
    Key([mod, "control"], "n",
        lazy.layout.normalize()),            # xmonad-tall
    Key([mod, "control"], "l",
        lazy.layout.delete(),                # Stack
        lazy.layout.increase_ratio(),     # Tile
        lazy.layout.grow()),            # xmonad-tall
    Key([mod, "control"], "h",
        lazy.layout.add(),             # Stack
        lazy.layout.decrease_ratio(),     # Tile
        lazy.layout.shrink()),         # xmonad-tall
    Key([mod, "control"], "k",
        lazy.layout.grow(),             # xmonad-tall
        lazy.layout.decrease_nmaster()),    # Tile
    Key([mod, "control"], "j",
        lazy.layout.shrink(),               # xmonad-tall
        lazy.layout.increase_nmaster()),   # Tile

    # Key([mod], "Tab",
    #     lazy.nextlayout()),

    # interact with prompts
    Key([mod], "r",              lazy.spawncmd()),
    Key([mod], "g",              lazy.switchgroup()),

    # start specific apps
    # Key([mod], "n",              lazy.spawn("firefox")),
    Key([mod], "Return",         lazy.spawn("urxvt")),

    # Change the volume if your keyboard has special volume keys.
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

    # Also allow changing volume the old fashioned way.
    Key([mod], "equal", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([mod], "minus", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
]

# This allows you to drag windows around with the mouse if you want.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groups = []
for i in ["1", "2", "3", "4", "u", "i", "o", "p"]:
    groups.append(Group(i))
    keys.append(
        Key([mod], i, lazy.group[i].toscreen())
    )
    keys.append(
        Key([mod, "shift"], i, lazy.window.togroup(i))
    )

border = dict(border_width=1)

layouts = [
    layout.Stack(stacks=2, **border),
    layout.MonadTall(**border), 
    # layout.Stack(stacks=2, border_width=1),
    layout.Max(),
]

main = None
follow_mouse_focus = True

import subprocess, re

def is_running(process):
    s = subprocess.Popen(["ps", "axuw"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x):
            return True
    return False

def execute_once(process):
    if not is_running(process):
        return subprocess.Popen(process.split())

# start the applications at Qtile startup
@hook.subscribe.startup
def startup():
    rc_dir = "/home/arkchar/.config/wmStartupScripts/"
    subprocess.Popen("sleep 3".split())
    execute_once("nm-applet")
    execute_once("synergys")
    execute_once("xcompmgr")
    execute_once(rc_dir + "xmodmap.py")
    execute_once("ibus-daemon --xim")
    execute_once("hsetroot -tile /home/arkchar/Pictures/desktop.jpg")
    execute_once(rc_dir + "trackpoint.sh")
    execute_once("xsetroot -cursor_name left_ptr")
    # execute_once("xset m 4 0")

from libqtile.config import EzKey as Key
from .mouse import *

terminal = "alacritty"

keys = [
    # Switch between windows
    Key("M-h", lazy.layout.left(), desc="Move focus to left"),
    Key("M-l", lazy.layout.right(), desc="Move focus to right"),
    Key("M-j", lazy.layout.down(), desc="Move focus down"),
    Key("M-k", lazy.layout.up(), desc="Move focus up"),
    Key("M-<space>", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key("M-S-h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key("M-S-l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key("M-S-j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key("M-S-k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key("M-C-h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key("M-C-l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key("M-C-j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key("M-C-k", lazy.layout.grow_up(), desc="Grow window up"),
    Key("M-n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key("M-S-<Return>", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key("M-<Return>", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key("M-<Tab>", lazy.next_layout(), desc="Toggle between layouts"),
    Key("M-w", lazy.window.kill(), desc="Kill focused window"),

    Key("M-C-r", lazy.restart(), desc="Restart Qtile"),
    Key("M-C-q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key("M-r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # Keybindings to launch user defined programs
    Key("A-d", lazy.spawn("dmenu_run"), desc="Launch dmenu"),
    Key("A-e", lazy.spawn("emacsclient -c -a 'emacs'"), desc="Launch emacs as emacsclient"),
    Key("A-f", lazy.spawn("thunar"), desc="Launch thunar"),
    Key("A-g", lazy.spawn("geany"), desc="Launch geany"),
    Key("A-n", lazy.spawn("nitrogen"), desc="Launch nitrogen"),
    Key("A-r", lazy.spawn("rofi -show run"), desc="Launch rofi"),
    Key("A-t", lazy.spawn("transmission-gtk"), desc="Launch transmission-gtk"),
    Key("A-u", lazy.spawn("uget-gtk"), desc="Launch uget-gtk"),
    Key("A-v", lazy.spawn("pavucontrol"), desc="Launch pavucontrol"),
    Key("A-w", lazy.spawn("chromium -no-default-browser-check"), desc="Launch chromium"),
    Key("A-C-m", lazy.spawn("/usr/local/src/thunderbird/thunderbird"), desc="Launch thunderbird"),
    Key("A-C-s", lazy.spawn("/usr/local/src/sublime_text/sublime_text"), desc="Launch sublime_text"),
    Key("A-C-w", lazy.spawn("/usr/local/src/waterfox/waterfox-bin"), desc="Launch waterfox"),
]

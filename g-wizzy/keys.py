from libqtile.config import EzKey as Key, EzDrag as Drag, EzClick as Click
from libqtile.lazy import lazy

from datetime import datetime as time

# BSP resizing taken from https://github.com/qtile/qtile/issues/1402
def resize(qtile, direction):
    layout = qtile.current_layout
    child = layout.current
    parent = child.parent

    while parent:
        if child in parent.children:
            layout_all = False

            if (direction == "left" and parent.split_horizontal) or (direction == "up" and not parent.split_horizontal):
                parent.split_ratio = max(5, parent.split_ratio - layout.grow_amount)
                layout_all = True
            elif (direction == "right" and parent.split_horizontal) or (direction == "down" and not parent.split_horizontal):
                parent.split_ratio = min(95, parent.split_ratio + layout.grow_amount)
                layout_all = True

            if layout_all:
                layout.group.layout_all()
                break

        child = parent
        parent = child.parent

@lazy.function
def resize_left(qtile):
    resize(qtile, "left")

@lazy.function
def resize_right(qtile):
    resize(qtile, "right")

@lazy.function
def resize_up(qtile):
    resize(qtile, "up")

@lazy.function
def resize_down(qtile):
    resize(qtile, "down")

@lazy.function
def float_to_front(qtile):
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.cmd_bring_to_front()

keys = [
    # Layout change
    Key("M-<Tab>", lazy.next_layout()),
    
    ## BSP Layout
    # Change focus
    Key("M-j", lazy.layout.down()),
    Key("M-k", lazy.layout.up()),
    Key("M-h", lazy.layout.left()),
    Key("M-l", lazy.layout.right()),
    # Move window
    Key("M-S-j", lazy.layout.shuffle_down()),
    Key("M-S-k", lazy.layout.shuffle_up()),
    Key("M-S-h", lazy.layout.shuffle_left()),
    Key("M-S-l", lazy.layout.shuffle_right()),
    # Move window
    Key("M-A-j", lazy.layout.flip_down()),
    Key("M-A-k", lazy.layout.flip_up()),
    Key("M-A-h", lazy.layout.flip_left()),
    Key("M-A-l", lazy.layout.flip_right()),
    # Resize window
    Key("M-C-j", resize_down),
    Key("M-C-k", resize_up),
    Key("M-C-h", resize_left),
    Key("M-C-l", resize_right),
    # Reset
    Key("M-S-n", lazy.layout.normalize()),
    # Toggle split
    Key("M-<space>", lazy.layout.toggle_split()),

    # Programs shortcuts
    Key("M-<Return>", lazy.spawn("kitty")),
    Key("M-e", lazy.spawn("nautilus")),

    Key("M-r", lazy.spawn("albert show")),
    Key("A-<Tab>", lazy.spawn("rofi -show window")),

    Key("M-f", lazy.spawn("firefox")),
    Key("M-S-f", lazy.spawn("firefox --private-window")),

    Key("<XF86Calculator>", lazy.spawn("gnome-calculator")),
    
    # Screen capture (Shift => selection, Ctrl => to clipboard)
    # Requires to write one-line script `maim_to_clip` and have it in $PATH
    Key("<Print>", lazy.spawn(f"maim /home/pierre/Pictures/{time.now().isoformat()}.png")),
    Key("S-<Print>", lazy.spawn(f"maim -s /home/pierre/Pictures/{time.now().isoformat()}.png")),
    Key("C-<Print>", lazy.spawn("maim_to_clip")),
    Key("C-S-<Print>", lazy.spawn("maim_to_clip -s")),

    Key("M-w", lazy.window.kill()),
    Key("M-C-r", lazy.restart()),
    Key("M-C-q", lazy.shutdown()),
    Key("M-S-C-q", lazy.spawn("shutdown 0")),
    Key("M-S-C-l", lazy.spawn("gnome-screensaver-command -l")),

    # Volume (hold shift for lighter adjustments)
    Key("<XF86AudioLowerVolume>", lazy.spawn("amixer -c 0 -q set Master 5%-")),
    Key("S-<XF86AudioLowerVolume>", lazy.spawn("amixer -c 0 -q set Master 1%-")),
    Key("<XF86AudioRaiseVolume>", lazy.spawn("amixer -c 0 -q set Master 5%+")),
    Key("S-<XF86AudioRaiseVolume>", lazy.spawn("amixer -c 0 -q set Master 1%+")),
    Key("<XF86AudioMute>", lazy.spawn("amixer -D pulse set Master 1+ toggle")),

    # Brightness (hold shift for lighter adjustments)
    Key("<XF86MonBrightnessUp>", lazy.spawn("light -A 5")),
    Key("S-<XF86MonBrightnessUp>", lazy.spawn("light -A 1")),
    Key("<XF86MonBrightnessDown>", lazy.spawn("light -U 5")),
    Key("S-<XF86MonBrightnessDown>", lazy.spawn("light -U 1")),

    # Multi-screen test (not very convincing)
    Key("M-<Escape>", lazy.next_screen()),
    Key("M-p", lazy.spawn("sh -c ~/scripts/monitor_layout.sh")),
    Key("M-S-p", lazy.spawn("sh -c ~/scripts/rotate_secondary_display.sh")),
]

mouse = [
    Drag("M-1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag("M-3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click("M-2", lazy.window.bring_to_front()),
    Click("M-S-1", lazy.window.toggle_floating()),
]


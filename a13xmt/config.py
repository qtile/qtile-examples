import os, subprocess
from libqtile import hook
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget


# ----------------------------
# -------- Hotkeys -----------
# ----------------------------

mod = "mod4"
keys = [

    # Layout hotkeys
    Key([mod], "h", lazy.layout.shrink_main()),
    Key([mod], "l", lazy.layout.grow_main()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),

    # Window hotkeys
    Key([mod], "space", lazy.window.toggle_fullscreen()),
    Key([mod], "c", lazy.window.kill()),

    # Spec hotkeys
    Key([mod], "Return", lazy.spawncmd()),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),

    # Apps hotkeys
    Key([mod], "v", lazy.spawn("urxvt")),
    Key([mod], "g", lazy.spawn("emacs")),
    Key([mod], "z", lazy.spawn("pcmanfm")),
    Key([mod], "x", lazy.spawn("deadbeef")),
    Key([mod], "Insert", lazy.spawn("firefox")),
    Key([mod], "Home", lazy.spawn("firefox -P music")),
    Key([mod], "Prior", lazy.spawn("firefox --private-window")),

    # System hotkeys
    Key([mod, "shift", "control"], "F11", lazy.spawn("sudo hibernate-reboot")),
    Key([mod, "shift", "control"], "F12", lazy.spawn("systemctl hibernate")),
    Key([], "Print", lazy.spawn("scrot -e 'mv $f /home/user/screenshots/'")),

    # Media hotkeys
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('pulseaudio-ctl up 5')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('pulseaudio-ctl down 5')),
    Key([], 'XF86AudioMute', lazy.spawn('pulseaudio-ctl set 1')),
]


# ----------------------------
# --- Workspaces and Rooms ---
# ----------------------------

# The basic idea behind Workspaces and Rooms is to control
# DIFFERENT subsets of groups with the SAME hotkeys.
# So we can have multiple 'qwerasdf' rooms in a different workspaces.
#
# Qtile Groups are used behind the scenes, but their visibility
# is set dynamically.

def get_group_name(workspace, room):
    """ Calculate Group name based on (workspace,room) combination.
    """
    return "%s%s" % (room, workspace)

# List of available workspaces.
# Each workspace has its own prefix and hotkey.
workspaces = [
    ('1', 'F1'),
    ('2', 'F2'),
    ('3', '1'),
    ('4', '2'),
    ('o', 'o'),
    ('p', 'p'),
]

# List of available rooms.
# Rooms are identical between workspaces, but they can
# be changed to different ones as well. Minor changes required.
rooms = "qwerasdf"

# Oops, time for a little hack there.
# This is a global object with information about current workspace.
# (viable as config code, not sure about client-server though)
wsp = {
    'current': workspaces[0][0], # first workspace is active by default
}
# ... and information about active group in the each workspace.
for w, _ in workspaces:
    wsp[w] = {
        'active_group': get_group_name(w, rooms[0]) # first room is active by default
    }

def get_workspace_groups(workspace):
    """ Get list of Groups that belongs to workspace.
    """
    return [ get_group_name(workspace, room) for room in rooms]

def to_workspace(workspace):
    """ Change current workspace to another one.
    """
    def f(qtile):
        global wsp

        # we need to save current active room(group) somewhere
        # to return to it later
        wsp[wsp['current']]['active_group'] = qtile.currentGroup.name

        # now we can change current workspace to the new one
        # (no actual switch there)
        wsp['current'] = workspace
        # and navigate to the active group from the workspace
        # (actual switch)
        qtile.groupMap[
            wsp[workspace]['active_group']
        ].cmd_toscreen()

        # we also need to change subset of visible groups in the GroupBox widget
        qtile.widgetMap['groupbox'].visible_groups=get_workspace_groups(workspace)
        qtile.widgetMap['groupbox'].draw()
        # You can do some other cosmetic stuff here.
        # For example, change Bar background depending on the current workspace.
        # # qtile.widgetMap['groupbox'].bar.background="ff0000"
    return f

def to_room(room):
    """ Change active room to another within the current workspace.
    """
    def f(qtile):
        global wsp
        qtile.groupMap[get_group_name(wsp['current'], room)].cmd_toscreen()
    return f

def window_to_workspace(workspace, room=rooms[0]):
    """ Move active window to another workspace.
    """
    def f(qtile):
        global wsp
        qtile.currentWindow.togroup(wsp[workspace]['active_group'])
    return f

def window_to_room(room):
    """ Move active window to another room within the current workspace.
    """
    def f(qtile):
        global wsp
        qtile.currentWindow.togroup(get_group_name(wsp['current'], room))
    return f

# Create individual Group for each (workspace,room) combination we have
groups = []
for workspace, hotkey in workspaces:
    for room in rooms:
        groups.append(Group(get_group_name(workspace, room)))

# Assign individual hotkeys for each workspace we have
for workspace, hotkey in workspaces:
    keys.append(Key([mod], hotkey, lazy.function(
        to_workspace(workspace))))
    keys.append(Key([mod, "shift"], hotkey, lazy.function(
        window_to_workspace(workspace))))

# Assign shared hotkeys for each room we have.
# Decision about actual group to open is made dynamically.
for room in rooms:
    keys.append(Key([mod], room, lazy.function(
        to_room(room))))
    keys.append(Key([mod, "shift"], room, lazy.function(
        window_to_room(room))))


# ---------------------------
# ---- Layouts & Widgets ----
# ---------------------------

layouts = [
    layout.MonadTall(
        border_normal=("344152"),
        border_focus=("344152"),
        border_width=1,
        ratio=0.70,
        single_border_width=1
    )
]

widget_defaults = dict(
    font='Arial',
    fontsize=12,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    border_width=2,
                    disable_drag=True,
                    highlight_method="line",
                    highlight_color=['#000000', '#000000'],
                    visible_groups=get_workspace_groups(wsp['current']),
                    spacing=0,
                ),
                widget.Prompt(
                    prompt="run: ",
                    ignore_dups_history=True,
                ),
                widget.WindowName(),
                widget.CPUGraph(
                    width=30,
                    border_width=1,
                    border_color="#000000",
                    frequency=5,
                    line_width=1,
                    samples=50,
                ),
                widget.MemoryGraph(
                    width=30,
                    border_width=1,
                    border_color="#000000",
                    line_width=1,
                    frequency=5,
                    fill_color="EEE8AA"
                ),
                widget.Volume(fontsize=10, update_interval=2),
                widget.Systray(),
                widget.Clock(
                    format='%a %b %d, %H:%M',
                ),
                widget.CurrentLayoutIcon(scale=0.65),
            ],
            30,
        ),
    )
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = "smart"
extentions = []
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

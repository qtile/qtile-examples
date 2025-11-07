try:
    from libqtile.manager import Key, Group
except ImportError:
    from libqtile.config import Key, Group

from libqtile.manager import Click, Drag, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget
import os

##########################################################################################
# HELPER FUNCTIONS
##########################################################################################

groups = [
    Group("a"),
    Group("s"),
    Group("d"),
    Group("f"),
    Group("u"),
    Group("i"),
    Group("o"),
    Group("p"),
]

def getIndex(currentGroupName):
    for i in xrange(len(groups)):
        if groups[i].name == currentGroupName:
            return i

def toPrevGroup(qtile):
    currentGroup = qtile.currentGroup.name
    i = getIndex(currentGroup)
    qtile.currentWindow.togroup(groups[ (i - 1) % len(groups)].name)

def toNextGroup(qtile):
    currentGroup = qtile.currentGroup.name
    i = getIndex(currentGroup)
    qtile.currentWindow.togroup(groups[ (i + 1) % len(groups)].name)



##########################################################################################
# KEYBINDINGS
##########################################################################################

keys = [
    Key(
        ["mod1"], "k",
        lazy.layout.down()
    ),
    Key(
        ["mod1"], "j",
        lazy.layout.up()
    ),
    Key(
        ["mod1", "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        ["mod1", "control"], "j",
        lazy.layout.shuffle_up()
    ),
    Key(
        ["mod1"], "space",
        lazy.layout.next()
    ),
    Key(
        ["mod1", "shift"], "space",
        lazy.layout.rotate()
    ),
    Key(
        ["mod1", "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key(["mod1"], "Return", lazy.spawn("urxvt -tr +sb -fg white -sh 30")),
    Key(["mod1"], "Tab",    lazy.nextlayout()),
    Key(["mod1"], "w",      lazy.window.kill()),

    Key(["mod1", "control"], "r", lazy.restart()),
    Key(["mod4"], "f", lazy.spawn("firefox")),
    Key(["mod4"], "d", lazy.spawn("deluge")),
]

for i in groups:
    keys.append(
        Key(["mod1"], i.name, lazy.group[i.name].toscreen())
    )
    keys.append(
        Key(["mod1", "shift"], i.name, lazy.window.togroup(i.name))
    )

keys.append(Key(["mod1"], "Left", lazy.group.prevgroup()))
keys.append(Key(["mod1"], "Right", lazy.group.nextgroup()))
keys.append(Key(["mod1", "shift"], "Left", lazy.function(toPrevGroup)))
keys.append(Key(["mod1", "shift"], "Right", lazy.function(toNextGroup)))



##########################################################################################

layouts = [
    layout.Max(),
    layout.Stack(stacks=2)
]

screens = [
    Screen(
        bottom = bar.Bar(
                    [
                        widget.GroupBox(),
                        widget.WindowName(fontsize=12),
                        widget.Systray(),
                        widget.Clock('%I:%M %p', fontsize=12, padding=6),
                    ],
                    30,
                ),
    ),
]

main = None
follow_mouse_focus = True
cursor_warp = False
floating_layout = layout.Floating()
mouse = ()
os.system("feh --bg-scale ~/Desktop/backgroundImage")

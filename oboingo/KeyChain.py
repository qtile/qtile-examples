"""
Creates KeyNodes that allow chaining of command groups

Originally lovingly borrowed from:  https://gitlab.com/Melkor333/dotfiles/-/blob/master/dotfiles/.config/qtile/qtile_config/KeyChain.py
Thanks Melkor33!

Cleaned up to work on qtile 0.15

Example usage:


mod3 = "Hyper_L"
mod4 = "mod4"
returnkey = "Escape"

# Create home (default) mode keys
home = KeyNode([], returnkey, [], ishome=True, name="Home")
print("Home: " + str(home))

# Set the an extra node
extra = KeyNode([], mod3, [], name="Extra")
print("Extra: " + str(extra))

# Add the extra node, and any default keys to the home node
home.addchildren(
    extra,
    # Restart or quit qtile
    KeyNode([mod4, "control"], "r", [], lazy.restart()),
    KeyNode([mod4, "control"], "q", [], lazy.shutdown()),
)

# Set the home of the extra node
extra.sethome(home)

# set the main qtile keys variable to the children of the home node.
keys = home.children

# Make a new qtile_keys node, with children
qtile_keys = KeyNode([], "q", [
    KeyNode([], 'r', [], lazy.restart()),
    KeyNode(["shift"], 'q', [], lazy.shutdown()),
    KeyNode([], "space", [], lazy.next_layout()),
], name="qtile")

# Make a new open_keys node, with children
open_keys = KeyNode([], 'o', [
    KeyNode([], 'c', [], lazy.spawn("google-chrome")),
    KeyNode([], 'v', [], lazy.spawn("code")),
    KeyNode([], 'g', [], lazy.spawn("gvim")),
    KeyNode([], 'o', [], lazy.spawn('rofi -show run')),
], name='open')

# Add the other nodes to the extra node
extra.addchildren(
    open_keys, # o
    qtile_keys, # q
)

# Set the number keys to screens, change this to however you switch groups, or hardcode your keys
k = ["1", "2", "3", "4"]
for index, i in enumerate(groups):
    home.addchildren(
        # mod1 + number of group (starting with 1) = switch to group
        KeyNode([mod4], str(index+1), [], lazy.group[i.name].toscreen(0)),
        # mod1 + shift + number of group (starting with 1) = switch to & move focused window to group
        KeyNode([mod4, "shift"], str(index+1), [], lazy.window.togroup(i.name)),
    )

"""

from libqtile.config import Key
from libqtile.widget.textbox import TextBox
from libqtile import bar, hook
from libqtile.backend.x11 import xcbq
from libqtile.command import lazy
from xcffib.xproto import EventMask
import xcffib
import subprocess

# Sets the widgets initial state
@hook.subscribe.startup_complete
def set_name():
    node = KeyNode.homenode
    if node.ishome:
        if hasattr(node, "desc"):
            node.updatewidgets(node)

class KeyNode(Key):
    homenode = ""
    def __init__(self,
                 modifiers,
                 key,
                 children,
                 *commands,
                 ishome=False,
                 **kwds):
        super().__init__(modifiers, key, *commands, lazy.function(self.updateMap()))

        # if this key has commands
        if commands:
            self.iscommand = True
        else:
            self.iscommand = False

        # Set the group name 
        if 'name' in kwds:
            self.desc = kwds.get('name')

        if ishome:
            self.home = self
            KeyNode.homenode = self
        self.key = key

        self.ishome = ishome
        self.children = children

    def __repr__(self):
        return "<KeyNode (%s, %s. %s, %s)>" % (self.modifiers, self.key, self.children, self.ishome)

    def addchildren(self, *children):
        for child in children:
            self.children.append(child)
            if hasattr(self, 'home'):
                child.sethome(self.home)

    def sethome(self, key):
        if not hasattr(self, 'home'):
            self.home = key
        if not self.iscommand:
            for child in self.children:
                child.sethome(self.home)

    def updatewidgets(self, node):
        # Update the Keywidgt instances
        for w in Keywidget.instances:
            if hasattr(w, "bar"):
                w.update(node.desc)


    def update(self, qtile):
        keylist = qtile.keys_map.copy()
        
        # unset all keys
        for key in keylist:
            qtile.ungrab_key(qtile.keys_map[key])

        # if this key has a command and a home, n = home, else n = self
        if self.iscommand and hasattr(self, 'home'):
            n = self.home
        else:
            n = self

        self.updatewidgets(n)

        # Add all the children for this node
        for child in n.children:
            qtile.grab_key(child)

        # Add the home key
        if not n.ishome and hasattr(n, 'home'):
            qtile.grab_key(n.home)

    def updateMap(self):
        def f(qtile):
            self.update(qtile)
        return f


class Keywidget(TextBox):
    instances = []
    """Shows number of available instances"""
    def __init__(self, text=" ", width=bar.CALCULATED, **config):
        super().__init__(text, width, **config)
        Keywidget.instances.append(self)
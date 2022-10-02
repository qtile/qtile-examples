from libqtile.config import Group, EzKey as Key
from libqtile.lazy import lazy

from keys import keys

groups = [Group(i) for i in "asdyxc"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key(f"M-{i.name}", lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key(f"M-S-{i.name}", lazy.window.togroup(i.name, switch_group=True)),
    ])
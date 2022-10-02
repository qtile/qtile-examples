from libqtile.config import Group, Match
from .keys import *
from .layouts import layouts

groups = [
    Group("", layout="max",        matches=[Match(wm_class=["navigator", "firefox", "vivaldi-stable", "chromium", "brave"])]),
    Group("", layout="monadtall",  matches=[Match(wm_class=["emacs", "geany", "Sublime_text"])]),
    Group("", layout="monadtall",  matches=[Match(wm_class=["inkscape", "nomacs", "ristretto", "nitrogen"])]),
    Group("", layout="monadtall",  matches=[Match(wm_class=["qpdfview", "thunar", "nemo", "caja", "pcmanfm"])]),
    Group("", layout="max",        matches=[Match(wm_class=["telegramDesktop"])]),
    Group("", layout="ratiotile"),
    Group("", layout="max",        matches=[Match(wm_class=["spotify", "pragha", "clementine", "deadbeef", "audacious"]), Match(title=["VLC media player"])]),
    Group("", layout="tile"),
]

for k, group in zip(["1", "2", "3", "4", "5", "6", "7", "8"], groups):
    keys.append(Key("M-"+(k), lazy.group[group.name].toscreen()))
    keys.append(Key("M-S-"+(k), lazy.window.togroup(group.name)))

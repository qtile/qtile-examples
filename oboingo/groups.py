#!/usr/bin/env python
# coding=utf-8
from libqtile.config import Group, ScratchPad, DropDown

from platforms import num_screens, hostname


if num_screens[hostname] == 4:
    # 4 Screens (Desktop)
    groups = []
    groups.extend([
        Group("chat", spawn="urxvt -e weechat", layout="columns", persist=True),
        Group("code", spawn="", layout="max", persist=True),
        Group("web", spawn="google-chrome", layout="max", persist=True),
        Group("files", spawn=["pcmanfm", "urxvt -e vifm"], layout="columns", persist=True),
        Group("docs", spawn="", layout="max", persist=True),
        Group("media", spawn="", layout="max", persist=True),
        Group("server", spawn="urxvt -e tmux", layout="max", persist=True),
        Group("local", spawn="urxvt -e tmux", layout="max", persist=True),
        Group("tor", spawn="", layout="max", persist=True),
        Group("rip", spawn=["filezilla", "makemkv", "ghb"], layout="columns", persist=True),
        Group("books", spawn="", layout="max", persist=True)
    ])
else:
    # 1 Screen (Laptop)
    groups = [Group(i) for i in ["web", "chat", "code", "term"]]

# Scratchpad
groups.append(
    ScratchPad("scratchpad", [
        # define a drop down terminal.
        # it is placed in the upper third of screen by default.
        DropDown("term", "urxvt", opacity=0.8),
    ]),
)

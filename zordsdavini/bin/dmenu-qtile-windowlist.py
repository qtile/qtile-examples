#!/usr/bin/env python

from libqtile.command import Client
import subprocess
import re

# connect to Qtile
c = Client()

# get info of windows
wins = []
id_map = {}
id = 0
for win in c.windows():
    if win["group"]:
        wins.append(bytes("%i: %s (%s)" % (id, win["name"], win["group"]),
            'utf-8'))
        id_map[id] = {
                'id' : win['id'],
                'group' : win['group']
                }
        id = id +1

# call dmenu
DMENU='dmenu -i -b -p ">>>" -nb #000 -nf #fff -sb #00BF32 -sf #fff'
p = subprocess.Popen(DMENU.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out = p.communicate(b"\n".join(wins))[0]

# get selected window info
id = int(re.match(b"^\d+", out).group())
win = id_map[id]

# focusing selected window
g = c.group[win["group"]]
g.toscreen()
w = g.window[win["id"]]
for i in range(len(g.info()["windows"])):
    insp = w.inspect()
    if insp['attributes']['map_state']:
        break

    g.next_window()

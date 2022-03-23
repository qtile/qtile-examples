# qtile-examples

## Table of Contents

- [Configs](#configs)
- [Plugins](#plugins)
- [Other Links](#other-links)

This is a repository for examples of how to use qtile by users. Below is a list
of user configurations and their descriptions.

Documentation for the default configuration is available
[here](http://docs.qtile.org/en/latest/manual/config/index.html) and the code
is available in the main qtile repo under
[libqtile/resources/default_config.py](https://github.com/qtile/qtile/blob/master/libqtile/resources/default_config.py).

## Configs

Config          | Description
----------------|------------
a13xmt          | rooms and workspaces
ani1001         | nord-theme, workspaces, additional-keys and some basics 
aeronotix.py    | dynamic groups
arkchar.py      | basic configuration
bglasber.py     | python functions in config
cjbarnes        | java support and application specific floating rules
cortesi.py      | kinesis keyboard keybindings
dwakar          | themed widgets
ei-grad.py      | custom widgets
emdete          | simple, beautiful, useful: lots of keyboard shortcuts
mcol            | wayland and x11 backends, graphical notifications
mort65          | rule matching, dynamic shortcuts, dropdown terminal
oboingo         | multiscreen, groups assigned to specific screens, key chording, time logger
osimplex        | OOP, scratchpad, aesthetics file, defaults files
ramnes.py       | debug layouts
roger           | dynamic groups, rule matching for windows
rxcomm          | Google Calendar widget
sweenu          | broken up in several files, custom screenshots, backlight
tailhook.py     | unicode-based window sorting
tin.py          | custom window shortcuts
tych0           | qtile development, multiple screens
zordsdavini     | various dmenu apps, screenshots, multiscreen, gmailwidget

## Plugins

Module                  | Description
------------------------|------------
traverse                | Functions for traversing focus over windows based on global position
graphical_notifications | An interactive graphical notification server similar to dunst
Qminimize               | A rofi script to handle minimize/unminimize of multiple windows at once
floating_window_snapping| Floating window borders snap to other window/screen borders when moved with mouse (X11 only)
[Mutable Scratch](https://github.com/jrwrigh/qtile-mutable-scratch) | A i3-like scratch pad, where windows maybe added/removed on the fly
[qtile-plasma](https://github.com/numirias/qtile-plasma) | An tree-based layout, very similar to i3

## Other links

Site                    | Description
------------------------|------------
[qtile-extras][1]       | A collection of widgets and other mods made by elParaguayo

[1]: https://github.com/elParaguayo/qtile-extras/ "qtile-extras"

## Contributing

To contribute please fork the repo on github and make a pull request. Please
also include in this README a short description of your config.

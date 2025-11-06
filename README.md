# qtile-examples

## Table of Contents

- [configs](#configs)
  - [x11](#x11)
  - [wayland](#wayland)
  - [archive](#archive)
- [plugins](#plugins)
- [useful links](#useful-links)

This is a repository for examples of how to use qtile by users. Below is a list of user configurations and their descriptions.

Documentation for the default configuration is available [here](http://docs.qtile.org/en/latest/manual/config/index.html) and the code is available in the main qtile repo under [`libqtile/resources/default_config.py`](https://github.com/qtile/qtile/blob/master/libqtile/resources/default_config.py).

## Configs

### x11

this section contains configuration files based primarily on the [`x11/xorg`](https://www.x.org/wiki/) windowing system.

| Config            | Description                                                                 |
| ----------------- | --------------------------------------------------------------------------- |
| [a13xmt](./a13xmt/)            | rooms and workspaces                                                        |
| [serge](./serge/)            |                                                         |
| [g-wizzy](./g-wizzy)            |                                                         |
| [ani1001](https://github.com/ani1001/dotfiles/tree/19ba46ca82887b65480f126b98ede1cf8257f048/.config/qtile)           | nord-theme, workspaces, additional-keys and some basics                     |
| [mcol](https://github.com/m-col/qtile-config)              | wayland and x11 backends, graphical notifications                           |
| [piotr-marendowski](https://github.com/marendowski/qtile-config) | Well documented, multimonitor, powerline-like, useful (with screenshots)    |
| [ramnes](https://github.com/ramnes/qtile-config)         | debug layouts                                                               |
| [zordsdavini](https://github.com/zordsdavini/qtile-config)       | various dmenu apps, screenshots, multiscreen, gmailwidget                   |
| [SpyrosRoum](https://github.com/SpyrosRoum/qtile-config)        | ability to toggle groups making them visible, like DWM                      |


### wayland

this section contains configuration files based on the [`wayland`](https://wayland.freedesktop.org/) windowing system.

| Source  | Description |
| ------- | ----------- |
| Item1.1 | Item2.1     |
| Item1.2 | Item2.2     |

### archive

this section contains unmaintained configuration files, those that use deprecated functions or those not contained within submodules.

| Source  | Description |
| ------- | ----------- |
| [tych0](./archive/tych0/)             | qtile development, multiple screens                                         |
| [sweenu](./archive/sweenu/)            | broken up in several files, custom screenshots, backlight                   |
| [rxcomm](./archive/rxcomm/)            | Google Calendar widget                                                      |
| [cjbarnes](./archive/cjbarnes/)          | java support and application specific floating rules                        |
| [cortesi](./archive/cortesi.py)        | kinesis keyboard keybindings                                                |
| [dwakar](./archive/dwakar/)            | themed widgets                                                              |
| [emdete](./archive/emdete/)            | simple, beautiful, useful: lots of keyboard shortcuts                       |
| [mort65](./archive/mort65/)            | rule matching, dynamic shortcuts, dropdown terminal                         |
| [oboingo](./archive/oboingo/)           | multiscreen, groups assigned to specific screens, key chording, time logger |
| [osimplex](./archive/osimplex/)          | OOP, scratchpad, aesthetics file, defaults files                            |
| [roger](./archive/roger/)             | dynamic groups, rule matching for windows                                   |
| [aeronotix](./archive/aeronotix.py)     | dynamic groups                                                              |
| [arkchar](./archive/arkchar.py)        | basic configuration                                                         |
| [bglasber](./archive/bglasber.py)       | python functions in config                                                  |
| [tin.py](./archive/tin.py)            | custom window shortcuts                                                     |
| [tailhook.py](./archive/tailhook.py)       | unicode-based window sorting                                               |
| [ei-grad.py](./archive/ei-grad.py)        | custom widgets                                                              |
| [lightspeedlife](./archive/lightspeedlife/) |                         |



## plugins


| Module                                                              | Description                                                                                        |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [traverse](./plugin/traverse.py)                                                            | Functions for traversing focus over windows based on global position                               |
| [graphical_notifications](./plugin/graphical_notifications.py)                                             | An interactive graphical notification server similar to dunst                                      |
| [Qminimize](https://github.com/emanuelep57/Qminimize/tree/c651a98717a4cfea1d1bfb47f212555f53f493a2)                                                           | A rofi script to handle minimize/unminimize of multiple windows at once                            |
| [floating_window_snapping](./plugin/floating_window_snapping.py)                                            | Floating window borders snap to other window/screen borders when moved with mouse (X11 only)       |
| [Mutable Scratch](https://github.com/jrwrigh/qtile-mutable-scratch) | A i3-like scratch pad, where windows maybe added/removed on the fly                                |
| [qtile-plasma](https://github.com/numirias/qtile-plasma)            | An tree-based layout, very similar to i3                                                           |
| [toggle_debug](./plugin/toggle_debug.py)                                                        | A command to toggle debug logging with notification                                                |
| [tidygroups](./plugin/tidygroups.py)                                                          | Function for moving windows to the leftmost groups (like dwm's `reorganizetags`)                   |
| [spawn_default_app](./plugin/spawn_default_app.py)                                                   | A function for setting, and then spawning a default app for each group based on a single keybind. |
| [mrtnvgr](./plugin/yandexdisk.py)           | YandexDisk widget                                                           |

## useful links

| Site              | Description                                                |
| ----------------- | ---------------------------------------------------------- |
| [qtile-extras][1] | A collection of widgets and other mods made by elParaguayo |

[1]: https://github.com/elParaguayo/qtile-extras/ "qtile-extras"

## Contributing

To contribute please fork the repo on github and make a pull request. Please
also include in this README a short description of your config.

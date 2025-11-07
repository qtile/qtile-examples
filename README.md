# qtile-examples

## Table of Contents

- [Configs](#configs)
- [Plugins](#plugins)
- [Archive](#archive)
- [Useful links](#useful-links)

This is a repository for examples of how to use qtile by users. Below is a list of user configurations and their descriptions.

Documentation for the default configuration is available [here](http://docs.qtile.org/en/latest/manual/config/index.html) and the code is available in the main qtile repo under [`libqtile/resources/default_config.py`](https://github.com/qtile/qtile/blob/master/libqtile/resources/default_config.py).

## Configs

This section contains configuration files based on both the [`x11/xorg`](https://www.x.org/wiki/) & the [`wayland`](https://wayland.freedesktop.org/) windowing system.

| Config            | Description                                                                 |
| ----------------- | --------------------------------------------------------------------------- |
| [a13xmt](./a13xmt/)            | rooms and workspaces                                                        |
| [ani1001](https://github.com/ani1001/dotfiles/tree/19ba46ca82887b65480f126b98ede1cf8257f048/.config/qtile)           | nord-theme, workspaces, additional-keys and some basics                     |
| [g-wizzy](./g-wizzy)            | custom keybindings and bar customization                                                         |
| [mcol](https://github.com/m-col/qtile-config)              | wayland and x11 backends, graphical notifications                           |
| [piotr-marendowski](https://github.com/marendowski/qtile-config) | Well documented, multimonitor, powerline-like, useful (with screenshots)    |
| [ramnes](https://github.com/ramnes/qtile-config)         | debug layouts                                                               |
| [serge](./serge/)            |    open apps in specific groups                   |
| [SpyrosRoum](https://github.com/SpyrosRoum/qtile-config)        | ability to toggle groups making them visible, like DWM                      |
| [zordsdavini](https://github.com/zordsdavini/qtile-config)       | various dmenu apps, screenshots, multiscreen, gmailwidget                   |

## Plugins

useful plugins/scripts to add into your qtile config.


| Module                                                              | Description                                                                                        |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [floating_window_snapping](./plugin/floating_window_snapping.py)                                            | Floating window borders snap to other window/screen borders when moved with mouse (X11 only)       |
| [graphical_notifications](./plugin/graphical_notifications.py)                                             | An interactive graphical notification server similar to dunst                                      |
| [move_window_ro_screen](./plugin/move_window_to_screen.py)  | move window to screen and focuses it    |
| [mrtnvgr](./plugin/yandexdisk.py)           | YandexDisk widget                                                           |
| [Mutable Scratch](https://github.com/jrwrigh/qtile-mutable-scratch) | A i3-like scratch pad, where windows maybe added/removed on the fly                                |
| [Qminimize](https://github.com/emanuelep57/Qminimize/tree/c651a98717a4cfea1d1bfb47f212555f53f493a2)                                                           | A rofi script to handle minimize/unminimize of multiple windows at once                            |
| [qtile-plasma](https://github.com/numirias/qtile-plasma)            | An tree-based layout, very similar to i3                                                           |
| [spawn_default_app](./plugin/spawn_default_app.py)                                                   | A function for setting, and then spawning a default app for each group based on a single keybind. |
| [tidygroups](./plugin/tidygroups.py)                                                          | Function for moving windows to the leftmost groups (like dwm's `reorganizetags`)                   |
| [toggle_debug](./plugin/toggle_debug.py)                                                        | A command to toggle debug logging with notification                                                |
| [traverse](./plugin/traverse.py)                                                            | Functions for traversing focus over windows based on global position                               |

### Archive

Unmaintained configuration files and those that use deprecated functions.

| Source  | Description |
| ------- | ----------- |
| [aeronotix](./archive/aeronotix.py)     | dynamic groups                                                              |
| [arkchar](./archive/arkchar.py)        | basic configuration                                                         |
| [bglasber](./archive/bglasber.py)       | python functions in config                                                  |
| [cjbarnes](./archive/cjbarnes/)          | java support and application specific floating rules                        |
| [cortesi](./archive/cortesi.py)        | kinesis keyboard keybindings                                                |
| [dwakar](./archive/dwakar/)            | themed widgets                                                              |
| [ei-grad.py](./archive/ei-grad.py)        | custom widgets                                                              |
| [emdete](./archive/emdete/)            | simple, beautiful, useful: lots of keyboard shortcuts                       |
| [lightspeedlife](./archive/lightspeedlife/) |                         |
| [mort65](./archive/mort65/)            | rule matching, dynamic shortcuts, dropdown terminal                         |
| [oboingo](./archive/oboingo/)           | multiscreen, groups assigned to specific screens, key chording, time logger |
| [osimplex](./archive/osimplex/)          | OOP, scratchpad, aesthetics file, defaults files                            |
| [roger](./archive/roger/)             | dynamic groups, rule matching for windows                                   |
| [rxcomm](./archive/rxcomm/)            | Google Calendar widget                                                      |
| [shribat](./archive/ShriBhat_qtile_config.py)  |  use emacs like keybindings          |
| [sweenu](./archive/sweenu/)            | broken up in several files, custom screenshots, backlight                   |
| [tailhook.py](./archive/tailhook.py)       | unicode-based window sorting                                               |
| [tin.py](./archive/tin.py)            | custom window shortcuts                                                     |
| [tych0](./archive/tych0/)             | qtile development, multiple screens                                         |

## Useful links

| Site              | Description                                                |
| ----------------- | ---------------------------------------------------------- |
| [qtile-extras][1] | A collection of widgets and other mods made by elParaguayo |

[1]: https://github.com/elParaguayo/qtile-extras/ "qtile-extras"

## Contributing

To contribute please fork the repo on github and make a pull request. Please
also include in this README a short description of your config.

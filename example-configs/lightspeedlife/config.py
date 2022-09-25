import LICENSE
del LICENSE

#FEATURES:
#   * .Xresources theme adherance
#   * Dynamic Groups
#   * Split file configuration
#   
#TODO:
#   * Window Rules, Group Exclusivity
#   * Chorded Keys
#   * Uniform motion for layouts
#       - e.g., shuffle_left/shuffle_right vs swap_left/swap_right
#           + additionally, in this particular case, with swap_<left|right>
#             being functions of the monad tall layout, with only two columns,
#             left/right directions are extraneous and ought to be unified in a
#             simple 'swap' command, no more, as is in spectrwm.
#   
#WISHES, DREAMS, EYECANDY:
#   * on-the-fly theming with oomox, feh, and .Xresources
#   * waveform visualizer as window border that renders sound from its window only
#   

# CONFIG
# ======
# > Load module defaults, expose modules to qtile
# > > *Including theming configurations*
# > > Screens, bars, widgets, groups, layouts
# > > Keybinds, Mousebinds
# 

import logging
import subprocess
from libqtile import hook
# from libqtile.config import Match, Rule
# from libqtile.dgroups import simple_key_binder

from rules import init_floating_layout
from layouts import init_layouts
from keys import init_binds
from groups import init_groups
from theming import theme, HOME
from screens import init_screens
logging.info('putting this here keeps pyFlakes from bothering me')

try:
    from typing import List  # noqa: F401
except ImportError:
    pass

PYTHONTRACEMALLOC=1

def rebind_input(qtile):
    global inputs
    for key in inputs.keys:
        qtile.unmap_key(key)
    inputs.configure()
    for key in inputs.keys:
        qtile.map_key(key)

focus_on_window_activation = "smart"
auto_fullscreen = False
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False

layout_defaults = theme.layouts
widget_defaults = theme.widgets
extension_defaults = widget_defaults.copy()

# Fundamental elements
floating_layout = init_floating_layout(layout_defaults)
groups = init_groups()
layouts = init_layouts(layout_defaults)
# dgroups_app_rules = init_rules()
screens = init_screens()
inputs = init_binds()
keys = inputs.keys
mouse = inputs.mouse
# widget_defaults = init_widget_defaults()
    
# Append some elements
# keys += init_group_keybindings(groups)
# groups += init_scratchpad()
# keys += init_dropdown_keybindings()

def main(qtile):
    @hook.subscribe.layout_change
    def ChangeMap(*arg):
        inputs.layout_group = arg
        rebind_input(qtile)


# Needed for some Java apps
# wmname = "LG3D"
wmname = "Qtile"

@hook.subscribe.startup_once
def autostart():
    subprocess.call([HOME + '.autorun.sh'])
    
@hook.subscribe.startup_complete
def started(*arg, **args):
    ...

# @hook.subscribe.changegroup
# def changedgroup(*arg, **args):
#     print('changedgroup', arg, args)



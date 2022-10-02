from modules.groups import groups
from modules.layouts import layouts, floating_layout
from modules.keys import *
from modules.hooks import *
from modules.screens import *

main = None  # WARNING: this is deprecated and will be removed soon
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart" # or focus
reconfigure_screens = True
auto_minimize = True
wmname = "Qtile"

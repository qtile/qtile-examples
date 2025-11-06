import os

from libqtile import layout, hook
from libqtile.config import Group

from keys import keys  # NOQA
from groups import groups  # NOQA
from screens import screens  # NOQA

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2, border_focus='#ffb6c1')
]

groups.extend([
    Group('Music', layouts=[layout.Max()]),
])

widget_defaults = {'font': 'Sans', 'fontsize': 16, 'padding': 3}


def wallpaper():
    path = '~/Pictures/wishyouwerehere_fancy.png'
    os.system('feh --bg-scale ' + path)


@hook.subscribe.startup
def autostart():
    wallpaper()


dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = 'focus'

wmname = 'qtile'

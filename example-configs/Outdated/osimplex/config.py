from os.path import expanduser
from subprocess import call

from libqtile import hook

from bindings import Keys, Mouses
from groups import Groups
from scratchpad import Scratchpad, DropDown_Keys
from rules import Rules
from screens import Screens
from aesthetics import Layout_Aesthetics, Widget_Aesthetics, Extension_Aesthetics

##### INIT #####

if __name__ in ["config", "__main__"]:

	# Init objects
	obj_keys = Keys()
	obj_mouse_touch = Mouses()
	obj_groups = Groups()
	obj_rules = Rules()
	obj_screens = Screens()

	obj_scratchpad = Scratchpad()
	obj_dd_keys = DropDown_Keys()

	obj_widget_aesthetics = Widget_Aesthetics()
	obj_layout_aesthetics = Layout_Aesthetics()
	obj_extension_aesthetics = Extension_Aesthetics()

	# Init qtile variables
	keys = obj_keys.init_keys()
	mouse = obj_mouse_touch.init_mouse()

	floating_layout = obj_layout_aesthetics.floating_layout

	groups = obj_groups.init_groups()
	dgroups_app_rules = obj_rules.init_rules()
	screens = obj_screens.init_mono_screen_single_bar()
	widget_defaults = obj_widget_aesthetics.widget_defaults
	extension_defaults = obj_extension_aesthetics.extension_defaults

	# Append
	keys += obj_keys.init_group_keybindings(groups)
	groups += obj_scratchpad.init_scratchpad()
	keys += obj_dd_keys.init_dropdown_keybindings()

	# Constant
	cursor_warp = False
	auto_fullscreen = False
	bring_front_click = False
	follow_mouse_focus = True
	focus_on_window_activation = "smart"

	# Needed for some Java programs
	wmname = "LG3D"

##### STARTUP PROGRAMS #####

# @hook.subscribe.startup_once
@hook.subscribe.startup
def start():
	call([expanduser("~/.config/qtile/autostart.sh")])

##### FLOATING TRANSIENT CLIENTS #####

@hook.subscribe.client_new
def transient_window(window):
	if window.window.get_wm_transient_for():
		window.floating = True

##### RESTART ON SCREEN CHANGE #####

@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
	qtile.cmd_restart()

# vim: tabstop=4 shiftwidth=4 noexpandtab

from libqtile import layout

def init_floating_layout(layout_defaults):
	return layout.Floating(float_rules=[
	    {'wmclass': 'confirm'},
	    {'wmclass': 'dialog'},
	    {'wmclass': 'download'},
	    {'wmclass': 'error'},
	    {'wmclass': 'file_progress'},
	    {'wmclass': 'notification'},
	    {'wmclass': 'splash'},
	    {'wmclass': 'toolbar'},
	    {'wmclass': 'confirmreset'},  # gitk
	    {'wmclass': 'makebranch'},  # gitk
	    {'wmclass': 'maketag'},  # gitk
	    {'wname': 'branchdialog'},  # gitk
	    {'wname': 'pinentry'},  # GPG key password entry
	    {'wmclass': 'ssh-askpass'},  # ssh-askpass
	    {'wmclass': 'Xephyr'},  #window manager testing w/ Xephyr
	], **layout_defaults)
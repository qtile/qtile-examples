from libqtile import bar, widget
from libqtile.config import Screen
from theming import theme as qtile_theme

theme = qtile_theme.theme

# SCREENS
# 

ur = str(r'◥')
ul = str(r'🢒🢒🢒🢒🢒🞂🞂🞂🞂◤')
lr = str(r'◢')
ll = str(r'◣')

def init_screens():
	return [
	    Screen(
	        top=bar.Bar([
	            widget.TextBox(str(ul), fontsize=32,
	            	spacing=0, padding=0),
	            widget.GroupBox(rounded=False, hide_unused=True,
	            	# setting background causes the whole widget to become
	            	# that color for some reason
	            	# background=theme['foreground'],
	            	# foreground=theme['background'],
	            	# inactive=theme['background'],
	            	# active=theme['foreground'],
	            	# this_screen_border=theme['foreground'],
	            	# this_current_screen_border=theme['background'],
	            	spacing=5, padding=0),
	            widget.TextBox(text=lr+ul, fontsize=32,
	            	spacing=0, padding=0),
	            # TODO: Make CurrentLayout Widget display custom texts.
	            # > Possibly as simple as editing layout.name
	            widget.CurrentLayout(scale=0.6),
	            widget.Prompt(prompt='$', padding=32),
	            widget.TextBox(padding=100),
	            widget.TextBox(lr, fontsize=32,
	            	spacing=0, padding=0),
	            widget.TaskList(icon_size=0, spacing=10,
	            	highlight_method='border',
	            	border=theme['color1'],
	            	background=theme['foreground'],
	            	foreground=theme['background']),
	            widget.TextBox(ul, fontsize=32,
	            	spacing=0, padding=0),
	            widget.TextBox(padding=100),
	            widget.TextBox(lr+ul, fontsize=32),
	            widget.Systray(),
	            widget.TextBox(lr, fontsize=32),
	            widget.Clock(background=theme['foreground'],
	            	foreground=theme['color0'],
	            	format='%Y%m%d[%w].%H%M:%S'),
	            widget.TextBox(background=theme['foreground'], padding=4),
	            widget.Pomodoro(foreground=theme['color0'],
	            	background=theme['foreground']),
	            widget.TextBox(background=theme['foreground'], padding=4),
	            ], 15),
	    ),
	]


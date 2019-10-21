from libqtile.widget.textbox import TextBox
from libqtile.widget.image import Image
from libqtile.widget.sep import Sep

from aesthetics import Colors, Fonts

class Colon_Widgets(object):

	font = Fonts()

	def white(self):
		return TextBox(
			text = " :: "
		)

	def bold_white(self):
		return TextBox(
			font = self.font.bold,
			text = " :: "
		)

class Pipe_Widgets(object):

	font = Fonts()

	def white(self):
		return TextBox(
			text = " | "
		)

	def bold_white(self):
		return TextBox(
			font = self.font.bold,
			text = " | "
		)

class Power_Widgets(object):

	def left_grey(self):
		return Image(
			scale = True,
			filename = "~/.config/qtile/power/bar01.png"
		)

	def right_grey(self):
		return Image(
			scale = True,
			filename = "~/.config/qtile/power/bar06.png"
		)

	def black_red(self):
		return Image(
			scale = True,
			filename = "~/.config/qtile/power/bar02.png"
		)

	def grey_red(self):
		return Image(
			scale = True,
			filename = "~/.config/qtile/power/bar02-b.png"
		)

	def red_magenta(self):
		return Image(
			scale = True,
			filename = "~/.config/qtile/power/bar03.png"
		)

	def magenta_green(self):
		return Image(
			scale = True,
			filename = "~/.config/qtile/power/bar04.png"
		)

	def green_blue(self):
		return Image(
			scale = True,
			filename = "~/.config/qtile/power/bar05.png"
		)

	def blue_orange(self):
		return Image(
			scale = True,
			filename = "~/.config/qtile/power/bar07.png"
		)

class Space_Widgets(object):

	color = Colors()

	def large_black(self):
		return Sep(
			linewidth = 0,
			padding = 3,
			background = self.color.black
		)

	def short_black(self):
		return Sep(
			linewidth = 0,
			padding = 1,
			background = self.color.black
		)

	def large_grey(self):
		return Sep(
			linewidth = 0,
			padding = 3,
			background = self.color.grey
		)

	def large_red(self):
		return Sep(
			linewidth = 0,
			padding = 3,
			background = self.color.red
		)

	def large_magenta(self):
		return Sep(
			linewidth = 0,
			padding = 3,
			background = self.color.magenta
		)

	def short_magenta(self):
		return Sep(
			linewidth = 0,
			padding = 1,
			background = self.color.magenta
		)

	def large_green(self):
		return Sep(
			linewidth = 0,
			padding = 3,
			background = self.color.green
		)

	def large_blue(self):
		return Sep(
			linewidth = 0,
			padding = 3,
			background = self.color.blue
		)

	def large_orange(self):
		return Sep(
			linewidth = 0,
			padding = 3,
			background = self.color.orange
		)

# vim: tabstop=4 shiftwidth=4 noexpandtab

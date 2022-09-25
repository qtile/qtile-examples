from libqtile.config import Screen
from libqtile.bar import Bar

from widgets_list_sep import Widgets_List
# from widgets_list_power import Widgets_List

class Bars(object):

	widgtet_list = Widgets_List()

	##### BARS #####

	def init_top_single_bar(self):
		return Bar(
			widgets = self.widgtet_list.init_top_single(),
			opacity = 1,
			size = 21
		)

	def init_top_double_bar(self):
		return Bar(
			widgets = self.widgtet_list.init_top_double(),
			opacity = 1,
			size = 21
		)

	def init_bottom_double_bar(self):
		return Bar(widgets = self.widgtet_list.init_bottom_double(),
			opacity = 1,
			size = 21
		)

class Screens(object):

	bars = Bars()

	##### SCREENS #####

	# Mono

	def init_mono_screen_single_bar(self):
		return [
			Screen(
				top = self.bars.init_top_single_bar()
			)
		]

	def init_mono_screen_double_bar(self):
		return [
			Screen(
				top = self.bars.init_top_double_bar(),
				bottom = self.bars.init_bottom_double_bar()
			)
		]

	# Dual

	def init_dual_screen_single_bar(self):
		return [
			Screen(
				top = self.bars.init_top_single_bar()
			),
			Screen(
				top = self.bars.init_top_single_bar()
			)
		]

	def init_dual_screen_double_bar(self):
		return [
			Screen(
				top = self.bars.init_top_double_bar(),
				bottom = self.bars.init_bottom_double_bar()
			),
			Screen(
				top = self.bars.init_top_double_bar(),
				bottom = self.bars.init_bottom_double_bar()
			)
		]

# vim: tabstop=4 shiftwidth=4 noexpandtab

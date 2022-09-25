from libqtile.layout.max import Max
from libqtile.layout.zoomy import Zoomy
# from libqtile.layout.stack import Stack
from libqtile.layout.columns import Columns
from libqtile.layout.floating import Floating
# from libqtile.layout.xmonad import MonadTall, MonadWide

from layout.stack import StackTall, StackWide
from layout.xmonad import MonadTall, MonadWide
from aesthetics import Layout_Aesthetics

class Layouts(object):

	theme = Layout_Aesthetics.layout_theme

	##### LAYOUTS #####

	def max(self, name = None):
		if name is None:
			return Max(**self.theme)

		return Max(name = name, **self.theme)

	def zoomy(self, name = None):
		if name is None:
			return Zoomy(**self.theme)

		return Zoomy(name = name, **self.theme)

	def floating(self, name = None):
		if name is None:
			return Floating(**self.theme)

		return Floating(name = name, **self.theme)

	def two_stackTall(self, name = None):
		if name is None:
			return StackTall(stacks = 2, **self.theme)

	def two_stackWide(self, name = None):
		if name is None:
			return StackWide(stacks = 2, **self.theme)

	def two_stack_new(self, name = None):
		if name is None:
			return Columns(num_columns = 2, split = False **self.theme)

		return Columns(name = name, num_columns = 2, split = False **self.theme)

	def monadWide(self, name = None):
		if name is None:
			return MonadWide(ratio = 0.5, **self.theme)

		return MonadWide(name = name, ratio = 0.5, **self.theme)

	def ten_monadWide(self, name = None):
		if name is None:
			return MonadWide(ratio = 0.6, **self.theme)

		return MonadWide(name = name, ratio = 0.6, **self.theme)

	def monadTall(self, name = None):
		if name is None:
			return MonadTall(ratio = 0.5, **self.theme)

		return MonadTall(name = name, ratio = 0.5, **self.theme)

	def five_monadTall(self, name = None):
		if name is None:
			return MonadTall(ratio = 0.55, **self.theme)

		return MonadTall(name = name, ratio = 0.55, **self.theme)

# vim: tabstop=4 shiftwidth=4 noexpandtab

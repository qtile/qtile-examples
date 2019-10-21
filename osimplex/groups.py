import re

from libqtile.config import Group, Match

from layouts import Layouts

class Groups(object):

	##### GROUPS #####

	def init_groups(self):

		layout = Layouts()

		return [
			Group("SYS",
				layouts = [
					layout.max(),
					layout.two_stackWide(),
					layout.two_stackTall()
				]
			),
			Group("CLI",
				layouts = [
					layout.two_stackTall(),
					layout.monadTall(),
					layout.ten_monadWide()
				],
				matches = [
					Match(title = [
						"Irssi",
						"Mpsyt"
					])
				]
			),
			Group("TYP",
				layouts = [
					layout.five_monadTall(),
					layout.two_stackTall(),
					layout.two_stackWide()
				],
				matches = [
					Match(wm_class = [
						"Subl3",
						"Howl",
						"Geany"
					])
				]
			),
			Group("VRT",
				layouts = [
					layout.floating()
				],
				matches = [
					Match(wm_class = [
						"Xephyr",
						"Virt-manager",
						re.compile("VirtualBox")
					])
				]
			),
			Group("MNG",
				layouts = [
					layout.max()
				],
				matches = [
					Match(wm_class = [
						"Nemo"
					])
				]
			),
			Group("AUX",
				layouts = [
					layout.max(),
					layout.ten_monadWide()
				]
			),
			Group("DOC",
				layouts = [
					layout.two_stackTall(),
					layout.max(),
					layout.two_stackWide(),
				],
				matches = [
					Match(wm_class = [
						"Zathura",
						"Evince"
					])
				]
			),
			Group("OFC",
				layouts = [
					layout.max(),
					layout.two_stackWide()
				],
				matches = [
					Match(wm_class = [
						"calibre",
						re.compile("NetBeans")
					]),
					Match(title = [re.compile("LibreOffice")])
				]
			),
			Group("GPX",
				layouts = [
					layout.max(),
					layout.two_stackWide()
				],
				matches = [
					Match(wm_class = [
						"Glade",
						"Inkscape",
						"mpv",
						re.compile("Gimp")
					])
				]
			),
			Group("TCM",
				layouts = [
					layout.max(),
					layout.two_stackTall()
				],
				matches = [
					Match(wm_class = [
						"Tor Browser",
						"firefox",
						"qutebrowser",
						"Chromium",
						"Links"
					]),
					Match(title = ["Links"])
				]
			),
			Group("",
				layouts = [
					layout.floating()
				]
			)
		]

# vim: tabstop=4 shiftwidth=4 noexpandtab

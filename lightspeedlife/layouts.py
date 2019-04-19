from libqtile import layout

# LAYOUTS
# 

def init_layouts(layout_defaults):
	return [
	    layout.MonadTall(**layout_defaults),
	    layout.Columns(**layout_defaults, num_stacks=2),
	    # layout.Bsp(**layout_defaults),
	    # layout.Matrix(**layout_defaults),
	    # layout.RatioTile(**layout_defaults),
	    # layout.Slice(**layout_defaults),
	    layout.Max(**layout_defaults),
	    # layout.Zoomy(margin=4, columnwidth=200),
	]


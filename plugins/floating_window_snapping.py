"""
Qtile plugin that allows a moving floating window's borders
to snap to other windows' borders and screen borders.

Usage:
1. Put this file in the same folder as the Qtile config.py file
usually ~/.config/qtile/
2. In config put:
from floating_window_snapping import move_snap_window
...
mouse = [
    Drag([mod], "Button1", move_snap_window(snap_dist=20),
        start=lazy.window.get_position()),
]
3. snap_dist (default 20) controls how many pixels the mouse has to move
before a snapped window will un-snap.
~10 for light strength snapping, ~20-30 for medium and higher for high res
displays or high dpi mice.

Tested with Qtile versions 17-19
TODO: border snapping on floating window resize
"""

from libqtile.lazy import lazy


def _get_borders(window):
    """Generate list of 4-tuples describing
    the borders including border width of every window and screen.
    """
    borders = []
    for s in window.qtile.screens:
        borders.append((s.x, s.y, s.x + s.width, s.y + s.height))
        for w in s.group.windows:
            if not w.hidden:
                borders.append((w.x, w.y, w.x+w.width+2*w.borderwidth, w.y+w.height+2*w.borderwidth))
    borders.remove((window.x, window.y, window.x+window.width+2*window.borderwidth, window.y+window.height+2*window.borderwidth))
    return borders


def _borders_touch(window, x, y, snap_dist):
    """Compares this window's borders to the borders of other
    windows/screens to see if they touch.
    """
    overlap_args = {"x": x, "y": y}
    borders = _get_borders(window)
    for b in borders:
        # Are the two borders on the same line
        if any(i in [window.edges[0], window.edges[2]+2*window.borderwidth] for i in [b[0], b[2]]):
            # Are they actually overlapping
            if window.edges[1] < b[3] and window.edges[3] > b[1]:
                # Has the mouse moved outside of the snap area
                if any(abs(window.edges[i] - x) < snap_dist for i in [0, 2]):
                    try:
                        # Window should snap so don't move along this axis
                        del overlap_args["x"]
                    except Exception:
                        pass
        # Repeat for y
        if any(i in [window.edges[1], window.edges[3]+2*window.borderwidth] for i in [b[1], b[3]]):
            if window.edges[0] < b[2] and window.edges[2] > b[0]:
                if any(abs(window.edges[i] - y) < snap_dist for i in [1, 3]):
                    try:
                        del overlap_args["y"]
                    except Exception:
                        pass
    return overlap_args


@lazy.window.function
def move_snap_window(window, x, y, snap_dist=20):
    """Move floating window to x and y.
    Border snapping makes floating window's borders
    stick to other borders for easy alignment
    """
    window.tweak_float(**_borders_touch(window, x, y, snap_dist)) 

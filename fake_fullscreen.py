"""
This module exports the function `toggle_fullscreen_state` which, as the name suggests,
toggles the fullscreen state of the current window. To clarify, this does *not* change
anything about the dimensions and position of the window, and internal (to Qtile)
fullscreen state represented by `libqtile.backend.base.FloatStates`. Instead, it changes
the fullscreen state from the point of view of the client. This can be used to make
programs render their window contents as if they were fullscreened while keeping them
within a tiled layout. It supports both X11 and Wayland.

*NOTE*: In its current form this is incompatible with `auto_fullscreen`, which must be
set to `False`. Manual fullscreening using the built-in commands (e.g.
`lazy.window.toggle_fullscreen()`) work as expected.

Example usage:

    from fake_fullscreen import toggle_fullscreen_state

    Key([mod, "shift"], "f", lazy.function(toggle_fullscreen_state))

"""

from libqtile import qtile


def _toggle_fullscreen_state_x11(*_):
    if qtile.current_window:
        xwin = qtile.current_window.window
        state = set(xwin.get_property("_NET_WM_STATE", "ATOM", unpack=int))
        atom = set([qtile.core.conn.atoms["_NET_WM_STATE_FULLSCREEN"]])
        with qtile.current_window.disable_mask(EventMask.PropertyChange):
            xwin.set_property("_NET_WM_STATE", list(state ^ atom))


def _toggle_fullscreen_state_wayland(*_):
    if qtile.current_window:
        qtile.current_window.surface.set_fullscreen(
            not qtile.current_window.surface.toplevel._ptr.current.fullscreen
        )


if qtile.core.name == "x11":
    from xcffib.xproto import EventMask

    toggle_fullscreen_state = _toggle_fullscreen_state_x11
else:
    toggle_fullscreen_state = _toggle_fullscreen_state_wayland

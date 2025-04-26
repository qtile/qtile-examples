"""
This plugin exports four functions - up, down, left and right - that when called will
move window focus to the first window in that general direction. Focussing is based
entirely on position and geometry, so is independent of screens, layouts and whether
windows are floating or tiled. It can also move focus to and from empty screens.

Example usage:

    import traverse

    keys.extend([
        Key([mod], "k", lazy.function(traverse.up)),
        Key([mod], "j", lazy.function(traverse.down)),
        Key([mod], "h", lazy.function(traverse.left)),
        Key([mod], "l", lazy.function(traverse.right)),
    ])

Qtile versions known to work: 0.28.1
"""

from dataclasses import dataclass
from typing import Optional

from libqtile.config import Screen
from libqtile.backend.base import Window


def up(qtile):
    """Focus next window or empty screen up"""
    _focus_window(qtile, Transform(exchange=True, flip=True))


def down(qtile):
    """Focus next window or empty screen down"""
    _focus_window(qtile, Transform(exchange=True, flip=False))


def left(qtile):
    """Focus next window or empty screen to the left"""
    _focus_window(qtile, Transform(exchange=False, flip=True))


def right(qtile):
    """Focus next window or empty screen to the right"""
    _focus_window(qtile, Transform(exchange=False, flip=False))


def focusable(qtile):
    """Generates potential navigation targets (Screens or Windows).

    Yields Screen objects for empty, non-focused screens. Yields Window
    objects for non-focused windows.

    Crucially, if a screen contains a fullscreen window, only that specific
    fullscreen window (if not already focused) will be yielded for that screen,
    preventing focus shifts to background windows on the same screen. If no
    window is fullscreen on a screen, all its non-focused windows are eligible.
    """

    for screen in qtile.screens:
        if not screen.group.windows and screen is not qtile.current_screen:
            yield screen
        has_fullscreen_window = any(w.fullscreen for w in screen.group.windows)
        for window in screen.group.windows:
            if window is qtile.current_window:
                continue
            if not has_fullscreen_window or window.fullscreen:
                yield window


@dataclass
class Point:
    """Point in virtual coordinates"""
    main: int
    cross: int

@dataclass
class Rectangle:
    """Store the dimensions of a rectangle in virtual coordinates"""
    obj: Window | Screen
    main: int
    cross: int
    length: int
    breadth: int

    @property
    def center(self) -> Point:
        """Return the center point of the rectangle"""
        return Point(
            self.main + self.length / 2,
            self.cross + self.breadth / 2,
        )

    @property
    def is_visible(self) -> bool:
        """Determine whether the rectangle is currently visible on the screen"""
        return isinstance(self.obj, Screen) or self.obj.is_visible()


@dataclass
class Transform:
    """Define how to extract coordinates form Window and Screen

    exchange - exchange x and y
    flip - mirror the main axis direction
    """

    exchange: bool
    flip: bool

    def __call__(self, obj: Window | Screen) -> Rectangle:
        tmp_x = -obj.x - obj.width if self.flip else obj.x
        tmp_y = -obj.y - obj.height if self.flip else obj.y
        return Rectangle(
            obj,
            tmp_y if self.exchange else tmp_x,
            tmp_x if self.exchange else tmp_y,
            obj.height if self.exchange else obj.width,
            obj.width if self.exchange else obj.height,
        )

def _focus_window(qtile, transform) -> Optional[Window | Screen]:
    focused = transform(qtile.current_window or qtile.current_screen)
    band_min = focused.cross
    band_max = focused.cross + focused.breadth

    # Filter to only consider visible objects in the correct direction
    candidates = filter(
        lambda candidate: candidate.center.main > focused.center.main + 5 and candidate.is_visible,
        map(transform, focusable(qtile))
    )

    # Then take closest in direction of the main axis, but prefer those on the
    # same level as the current window.
    closest = sorted(candidates, key=lambda candidate:
         (
            0 if band_min <= candidate.cross <= band_max
              or band_min <= candidate.cross + candidate.breadth <= band_max
            else 1,
            candidate.center.main,
            abs(focused.center.cross - candidate.center.cross),
        )
    )

    if not closest:
        # Could not find anything to focus. Maybe this is the edge of the known space :-D
        return None

    target = closest[0].obj

    qtile.focus_screen(target.group.screen.index)
    qtile.core.warp_pointer(int(target.x + target.width / 2), int(target.y + target.height / 2))

    if isinstance(target, Window):
        target.group.focus(target, True)
        target.focus(False)
        target.bring_to_front()

    return target

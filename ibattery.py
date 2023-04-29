"""
a widget that displays a nice battery icon using cairo
it is similiar to the one in ios 16.

Use:
    1. import it to your qtile config.py as follows:
    from ibattery import Battery as MyBattery

    2. add it to your widget list in your bar:
    MyBattery(),

requirements: psutil (used to gather info about the battery.)
optional: dbus-next (used to send notification.)
"""

from libqtile.widget import base
from libqtile.log_utils import logger
from libqtile.utils import send_notification
from libqtile import bar

import math
import cairocffi as cairo
import psutil


class Battery(base._Widget):
    """A widget to display a nice battery.

    requirements: psutil
    optional: dbus-next (used to send notification).
    """

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        (
            "padding",
            2,
            "int. padding on either side of of the widget."
        ),
        (
            "foreground",
            "d5d5d5",
            "string. Battery color in normal mode."
        ),
        (
            "charging_fg",
            "02a724",
            "string. foreground color when battery is charging."
        ),
        (
            "update_interval",
            20,
            "int. time to wait until the widgets refreshes."
        ),
        (
            "low_foreground",
            "ff0000",
            "string. change color when battery is low."
        ),
        (
            "warn_below",
            10,
            "int. battery level to indicate battery is low."
        ),
        (
            "notify",
            False,
            "bool. send a notification when battery is low."
        ),
        (
            "notification_timeout",
            10,
            "int. time in seconds to display notification."
        ),
        (
            "size",
            (18, 35),
            "Size of the widget. takes a tuple: (height:int, width:int). "
        ),
        (
            "font_family",
            "sans",
            "string. font family for the numbers inside the battery icon."
        ),
        (
            "font_size",
            15,
            "int. font size of the numbers inside the battery."
        ),
        (
            "font_color",
            None,
            "string. font color"
        ),
        (
            "battery_border",
            False,
            "bool. add a border to the battery icon."
        ),
    ]

    def __init__(self, **config):
        base._Widget.__init__(self, bar.CALCULATED, **config)
        self.add_defaults(Battery.defaults)

        self.HEIGHT, self.BAR_WIDTH = self.size  # battery bar
        self.margin = 2
        self.length = self.padding * 2 + self.BAR_WIDTH + 7.5 + self.margin * 2

        self._has_notified = False
        self.timeout = int(self.notification_timeout * 1000)

        self._foreground = self.foreground if self.foreground else "d5d5d5"

    def _notify(self, percent):
        if not self._has_notified:
            send_notification(
                "LOW BATTERY",
                f"Battery at {percent}%",
                urgent=True,
                timeout=self.timeout
            )
            self._has_notified = True
        else:
            self._has_notified = False

    def update(self):
        percent, charging = self.get_bat()
        if self.notify and percent < self.warn_below and not charging:
            self._notify(percent)
        self.configure_(percent, charging)
        self.draw_battery(percent, charging)

    def configure_(self, percent, plugged):
        if plugged:
            self.foreground = self.charging_fg or self._foreground
        elif percent <= self.warn_below and self.low_foreground:
            self.foreground = self.low_foreground
        else:
            self.foreground = self._foreground

    def calculate_length(self):
        if self.bar.horizontal:
            return self.padding * 2 + self.BAR_WIDTH + 7.5 + self.margin * 2
        else:
            return 0

    def draw(self):
        percent, charging = self.get_bat()
        self.configure_(percent, charging)
        self.draw_battery(percent, charging)

    def draw_battery(self, percent, charging):
        self.drawer.clear(self.background or self.bar.background)
        if self.bar.horizontal:
            PERCENT = self.BAR_WIDTH / 100 * percent
            y_margin = (self.bar.height - self.HEIGHT) / 2
            mp = self.padding + self.margin

            self.rgb("808080")
            self._fill_body(
                mp,
                y_margin,
                width=self.BAR_WIDTH,
                height=self.HEIGHT,
                linewidth=1,
                aspect=0.8
            )
            if self.battery_border:
                self.rgb(self.foreground)
                self._border(
                    mp,
                    y_margin,
                    width=self.BAR_WIDTH,
                    height=self.HEIGHT,
                    linewidth=2.6,
                    aspect=0.8
                )
            self.rgb(self.foreground)
            self._fill_body(
                mp,
                y_margin,
                width=max(PERCENT, self.BAR_WIDTH / 100 * 10),
                height=self.HEIGHT,
                linewidth=1,
                aspect=0.8
            )
            self.rgb("000000")
            self._border(
                mp,
                y_margin,
                width=self.BAR_WIDTH,
                height=self.HEIGHT,
                linewidth=0.6,
                aspect=0.8
            )
            if self.battery_border:
                self.rgb(self.foreground)
            else:
                self.rgb("808080")
            self._fill_body(
                self.BAR_WIDTH - 3 + mp,
                y_margin + 1.5,
                width=7.5,
                height=self.HEIGHT - 3,
                linewidth=5,
                aspect=5.0
            )
            self.drawer.ctx.select_font_face(
                self.font_family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD
            )
            text = str(percent)
            self.drawer.ctx.set_font_size(self.font_size)
            (x, y, width, height, dx, dy) = self.drawer.ctx.text_extents(text)
            text_x = (self.length - 7.5 - width) / 2 - x
            self.drawer.ctx.move_to(
                text_x,
                (self.bar.height + height) / 2
            )
            self.rgb(self.font_color or self.bar.background)
            self.drawer.ctx.show_text(text)

            self.drawer.draw(
                offsetx=self.offset,
                offsety=self.offsety,
                width=self.length
            )

    def rgb(self, hex):
        self.drawer.set_source_rgb(hex)

    def get_bat(self):
        battery = psutil.sensors_battery()
        try:
            plugged = battery.power_plugged
        except AttributeError:
            logger.exception("No Battery was found.")
        percent = int(battery.percent)
        return (percent, plugged)

    def _rounded_body(self, x, y, width, height, linewidth, aspect):
        aspect = aspect
        corner_radius = height / 5.0
        radius = corner_radius / aspect
        degrees = math.pi / 180.0

        self.drawer.ctx.new_sub_path()

        delta = radius + linewidth / 2
        self.drawer.ctx.arc(
            x + width - delta,
            y + delta,
            radius,
            -90 * degrees,
            0 * degrees
        )
        self.drawer.ctx.arc(
            x + width - delta,
            y + height - delta,
            radius,
            0 * degrees,
            90 * degrees
        )
        self.drawer.ctx.arc(
            x + delta,
            y + height - delta,
            radius,
            90 * degrees,
            180 * degrees
        )
        self.drawer.ctx.arc(
            x + delta,
            y + delta,
            radius,
            180 * degrees,
            270 * degrees
        )
        self.drawer.ctx.close_path()

    def _border(self, x, y, width, height, linewidth, aspect):
        self._rounded_body(x, y, width, height, linewidth, aspect)
        self.drawer.ctx.set_line_width(linewidth)
        self.drawer.ctx.stroke()

    def _fill_body(self, x, y, width, height, linewidth, aspect):
        self._rounded_body(x, y, width, height, linewidth, aspect)
        self.drawer.ctx.fill()

    def timer_setup(self):
        self.update()
        if self.update_interval is not None:
            self.timeout_add(self.update_interval, self.timer_setup)

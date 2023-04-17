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
            4,
            "padding on either side of of the widget."
        ),
        (
            "foreground",
            "ffffff",
            "Battery color in normal mode."
        ),
        (
            "charging_fg",
            "02a724",
            "foreground color when battery is charging."
        ),
        (
            "update_interval",
            30,
            "time to wait until the widgets refreshes."
        ),
        (
            "low_foreground",
            "ff0000",
            "change color when battery is low."
        ),
        (
            "warn_below",
            10,
            "battery level to indicate battery is low."
        ),
        (
            "notify",
            False,
            "send a notification when battery is low."
        ),
        (
            "notification_timeout",
            10,
            "time in seconds to display notification."
        ),
        (
            "size",
            (16, 30),
            "Size of the widget. takes a tuple: (height, width). "
        ),
        (
            "font_size",
            12,
            "font size of the numbers inside the battery."
        ),
    ]

    def __init__(self, **config):
        base._Widget.__init__(self, bar.CALCULATED, **config)
        self.add_defaults(Battery.defaults)

        self.HEIGHT, self.BAR_WIDTH = self.size  # battery bar
        self.widget_width = self.BAR_WIDTH + 6
        self.length = self.padding * 2 + self.widget_width

        self._has_notified = False
        self.timeout = int(self.notification_timeout * 1000)

        self._foreground = self.foreground

    def _notify(self, percent):
        if not self._has_notified:
            send_notification(
                "Warning",
                f"Battery at {percent}%\ncharge me baby!",
                urgent=True,
                timeout=self.timeout
            )
            self._has_notified = True
        else:
            self._has_notified = False

    def update(self):
        percent, charging = self.get_bat()
        if self.notify and percent < self.warn_below:
            self._notify(percent)
        self.configure_(percent, charging)
        self.draw_battery(percent, charging)

    def configure_(self, percent, plugged):
        if plugged:
            self.foreground = self.charging_fg
        elif percent <= self.warn_below:
            self.foreground = self.low_foreground
        else:
            self.foreground = self._foreground

    def calculate_length(self):
        if self.bar.horizontal:
            return (self.padding * 2) + self.widget_width
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

            self.drawer.set_source_rgb("8c8c8c")
            self._fill_body(
                1 + self.padding,
                y_margin,
                width=self.BAR_WIDTH,
                height=self.HEIGHT,
                linewidth=1
            )
            self.drawer.set_source_rgb(self.foreground)
            self._border(
                1 + self.padding,
                y_margin,
                width=self.BAR_WIDTH,
                height=self.HEIGHT,
                linewidth=2.6
            )
            if percent <= self.warn_below:
                self.drawer.set_source_rgb(self.low_foreground)
            else:
                self.drawer.set_source_rgb(self.foreground if charging else "ff8c1a")
            self._fill_body(
                2 + self.padding,
                y_margin,
                width=max(PERCENT, self.BAR_WIDTH / 100 * 10),
                height=self.HEIGHT,
                linewidth=1
            )
            self.drawer.set_source_rgb("000000")
            self._border(
                1 + self.padding,
                y_margin,
                width=self.BAR_WIDTH,
                height=self.HEIGHT,
                linewidth=0.6
            )
            self.drawer.set_source_rgb(self.foreground)
            self._fill_body(
                self.BAR_WIDTH - 2 + self.padding,
                y_margin + 1,
                width=8.3,
                height=self.HEIGHT - 2,
                linewidth=5
            )
            self.drawer.ctx.select_font_face(
                "sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD
            )
            bar_center = self.BAR_WIDTH / 2
            text = str(percent)
            self.drawer.ctx.set_font_size(self.font_size)
            (x, y, width, height, dx, dy) = self.drawer.ctx.text_extents(text)
            self.drawer.ctx.move_to(
                bar_center - 10 + self.padding,
                (self.bar.height + height) / 2
            )
            self.drawer.set_source_rgb("ffffff")
            self.drawer.ctx.show_text(text)

            self.drawer.draw(
                offsetx=self.offset,
                offsety=self.offsety,
                width=self.length
            )

    def get_bat(self):
        battery = psutil.sensors_battery()
        try:
            plugged = battery.power_plugged
        except AttributeError:
            logger.exception("No Battery was found.")
        percent = int(battery.percent)
        return (percent, plugged)

    def _rounded_body(self, x, y, width, height, linewidth):
        aspect = 0.8
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

    def _border(self, x, y, width, height, linewidth):
        self._rounded_body(x, y, width, height, linewidth)
        self.drawer.ctx.set_line_width(linewidth)
        self.drawer.ctx.stroke()

    def _fill_body(self, x, y, width, height, linewidth):
        self._rounded_body(x, y, width, height, linewidth)
        self.drawer.ctx.fill()

    def timer_setup(self):
        self.update()
        if self.update_interval is not None:
            self.timeout_add(self.update_interval, self.timer_setup)

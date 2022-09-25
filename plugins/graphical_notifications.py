"""
Qtile plugin that acts as a notification server and draws notification windows.

Clicking on a notification will trigger the default action, e.g. telling Firefox to open
the tab that sent the notification. If you want access to a notification's non-default
actions then you need to disable the "actions" capability of the `Notifier` by passing
`actions=False`.

Usage:

    from graphical_notifications import Notifier

    notifier = Notifier()

    keys.extend([
        Key([mod],          'grave', lazy.function(notifier.prev)),
        Key([mod, 'shift'], 'grave', lazy.function(notifier.next)),
        Key(['control'],    'space', lazy.function(notifier.close)),
    ])

Qtile versions known to work: 0.17 - 0.18
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from libqtile import configurable, hook, images, pangocffi, qtile
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.notify import notifier, ClosedReason
from libqtile.popup import Popup

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, List, Optional, Tuple

    from cairocffi import ImageSurface

    from libqtile.core.manager import Qtile
    try:
        from libqtile.notify import Notification
    except ImportError:  # no dbus_next
        Notification = Any  # type: ignore


class Notifier(configurable.Configurable):
    """
    This class provides a full graphical notification manager for the
    org.freedesktop.Notifications service implemented in libqtile.notify.

    The format option determines what text is shown on the popup windows, and supports
    markup and new line characters e.g. '<b>{summary}</b>\n{body}'. Available
    placeholders are summary, body and app_name.

    Foreground and background colours can be specified either as tuples/lists of 3
    strings, corresponding to low, normal and critical urgencies, or just a single
    string which will then be used for all urgencies. The timeout and border options can
    be set in the same way.

    The max_windows option limits how many popup windows can be drawn at a time. When
    more notifications are recieved while the maximum number are already drawn,
    notifications are queued and displayed when existing notifications are closed.

    TODO:
        - text overflow
        - select screen / follow mouse/keyboard focus
        - critical notifications to replace any visible non-critical notifs immediately?
        - hints: image-path, desktop-entry (for icon)
        - hints: Notifier parameters set for single notification?
        - hints: progress value e.g. int:value:42 with drawing

    """
    defaults = [
        ('x', 32, 'x position on screen to start drawing notifications.'),
        ('y', 64, 'y position on screen to start drawing notifications.'),
        ('width', 192, 'Width of notifications.'),
        ('height', 64, 'Height of notifications.'),
        ('format', '{summary}\n{body}', 'Text format.'),
        (
            'foreground',
            ('#ffffff', '#ffffff', '#ffffff'),
            'Foreground colour of notifications, in ascending order of urgency.',
        ),
        (
            'background',
            ('#111111', '#111111', '#111111'),
            'Background colour of notifications, in ascending order of urgency.',
        ),
        (
            'border',
            ('#111111', '#111111', '#111111'),
            'Border colours in ascending order of urgency. Or None for none.',
        ),
        (
            'timeout',
            (5000, 5000, 0),
            'Millisecond timeout duration, in ascending order of urgency.',
        ),
        ('opacity', 1.0, 'Opacity of notifications.'),
        ('border_width', 4, 'Line width of drawn borders.'),
        ('corner_radius', None, 'Corner radius for round corners, or None.'),
        ('font', 'sans', 'Font used in notifications.'),
        ('font_size', 14, 'Size of font.'),
        ('fontshadow', None, 'Color for text shadows, or None for no shadows.'),
        ('text_alignment', 'left', 'Text alignment: left, center or right.'),
        ('horizontal_padding', None, 'Padding at sides of text.'),
        ('vertical_padding', None, 'Padding at top and bottom of text.'),
        ('line_spacing', 4, 'Space between lines.'),
        (
            'overflow',
            'truncate',
            'How to deal with too much text: more_width, more_height, or truncate.',
        ),
        ('max_windows', 2, 'Maximum number of windows to show at once.'),
        ('gap', 12, 'Vertical gap between popup windows.'),
        ('sticky_history', True, 'Disable timeout when browsing history.'),
        ('icon_size', 36, 'Pixel size of any icons.'),
        ('fullscreen', 'show', 'What to do when in fullscreen: show, hide, or queue.'),
        ('screen', 'focus', 'How to select a screen: focus, mouse, or an int.'),
        ('actions', True, 'Whether to enable the actions capability.'),
    ]
    capabilities = {'body', 'body-markup', 'actions'}
    # specification: https://developer.gnome.org/notification-spec/

    def __init__(self, **config) -> None:
        configurable.Configurable.__init__(self, **config)
        self.add_defaults(Notifier.defaults)
        self._hidden: List[Popup] = []
        self._shown: List[Popup] = []
        self._queue: List[Notification] = []
        self._positions: List[Tuple[int, int]] = []
        self._scroll_popup: Optional[Popup] = None
        self._current_id: int = 0
        self._notif_id: Optional[int] = None
        self._paused: bool = False
        self._icons: Dict[str, Tuple[ImageSurface, int]] = {}

        self._make_attr_list('foreground')
        self._make_attr_list('background')
        self._make_attr_list('timeout')
        self._make_attr_list('border')

        hook.subscribe.startup(lambda: asyncio.create_task(self._configure()))

        if self.actions is False:
            Notifier.capabilities.remove("actions")

    def _make_attr_list(self, attr: str) -> None:
        """
        Turns '#000000' into ('#000000', '#000000', '#000000')
        """
        value = getattr(self, attr)
        if not isinstance(value, (tuple, list)):
            setattr(self, attr, (value,) * 3)

    async def _configure(self) -> None:
        """
        This method needs to be called to set up the Notifier with the Qtile manager and
        create the required popup windows.
        """
        if self.horizontal_padding is None:
            self.horizontal_padding = self.font_size // 2
        if self.vertical_padding is None:
            self.vertical_padding = self.font_size // 2

        popup_config = {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }

        for opt in Popup.defaults:
            key = opt[0]
            if hasattr(self, key):
                value = getattr(self, key)
                if isinstance(value, (tuple, list)):
                    popup_config[key] = value[1]
                else:
                    popup_config[key] = value

        for win in range(self.max_windows):
            popup = Popup(qtile, **popup_config)
            popup.win.process_button_click = self._process_button_click(popup)
            popup.notif = None
            self._hidden.append(popup)
            self._positions.append(
                (
                    self.x,
                    self.y + win * (self.height + 2 * self.border_width + self.gap)
                )
            )

        # Clear defunct callbacks left when reloading the config
        notifier.callbacks.clear()
        notifier.close_callbacks.clear()

        await notifier.register(
            self._notify, Notifier.capabilities, on_close=self._on_close
        )
        logger.info("Notification server started up successfully")

    def _process_button_click(self, popup: Popup) -> Callable:
        def _(x: int, y: int, button: int) -> None:
            if button == 1:
                self._act(popup)
                self._close(popup, reason=ClosedReason.dismissed)
            if button == 3:
                self._close(popup, reason=ClosedReason.dismissed)
        return _

    def _notify(self, notif: Notification) -> None:
        """
        This method is registered with the NotificationManager to handle notifications
        received via dbus. They will either be drawn now or queued to be drawn soon.
        """
        if self._paused:
            self._queue.append(notif)
            return

        if qtile.current_window and qtile.current_window.fullscreen:
            if self.fullscreen != 'show':
                if self.fullscreen == 'queue':
                    if self._unfullscreen not in hook.subscriptions:
                        hook.subscribe.float_change(self._unfullscreen)
                    self._queue.append(notif)
                return

        if notif.replaces_id:
            for popup in self._shown:
                if notif.replaces_id == popup.notif.replaces_id:
                    self._shown.remove(popup)
                    self._send(notif, popup)
                    self._reposition()
                    return

        if self._hidden:
            self._send(notif, self._hidden.pop())
        else:
            self._queue.append(notif)

    def _on_close(self, nid: int) -> None:
        for popup in self._shown:
            self._close(popup, nid=nid, reason=ClosedReason.method)

    def _unfullscreen(self) -> None:
        """
        Begin displaying of queue notifications after leaving fullscreen.
        """
        if not qtile.current_window.fullscreen:
            hook.unsubscribe.float_change(self._unfullscreen)
            self._renotify()

    def _renotify(self) -> None:
        """
        If we hold off temporarily on sending notifications and accumulate a queue, we
        should use this to send the queue through self._notify again.
        """
        queue = self._queue.copy()
        self._queue.clear()
        while queue:
            self._notify(queue.pop(0))

    def _send(
        self, notif: Notification, popup: Popup, timeout: Optional[int] = None
    ) -> None:
        """
        Draw the desired notification using the specified Popup instance.
        """
        text = self._get_text(notif)

        if "urgency" in notif.hints:
            urgency = notif.hints["urgency"].value
        else:
            urgency = 1

        self._current_id += 1
        popup.id = self._current_id  # Used for closing the popup
        popup.notif = notif  # Used for finding the visible popup's notif for actions
        if popup not in self._shown:
            self._shown.append(popup)
        popup.x, popup.y = self._get_coordinates()
        popup.place()
        icon = self._load_icon(notif)
        popup.unhide()

        popup.background = self.background[urgency]
        popup.foreground = self.foreground[urgency]
        popup.clear()

        if icon:
            popup.draw_image(
                icon[0],
                self.horizontal_padding,
                1 + (self.height - icon[1]) / 2,
            )
            popup.horizontal_padding += self.icon_size + self.horizontal_padding / 2

        for num, line in enumerate(text.split('\n')):
            popup.text = line
            y = self.vertical_padding + num * (popup.layout.height + self.line_spacing)
            popup.draw_text(y=y)
        if self.border_width:
            popup.set_border(self.border[urgency])
        popup.draw()
        if icon:
            popup.horizontal_padding = self.horizontal_padding

        if timeout is None:
            if notif.timeout is None or notif.timeout < 0:
                timeout = self.timeout[urgency]
            else:
                timeout = notif.timeout
        elif timeout < 0:
            timeout = self.timeout[urgency]
        if timeout > 0:
            qtile.call_later(timeout / 1000, self._close, popup, self._current_id)

    def _get_text(self, notif: Notification) -> str:
        summary = ''
        body = ''
        app_name = ''
        if notif.summary:
            summary = pangocffi.markup_escape_text(notif.summary)
        if notif.body:
            body = pangocffi.markup_escape_text(notif.body)
        if notif.app_name:
            app_name = pangocffi.markup_escape_text(notif.app_name)
        return self.format.format(summary=summary, body=body, app_name=app_name)

    def _get_coordinates(self) -> Tuple[int, int]:
        x, y = self._positions[len(self._shown) - 1]
        if isinstance(self.screen, int):
            screen = qtile.screens[self.screen]
        elif self.screen == 'focus':
            screen = qtile.current_screen
        elif self.screen == 'mouse':
            screen = qtile.find_screen(*qtile.mouse_position)
        return x + screen.x, y + screen.y

    def _close(self, popup: Popup, nid: Optional[int] = None, reason=1) -> None:
        """
        Close the specified Popup instance.
        """
        if popup in self._shown:
            if nid is not None and popup.id != nid:
                return
            self._shown.remove(popup)
            if self._scroll_popup is popup:
                self._scroll_popup = None
                self._notif_id = None
            popup.hide()
            if self._queue and not self._paused:
                self._send(self._queue.pop(0), popup)
            else:
                self._hidden.append(popup)
            notifier._service.NotificationClosed(popup.notif.id, reason)
        self._reposition()

    def _act(self, popup: Popup) -> None:
        """
        Execute the actions specified by the notification visible on a clicked popup.
        """
        # Currently this always invokes default action
        #actions = {i: l for i, l in zip(notif.actions[:-1:2], notif.actions[1::2])}
        if popup.notif.actions:
            notifier._service.ActionInvoked(popup.notif.id, popup.notif.actions[0])

    def _reposition(self) -> None:
        for index, shown in enumerate(self._shown):
            shown.x, shown.y = self._positions[index]
            shown.place()

    def _load_icon(self, notif: Notification) -> Optional[Tuple[ImageSurface, int]]:
        if not notif.app_icon:
            return None
        if notif.app_icon in self._icons:
            return self._icons.get(notif.app_icon)
        try:
            img = images.Img.from_path(notif.app_icon)
            if img.width > img.height:
                img.resize(width=self.icon_size)
            else:
                img.resize(height=self.icon_size)
            surface, _ = images._decode_to_image_surface(
                img.bytes_img, img.width, img.height
            )
            self._icons[notif.app_icon] = surface, surface.get_height()
        except (FileNotFoundError, images.LoadingError, IsADirectoryError) as e:
            logger.exception(e)
            self._icons[notif.app_icon] = None
        return self._icons[notif.app_icon]

    def close(self, _qtile=None) -> None:
        """
        Close the oldest of all visible popup windows.
        """
        if self._shown:
            self._close(self._shown[0])

    def close_all(self, _qtile=None) -> None:
        """
        Close all popup windows.
        """
        self._queue.clear()
        while self._shown:
            self._close(self._shown[0])

    def prev(self, _qtile=None) -> None:
        """
        Display the previous notification in the history.
        """
        if notifier.notifications:
            if self._scroll_popup is None:
                if self._hidden:
                    self._scroll_popup = self._hidden.pop(0)
                else:
                    self._scroll_popup = self._shown[0]
                self._notif_id = len(notifier.notifications)
            if self._notif_id > 0:
                self._notif_id -= 1
            self._send(
                notifier.notifications[self._notif_id],
                self._scroll_popup,
                0 if self.sticky_history else None,
            )

    def next(self, _qtile=None) -> None:
        """
        Display the next notification in the history.
        """
        if self._scroll_popup:
            if self._notif_id < len(notifier.notifications) - 1:
                self._notif_id += 1
            if self._scroll_popup in self._shown:
                self._shown.remove(self._scroll_popup)
            self._send(
                notifier.notifications[self._notif_id],
                self._scroll_popup,
                0 if self.sticky_history else None,
            )

    def pause(self, _qtile=None) -> None:
        """
        Pause display of notifications on screen. Notifications will be queued and
        presented as usual when this is called again.
        """
        if self._paused:
            self._paused = False
            self._renotify()
        else:
            self._paused = True
            while self._shown:
                self._close(self._shown[0])

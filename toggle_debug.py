"""
A function, designed for keybinding, that toggles debug logging. By default, a
desktop notification is sent to report the new logging mode, but this can be disabled by
passing ``notify=False``.

Example usage:

    from toggle_debug import toggle_debug

    keys.extend([
        Key([mod, "control"], "d", lazy.function(toggle_debug, timeout=1000)),
    ])

Qtile versions known to work: 0.21
"""

from __future__ import annotations

from logging import DEBUG
from typing import TYPE_CHECKING

from libqtile.utils import send_notification

if TYPE_CHECKING:
    from libqtile.core.manager import Qtile


_notif_id = None


def toggle_debug(qtile: Qtile, notify: bool = True, timeout: int = 2500) -> None:
    if qtile.cmd_loglevel() == DEBUG:
        qtile.cmd_warning()
        state = "disabled"
    else:
        qtile.cmd_debug()
        state = "enabled"

    if notify:
        global _notif_id

        _notif_id = send_notification(
            "Logging",
            f"Debugging {state}",
            timeout=timeout,
            id_=_notif_id,
        )

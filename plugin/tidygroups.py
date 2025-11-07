"""
Move windows to the leftmost empty groups.

For example, if you have windows on groups 2, 4 and 6,
running this command will move windows to groups 1, 2 and 3.

If follow_focus is True (default) the current window will remain focused
and the the group containing that window will be focused.

If match_layout is True (default) the layout in the destination will be changed
to match the layout of the group being moved but only if that layout is available
in the group. NB this only matches layouts by name so different configurations of
the same layout may not be matched.

Scratchpad windows are not moved.

Usage:

    from tidygroups import tidygroups

    keys.extend([
        Key([mod, "shift"], 't', lazy.function(tidygroups)),
        Key([mod, "control"], 't', lazy.function(tidygroups, follow_focus=False))
    ])    
"""
from libqtile.scratchpad import ScratchPad


def tidygroups(qtile, follow_focus: bool = True, match_layout: bool = True) -> None:
    def match_layout_name(current, destination) -> str | None:
        layouts = (
            layout.name
            for layout in destination.layouts
            if layout.name == current.layout.name
        )
        return next(layouts, None)

    win = qtile.current_window
    empty = []

    for group in qtile.groups:

        # We need to skip scratchpads
        if isinstance(group, ScratchPad):
            continue

        # If the group is empty, add it to the list of empty groups
        # and then move on to the next group
        if not group.windows:
            empty.append(group)
            continue

        # If we have an empty group available and the current group has
        # windows then we can start moving windows.
        if empty and group.windows:

            # Get the first available empty group
            destination = empty.pop(0)

            if match_layout:
                # Let's see if we can match the current layout in the destination
                layout = match_layout_name(group, destination)

                if layout is not None and layout != destination.layout.name:
                    destination.cmd_setlayout(layout)

            # We iterate over a copy of the windows list as we're modifying the original
            for window in group.windows.copy():
                if group is qtile.current_group:
                    window.hide()
                group.remove(window)
                destination.add(window)

            # This group is now empty so we can add it to the list of empty groups
            empty.append(group)

    # Set focus to group containing the previously focused window
    if follow_focus and win is not None:
        win.group.cmd_toscreen()
        win.focus(False)

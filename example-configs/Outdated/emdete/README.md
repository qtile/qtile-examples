emdete
======

ideas
-----

use the mod key for (nearly) everything (i would like to catch all keypresses
with the mod key in qtile and not deliver it to the window). the shift key
reverse the operation (tab activates the next, shift-tab the previous window).
the groups are numberic from 0 to 9. you can skip through these by the
left/right key. the keys XF86Back and XF86Forward are bound (without mod) as
well to make this even easier. esc can be used to switch between last and
current group, tab to switch between windows.

dependencies
------------

the config controls audio volume via amixer.

the config starts the following programs: x-terminal-emulator via return, gvim
via v and xlock via l (and xf86launch1, on thinkpads the blue key on top).

missing
-------

the tab key switches between windows in a group. i would like to see a reorder
of the list of windows so that mod-tab, mod-tab brings you back to the window
that was active before the two operations (mod released inbetween in composite
to mod-tab-tab which iteretes to the next window).

pidgin behaves weird when qtile is restarted.

second screen setup is not stable.


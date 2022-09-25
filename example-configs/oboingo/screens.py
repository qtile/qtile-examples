#!/usr/bin/env python
# coding=utf-8

from libqtile.config import Screen

from platforms import num_screens, hostname


# Different bars depending on how many screens
if num_screens[hostname] == 4:
    from bars import chat_bar, main_bar, media_bar, code_bar

    # 4 Screens (Desktop)
    chat_screen = Screen(top=chat_bar)
    main_screen = Screen(top=main_bar)
    media_screen = Screen(top=media_bar)
    code_screen = Screen(top=code_bar)
    screens = [main_screen, media_screen, code_screen, chat_screen]
else:
    from bars import main_bar

    # 1 screen (Laptop)
    main_screen = Screen(top=main_bar)
    screens = [main_screen]

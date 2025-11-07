#!/usr/bin/env python
# coding=utf-8

import platform

""""
Number of screens on machines I use regularly. I wish there was a good way to
query this from qtile...

It takes the hostname, then determines the number of screens for that hostname
This value is a lookup from the list, not a live query

This it used in other places to determine groups/screens/bars/etc
"""

hostname = platform.node()
num_screens = {
    'Julian': 1,
    'private': 4,
    'xephyr': 1,
}

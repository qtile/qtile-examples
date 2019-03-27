#!/usr/bin/env python
# coding=utf-8

from libqtile import bar, widget

from platforms import num_screens, hostname

soft_sep = {'linewidth': 2, 'size_percent': 70,
            'foreground': '393939', 'padding': 7}

"""
Different Bar layouts for different computers
4 screens on the desktop, but only 1 on the laptops
"""

if num_screens[hostname] == 4:
    # 4 Screens (Desktop)
    chat_bar = bar.Bar(
        [
            widget.CurrentLayoutIcon(scale=0.9, foreground="EFEFEF", ),
            widget.GroupBox(),
            widget.Sep(linewidth=2, size_percent=100, padding=12),
            widget.Prompt(),
            widget.TaskList(),
            widget.DF(),
            widget.Pomodoro(),
            widget.Systray(),
            widget.Net(interface="eno1"),
            widget.Sep(**soft_sep),
            widget.Volume(),
            widget.Sep(**soft_sep),
            widget.ThermalSensor(),
            widget.Sep(**soft_sep),
            widget.Memory(),
            widget.Sep(**soft_sep),
            widget.Clock(format='%Y-%m-%d %a %H:%M:%S'),
        ], 30)
    main_bar = bar.Bar(
        [
            widget.CurrentLayoutIcon(scale=0.9, foreground="EFEFEF", ),
            widget.GroupBox(),
            widget.Sep(linewidth=2, size_percent=100, padding=12),
            widget.Prompt(),
            widget.TaskList(),
            widget.DF(),
            widget.Pomodoro(),
            widget.Systray(),
            widget.Net(interface="eno1"),
            widget.Sep(**soft_sep),
            widget.Volume(),
            widget.Sep(**soft_sep),
            widget.ThermalSensor(),
            widget.Sep(**soft_sep),
            widget.Memory(),
            widget.Sep(**soft_sep),
            widget.Clock(format='%Y-%m-%d %a %H:%M:%S'),
        ], 30)
    media_bar = bar.Bar(
        [
            widget.CurrentLayoutIcon(scale=0.9, foreground="EFEFEF", ),
            widget.GroupBox(),
            widget.Sep(linewidth=2, size_percent=100, padding=12),
            widget.Prompt(),
            widget.TaskList(),
            widget.Sep(**soft_sep),
            widget.Volume(),
        ], 30)
    code_bar = bar.Bar(
        [
            widget.CurrentLayoutIcon(scale=0.9, foreground="EFEFEF", ),
            widget.GroupBox(),
            widget.Sep(linewidth=2, size_percent=100, padding=12),
            widget.Prompt(),
            widget.TaskList(),
            widget.DF(),
            widget.Pomodoro(),
            widget.Systray(),
            widget.Net(interface="eno1"),
            widget.Sep(**soft_sep),
            widget.Volume(),
            widget.Sep(**soft_sep),
            widget.ThermalSensor(),
            widget.Sep(**soft_sep),
            widget.Memory(),
            widget.Sep(**soft_sep),
            widget.Clock(format='%Y-%m-%d %a %H:%M:%S'),
        ], 30)
else:
    main_bar = bar.Bar(
        [
            widget.CurrentLayoutIcon(scale=0.9, foreground="EFEFEF", ),
            widget.GroupBox(),
            widget.Sep(linewidth=2, size_percent=100, padding=12),
            widget.Prompt(),
            widget.TaskList(),
            widget.DF(),
            widget.Pomodoro(),
            widget.Systray(),
            widget.Net(interface="wlp2s0"),
            widget.Sep(**soft_sep),
            widget.Volume(),
            widget.Sep(**soft_sep),
            widget.Battery(),
            widget.Sep(**soft_sep),
            widget.ThermalSensor(),
            widget.Sep(**soft_sep),
            widget.Memory(),
            widget.Sep(**soft_sep),
            widget.Clock(format='%Y-%m-%d %a %H:%M:%S'),
        ], 30)

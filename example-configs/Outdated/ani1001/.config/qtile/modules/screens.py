from libqtile import bar
from .widgets import *
from libqtile.config import Screen

import os

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    background=colors[1], #2e3440
                    foreground=colors[5], #d8dee9
                    linewidth=1,
                    padding=10
                ),
                widget.Image(
                    filename="~/.config/qtile/icons/qtilelogo.png",
                    iconsize=8,
                    background=colors[1],
                    mouse_callbacks={'Button1': lambda : qtile.cmd_spawn('rofi -show run')}
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.GroupBox(
                    active=colors[16], #b48ead
                    borderwidth=2,
                    disable_drag=True,
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    hide_unused=False,
                    highlight_method='line',
                    inactive=colors[6], #e5e9f0
                    margin_x=0,
                    margin_y=3,
                    padding_x=5,
                    padding_y=8,
                    rounded=False,
                    this_current_screen_border=colors[14], #ebcb8b
                    urgent_alert_method='line'
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.CurrentLayoutIcon(
                    background=colors[1],
                    custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                    foreground=colors[6], #e5e9f0
                    padding=0,
                    scale=0.65
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.CurrentLayout(
                    background=colors[1],
                    font='Ubuntu Bold',
                    foreground=colors[6]
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.Prompt(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6]
                ),
                widget.Spacer(),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text=' '
                ),
                widget.KeyboardLayout(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6]
                ),
                widget.CapsNumLockIndicator(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6]
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text=' '
                ),
                widget.Clock(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6],
                    format='%a %d, (%B) %H:%M:%S '
                ),
            ],
            22,
            opacity=1.0
        ),
        bottom=bar.Bar(
            [
                widget.WindowName(
                    background=colors[1],
                    foreground=colors[6],
                    font='Ubuntu',
                    fontsize = 12,
                    max_chars=60
                ),
                widget.Spacer(),
                widget.Systray(
                    background=colors[1],
                    icon_size=20,
                    padding=4
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text=' '
                ),
                widget.ThermalSensor(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6],
                    update_interval=2
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text=' '
                ),
                widget.Memory(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6],
                    format="{MemUsed: .0f}{mm}",
                    update_interval=1.0
                ),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text=' '
                ),
                widget.CPU(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[6],
                    format='CPU {load_percent}%',
                    update_interval=1
                ),
                #widget.CPUGraph(
                #    background=colors[1],
                #    border_color=colors[5],
                #    border_width=0,
                #    core='all',
                #    fill_color=colors[10], #81a1c1
                #    foreground=colors[5],
                #    graph_color=colors[10],
                #    line_width=1,
                #    type='linefill'
                #),
                widget.Sep(
                    background=colors[1],
                    foreground=colors[5],
                    linewidth=1,
                    padding=10
                ),
                widget.TextBox(
                    background=colors[1],
                    font='Ubuntu Nerd Font',
                    fontsize=14,
                    foreground=colors[6],
                    padding=0,
                    text='  '
                ),
                widget.Net(
                    background=colors[1],
                    font='Ubuntu',
                    fontsize=12,
                    foreground=colors[5],
                    format='{interface}: {down} ↓ ',
                    interface='all',
                    padding=0
                ),
                #widget.NetGraph(
                #    background=colors[1],
                #    bandwidth="down",
                #    border_color=colors[5],
                #    border_width=0,
                #    fill_color=colors[9], #88c0d0
                #    foreground=colors[5],
                #    graph_color=colors[9],
                #    interface="auto",
                #    line_width=1,
                #    padding=0,
                #    type='linefill'
                #),
            ],
            22,
            opacity=1.0
        ),
    ),
]

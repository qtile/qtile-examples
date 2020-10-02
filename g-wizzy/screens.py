from libqtile.config import Screen
from libqtile import widget, bar

from Xlib import display as xdisplay

# Solarized light
theme = dict(
    base03 = '002b36',
    base02 = '073642',
    base01 = '586e75',
    base00 = '657b83',
    base0 = '839496',
    base1 = '93a1a1',
    base2 = 'eee8d5',
    base3 = 'fdf6e3',
    yellow = 'b58900',
    orange = 'cb4b16',
    red = 'dc322f',
    magenta = 'd33682'
)

color_schemes = [
    dict(
        background = theme['base3'],
        arrow_color = theme['base2'],
        foreground = theme['base01']
    ),
    dict(
        background = theme['base2'],
        arrow_color = theme['base3'],
        foreground = theme['base01']
    )
]

# Separator-related functions and variables

def separator(right_looking = True):
    global color_scheme
    if right_looking:
        separator.current_scheme = 1 - separator.current_scheme
        color_scheme = color_schemes[separator.current_scheme]

        return widget.TextBox(
            u'\ue0b0', 
            **separator_defaults,
            background = color_scheme["background"],
            foreground = color_scheme["arrow_color"]
        )
    else:
        ret = widget.TextBox(
            u'\ue0b2', 
            **separator_defaults,
            background = color_scheme["background"],
            foreground = color_scheme["arrow_color"]
        )

        separator.current_scheme = 1 - separator.current_scheme
        color_scheme = color_schemes[separator.current_scheme]

        return ret

color_scheme = color_schemes[1]
separator.current_scheme = 1

separator_defaults = dict(
    font='Victor Mono',
    fontsize=24,
    padding=0,
)


widget_defaults = dict(
    font='Victor Mono Semibold',
    fontsize=12,
    padding=6,
)
extension_defaults = widget_defaults.copy()

icon_defaults = dict(
    font='feather',
    fontsize = 18,
    padding = 6,
)

battery_widget_defaults = dict(
    format='{char}[{percent:2.0%}]  ',
    low_percentage=0.2,
    update_interval=5,
    show_short_text=False
)

bar_widgets = [

    widget.GroupBox(
        **widget_defaults,
        **color_scheme,
        disable_drag=False,
        # Text colors
        active=theme["base03"],
        inactive=theme["base1"],
        # Current screen colors
        highlight_method='line',
        highlight_color=theme["yellow"],
        this_current_screen_border=theme["red"],
        # Urgent colors
        urgent_alert_method="block",
        urgent_border=theme["magenta"]
    ),

    separator(),

    widget.Spacer(
        length = 16,
        **color_scheme,
    ),

    widget.WindowName(
        **widget_defaults,
        **color_scheme,
    ),

    # Note: requires to change the default Ubuntu command in libqtile.widget.CheckUpdates
    # from `aptitude search ~U`
    # into `apt list --upgradable`
    # and change the number of lines to substract from 0 to 1
    widget.CheckUpdates(
        **widget_defaults,
        **color_scheme,
        distro="Ubuntu",
        colour_no_updates=color_scheme["foreground"],
        colour_have_updates=theme["orange"],
    ),

    separator(right_looking = False),

    widget.Clock(
        **widget_defaults,
        **color_scheme,
        format='%H:%M:%S %a %d.%m.%Y',
    ),

    separator(right_looking = False),

    widget.Systray(
        icon_size=24,
        **widget_defaults,
        **color_scheme,
    ),

    widget.Spacer(
        length = 16,
        **color_scheme,
    ),

    separator(right_looking = False),

    # Volume icon and widget
    widget.TextBox(
        u'\ue8ef',
        **icon_defaults,
        **color_scheme,
    ),
    widget.Volume(
        **widget_defaults,
        **color_scheme,
        device = "sysdefault",
        format='[{percent:2.0%}]  '
    ),

    separator(right_looking = False),
    
    # Brightness icon and widget
    widget.TextBox(
        u'\ue8cf',
        **icon_defaults,
        **color_scheme,
    ),
    widget.Backlight(
        **widget_defaults,
        **color_scheme,
        backlight_name='intel_backlight',
        format='[{percent:2.0%}]  '
    ),

    separator(right_looking = False),
    
    # Battery icon and widget
    widget.TextBox(
        u'\ue832',
        **icon_defaults,
        **color_scheme
    ), 
    widget.Battery(
        **widget_defaults,
        **battery_widget_defaults,
        **color_scheme,
        battery=0
    ),

    separator(right_looking = False),
    
    # Battery icon and widget
    widget.TextBox(
        u'\ue832', 
        **icon_defaults,
        **color_scheme,
    ),
    widget.Battery(
        **widget_defaults,
        **battery_widget_defaults,
        **color_scheme,
        battery=1
    ),

    separator(right_looking = False),
    
    widget.CPUGraph(
        **widget_defaults,
        **color_scheme,
        frequency=0.33,
        samples=300,
        border_width=0,
        line_width=0,
        fill_color=theme['yellow'],
        margin_x=12
    ),
]

# Second screen bar
separator.current_scheme = 0

second_bar_widgets = [
    widget.GroupBox(
        **widget_defaults,
        **color_scheme,
    ),

    separator(),

    widget.Spacer(
        length = 16,
        **color_scheme,
    ),

    widget.WindowName(
        **widget_defaults,
        **color_scheme,
    ),

    separator(right_looking = False),


    widget.CurrentScreen(
        **widget_defaults,
        **color_scheme,
        active_text = "active",
        inactive_text = "inactive"
    ),
]

screens = [
    Screen(
        bottom=bar.Bar(
            bar_widgets,
            24,
        ),
    ),
]

def get_num_monitors():
    num_monitors = 0
    try:
        display = xdisplay.Display()
        screen = display.screen()
        resources = screen.root.xrandr_get_screen_resources()

        for output in resources.outputs:
            monitor = display.xrandr_get_output_info(output, resources.config_timestamp)
            preferred = False
            if hasattr(monitor, "preferred"):
                preferred = monitor.preferred
            elif hasattr(monitor, "num_preferred"):
                preferred = monitor.num_preferred
            if preferred:
                num_monitors += 1
    except Exception as e:
        # always setup at least one monitor
        return 1
    else:
        return num_monitors

if get_num_monitors() > 1:
    screens.append(
            Screen(
                 top=bar.Bar(
                 second_bar_widgets,
                 24,
            ),
        )
    )

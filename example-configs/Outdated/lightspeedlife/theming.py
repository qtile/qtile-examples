from re import findall
from os import path
from io import open

HOME = path.expanduser('~/')
CONFIG = HOME + '.config/'
Q_CONFIG = CONFIG + 'qtile/'
Q_THEMES = Q_CONFIG + 'themes/'

#THEMING
#
# TODO: impliment autosetting of 'urgent' color to something disharmonious
# 

class Themer:
    def __init__(self, path):
        if '.xcs' in path:
            theme_file = open(path, 'r')
            self._theme = dict(
                findall(r'(^\w*)=(\w*)', theme_file)
                )
            theme_file.close()
        elif '.txt' in path:
            theme_file = open(path, 'r')
            self._theme = dict(
                #Getting color names and values from every line that doesn't begin with 
                #'!' in .Xresources
                findall(r'[^!]\*?(\w*)\:\s*#?(.*)', theme_file.read())
                )
            theme_file.close()

        if 'cursorColor' not in self._theme:
            self._theme.update({ 'cursorColor': self._theme['color4']})

        self._layouts = {
            'bg_color': self._theme['foreground'],
            'active_bg': self._theme['color6'],
            'active_fg': self._theme['color14'],
            'inactive_bg': self._theme['color4'],
            'inactive_fg': self._theme['color12'],
            'border_focus': self._theme['color14'],
            'border_focus_fixed': self._theme['color14'],
            'border_focus_stack': self._theme['color14'],
            'border_normal': self._theme['color4'],
            'border_normal_fixed': self._theme['color4'],
            'border_normal_stack': self._theme['color4'],
            'border_width': 8,
            'border_width_single': 0,
            'single_border_width': 0,
            'max_border_width': 0,
            'fullscreen_border_width': 0,
            'fontsize': 10,
            'padding_left': 0,
            'grow_amount': 10,                           #Default: 10
            'lower_right': True,                         #Defaul: True
            'margin': 25,                                #Default: 0
            'ratio': 0.6,                                #Default: 1.6
            'insert_position': 0,                        #Default: 0
            }


        self._widgets = {
            'background': self._theme["background"],
            'foreground': self._theme["foreground"],
            'highlight_color': [self._theme['color9'], self._theme['color14']],
            'highlight_method': 'border',
            'margin_x': 8,
            'margin_y': 0,
            'spacing': 0,
            'padding': 0,
            'rounded': False,
            'borderwidth': 2,
            'border': self._theme['foreground'],
            'border_color': self._theme["foreground"],
            'color_break': self._theme['color10'],
            'active': self._theme["foreground"],
            'color_active': self._theme['background'],
            'inactive': self._theme['foreground'],
            'color_inactive': self._theme['foreground'],
            'this_current_screen_border': self._theme['foreground'],
            'other_current_screen_border': self._theme['foreground'],
            'this_screen_border': self._theme['foreground'],
            'other_screen_border': self._theme['foreground'],
            'opacity': 0.5,
            # Get just the font name (second field) no more
            'font': findall('\-\w*\-([^-]*)\-.*', self._theme['font'])[0],
            'fontsize': 11,
            'cursor_color': self._theme['cursorColor'],
            'fontshadow': None,
        }

    @property
    def layouts(self):
        return self._layouts
    
    @property
    def widgets(self):
        return self._widgets
        
    @property
    def theme(self):
        return self._theme

 
theme_list = {
    'eighties.light': Themer(Q_THEMES + 'eighties.light.txt'),
    'base32_grayscale01': Themer(Q_THEMES + 'base32_grayscale01.txt'),
    'VisiBlue': Themer(Q_THEMES + 'VisiBlue.txt'),
    'VisiBlue02': Themer(Q_THEMES + 'VisiBlue02.txt'),
    'Muzieca mono': Themer(Q_THEMES + 'Muzieca mono.txt'),
    'astromouse': Themer(Q_THEMES + 'astromouse.txt'),
    'dkeg_redphoenix': Themer(Q_THEMES + 'dkeg - redphoenix.txt'),
    'dkeg_citystreets': Themer(Q_THEMES + 'dkeg - citystreets.txt'),
    'euphrasia': Themer(Q_THEMES + 'euphrasia.txt'),
    'jwr-dark': Themer(Q_THEMES + 'jwr-dark.txt'),
    'mostly-bright': Themer(Q_THEMES + 'mostly-bright.txt'),
    'yousai': Themer(Q_THEMES + 'yousai.txt'),
    'space_amoled01': Themer(Q_THEMES + 'space_amoled01.txt'),
    'grayscale_light01': Themer(Q_THEMES + 'grayscale_light01.txt'),
}
theme = theme_list['base32_grayscale01']

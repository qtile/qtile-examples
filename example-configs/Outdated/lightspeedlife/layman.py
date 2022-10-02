# import logging

# LAYMAN
# ======
# > Configure groups, layouts, keys--dynamically.
#
# TODO (M, 1):
# * Impliment 'last group' toggle switcher

class layMan:
    """manages keybinds based on layouts, groups. May manage the layouts and
    groups at some time in the future as well, or other somesuch on-the-fly
    layout generation beyond what is available with the standard qtile libs.

    for keybinds, stores keys in a hidden _keys attribute. The keys property
    has methods for setting and getting this. In future versions of this class,
    Setters may check for conflicts before setting, and there might be some
    fancy layout manipulation and/or default application starting.
    """
    def __init__(self, const_keys, const_mouse,
        layout_keys={}, groups_keys={}):
        self._const_keys = const_keys
        self._const_mouse = const_mouse
        self._layout_keys = layout_keys
        self._groups_keys = groups_keys
        self._keys = self._const_keys
        self._mouse = self._const_mouse
        self._current_layout = None
        self._current_group = None

    @property
    def current_layout(self):
        return self._current_layout

    @property
    def current_group(self):
        return self._current_group
    
    @property
    def layout_group(self):
        return (self._current_layout, self._current_group)

    @layout_group.setter
    def layout_group(self, layout_group):
        self._current_layout, self._current_group = layout_group
    
    @property
    def mouse(self):
        return self._mouse

    @mouse.setter
    def mouse(self, bindings):
        self._mouse = bindings
    
    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, keys_list):
        self._keys = keys_list
        
    def configure(self):
        self._keys = self._const_keys
        # if the current layout has custom keys, set them:
        if getattr(self._current_layout, 'name', None) in self._layout_keys:
            print('applying layout... ', self._current_layout.name)
            print('agregando: ', self._layout_keys[self._current_layout.name])
            self._keys.extend(self._layout_keys[self._current_layout.name])
        else:
            self._keys.extend(self._layout_keys['ambiguous'])
        # if the current group(s) has custom keys, append those too:
        if getattr(self._current_group, 'name', None) in self._groups_keys:
            self._keys.extend(*self._groups_keys[self._current_group])

        self._mouse = self._const_mouse
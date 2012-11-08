import os
import subprocess

import cairo

from libqtile.widget import base
from libqtile import manager, bar


__all__=[
    'NetworkStatus',
]

class NetworkStatus(base._TextBox):
    '''Widget that displays network status
       if theme_path is set it draws the
       widget as an icon'''

    defaults = manager.Defaults(
        ("font", "Arial", "Text font"),
        ("fontsize", None, "Font pixel size. Calculated if None."),
        ("padding", 3, "Padding left and right. Calculated if None."),
        ("background", None, "Background colour."),
        ("foreground", "#ffffff", "Foreground colour."),
        ("theme_path", None, "Path of the icons"),
        ("update_interval", 0.2, "Update time in seconds."),
    )
    def __init__(self, **config):
        base._TextBox.__init__(self, 'NET', width=bar.CALCULATED, **config)
        if self.theme_path:
            self.width_type = bar.STATIC
            self.width = 0
        self.surfaces = {}
        self.netstate = "disconnected"

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        if self.theme_path:
            self.setup_images()
        self.timeout_add(self.update_interval, self.update)

    def update(self):
        networkprocess = subprocess.Popen(['nmcli', '-f', 'state', '-t', 'nm'],
                                          stdout = subprocess.PIPE)
        state = networkprocess.communicate()
        
        if state[0] != self.netstate:
            self.netstate = state[0]
            self.draw()
        return True

    def setup_images(self):
        for img_name in ('network-online', 'network-acquiring',
                         'network-offline'):
            try:
                img = cairo.ImageSurface.create_from_png(
                    os.path.join(self.theme_path,
                                 '%s.png' % img_name))
            except cairo.Error, error:
                self.theme_path = None
                self.width_type = bar.CALCULATED
                self.qtile.log.add(error)
                self.qtile.log.add('Switching to text mode')
                return
            input_width = img.get_width()
            input_height = img.get_height()

            sp = input_height/float(self.bar.height-1)

            width = input_width / sp
            if width > self.width:
                self.width = int(width) + self.actual_padding * 2

            imgpat = cairo.SurfacePattern(img)

            scaler = cairo.Matrix()

            scaler.scale(sp, sp)
            scaler.translate(self.actual_padding*-1, 0)
            imgpat.set_matrix(scaler)

            imgpat.set_filter(cairo.FILTER_BEST)
            self.surfaces[img_name] = imgpat

    def draw(self):
        if self.theme_path:
            self.drawer.clear(self.bar.background)
            if 'disconnected' in self.netstate:
                img_name = 'network-offline'
            elif 'connected' in self.netstate:
                img_name = 'network-online'
            else:
                img_name = 'network-acquiring'

            self.drawer.ctx.set_source(self.surfaces[img_name])
            self.drawer.ctx.paint()
            self.drawer.draw(self.offset, self.width)
        else:
            if "disconnected" in self.netstate:
                self.text = '!'
            else:
                self.text = '(<.>)'
            base._TextBox.draw(self)

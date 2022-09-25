from libqtile import layout

from plasma import Plasma

layout_defaults = dict(
    margin = 5,
    border_width = 3,
    border_focus="#FFFFFF",
    grow_amount = 3,
    )

floating_layout_defaults = layout_defaults.copy()
floating_layout_defaults["border_width"] = 0

layouts = [
    layout.Max(**layout_defaults),
    layout.Bsp(name="bsp", **layout_defaults),
    # Plasma(**layout_defaults),

    # layout.Stack(num_stacks=2),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

floating_layout = layout.Floating(auto_float_typesR=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'notify'},
    {'wmclass': 'popup_menu'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitkm
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
], **floating_layout_defaults)

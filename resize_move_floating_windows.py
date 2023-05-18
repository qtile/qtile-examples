"""
This plugin exports 2 functions - resize and move.

-- resize --
Resize floating windows & changes bsp resize behaviour to act more like columns
(if window is not floating & layout not bsp falls back to standard layout resize)

Floating resize controls
down key grows window vertically
Up key shrinks window verically
right key grows window horizontally
left key shrinks window horizontally

Args:
    direction: "left", "right", "up", "down"
    (optional) floating_grow_amount: amount to grow floating windows by (defaults to 50)

Example usage:

    import resize_move_floating_windows.py

    keys.extend([
        Key([mod, "control"], 'k', lazy.function(resize_move_floating_windows.resize("up")),
        Key([mod, "control"], 'j', lazy.function(resize_move_floating_windows.resize("down")),
        Key([mod, "control"], 'h', lazy.function(resize_move_floating_windows.resize("left")),
        Key([mod, "control"], 'l', lazy.function(resize_move_floating_windows.resize("right")),
    ])

--move--
Move floating windows (if window is not floating falls back to standard layout shuffle)
                                                                                        
Args:
    direction: "left", "right", "up", "down"
    (optional) floating_move_amount: amount to move floating windows by (defaults to 50)

Example usage:

    import resize_move_floating_windows.py

    keys.extend([
        Key([mod, "shift"], 'k', lazy.function(resize_move_floating_windows.move("up")),
        Key([mod, "shift"], 'j', lazy.function(resize_move_floating_windows.move("down")),
        Key([mod, "shift"], 'h', lazy.function(resize_move_floating_windows.move("left")),
        Key([mod, "shift"], 'l', lazy.function(resize_move_floating_windows.move("right")),
    ])
"""

def resize(qtile, direction, floating_grow_amount = 50):
    """
    Resize floating windows & changes bsp resize behaviour to act more like columns
    (if window is not floating & layout not bsp falls back to standard layout resize)
    
    Floating resize controls
    down key grows window vertically
    Up key shrinks window verically
    right key grows window horizontally
    left key shrinks window horizontally
    
    Args:
        direction: "left", "right", "up", "down"
        (optional) floating_grow_amount: amount to grow floating windows by (defaults to 50)
    
    Example usage:
    
        import resize_move_floating_windows.py
    
        keys.extend([
            Key([mod, "control"], 'k', lazy.function(resize_move_floating_windows.resize("up")),
            Key([mod, "control"], 'j', lazy.function(resize_move_floating_windows.resize("down")),
            Key([mod, "control"], 'h', lazy.function(resize_move_floating_windows.resize("left")),
            Key([mod, "control"], 'l', lazy.function(resize_move_floating_windows.resize("right")),
        ])
    """
    def resize_floating():
        if direction == "down":
            window.cmd_resize_floating(0,int(floating_grow_amount))
        elif direction == "right":
            window.cmd_resize_floating(int(floating_grow_amount),0)
            window.cmd_move_floating(-int(floating_grow_amount/2), 0)
        elif direction == "up":
            window.cmd_resize_floating(0,-int(floating_grow_amount))
        elif direction == "left":
            window.cmd_resize_floating(-int(floating_grow_amount),0)
            window.cmd_move_floating(int(floating_grow_amount/2), 0)
            window.cmd_is_visible()
    
    def resize_bsp():
        layout = qtile.current_layout
        child = layout.current
        parent = child.parent
        while parent:
            if child in parent.children:
                layout_all = False

                if (direction == "left" and parent.split_horizontal) or (
                        direction == "up" and not parent.split_horizontal):
                    parent.split_ratio = max(
                        5, parent.split_ratio - layout.grow_amount)
                    layout_all = True
                elif (direction == "right" and parent.split_horizontal) or (
                        direction == "down" and not parent.split_horizontal):
                    parent.split_ratio = min(
                        95, parent.split_ratio + layout.grow_amount)
                    layout_all = True
                if layout_all:
                    layout.group.layout_all()
                    break
            child = parent
            parent = child.parent

    window = qtile.current_window
    current_layout = qtile.current_layout.info()["name"]
    if window.floating:
        resize_floating()

    elif current_layout == "bsp":
        resize_bsp()

    else: # Standard layout resize
        grow_layout = {
            "up": qtile.current_layout.cmd_grow_up,
            "right": qtile.current_layout.cmd_grow_right,
            "down": qtile.current_layout.cmd_grow_down,
            "left": qtile.current_layout.cmd_grow_left,
        }
        grow_layout[direction]()


def move(qtile, direction, floating_move_amount=50):
    """
    Move floating windows (if window is not floating falls back to standard layout shuffle)
                                                                                            
    Args:
        direction: "left", "right", "up", "down"
        (optional) floating_move_amount: amount to move floating windows by (defaults to 50)
    
    Example usage:
    
        import resize_move_floating_windows.py
    
        keys.extend([
            Key([mod, "shift"], 'k', lazy.function(resize_move_floating_windows.move("up")),
            Key([mod, "shift"], 'j', lazy.function(resize_move_floating_windows.move("down")),
            Key([mod, "shift"], 'h', lazy.function(resize_move_floating_windows.move("left")),
            Key([mod, "shift"], 'l', lazy.function(resize_move_floating_windows.move("right")),
        ])
    """
    window = qtile.current_window
    if window.floating:
        # Moves floating windows
        if direction == "down":
            window.cmd_move_floating(0,floating_move_amount)
        elif direction == "right":
            window.cmd_move_floating(floating_move_amount,0)
        elif direction == "up":
            window.cmd_move_floating(0,-floating_move_amount)
        elif direction == "left":
            window.cmd_move_floating(-floating_move_amount,0)
    else:
        move_layout = {
            "up": qtile.current_layout.cmd_shuffle_up,
            "right": qtile.current_layout.cmd_shuffle_right,
            "down": qtile.current_layout.cmd_shuffle_down,
            "left": qtile.current_layout.cmd_shuffle_left,
        }
        move_layout[direction]()

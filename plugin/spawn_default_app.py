"""
Spawn the default app set for each group.

For example, if you set up your first group with a default
app of "firefox", your second group with a default app of
"vscode", and didn't set a default app for the remainder of 
your groups, then when you switch to the first group and call
this function, it will spawn firefox. When you switch to the
second group and call this function, it will spawn vscode.
When you switch to any other group and call this function, it
will spawn the application specified by unset_default_app.

Setup:

    To start, define a list of default apps the same length
    as your list of groups. If you don't want to set a default
    app for a group, set the value to None. You can then call
    this function from your keybinds by passing in your list
    of groups and default apps to spawn the default app for the
    current group.

Usage:

    from spawn_default_app import spawn_default_app

    run_launcher = "<your_run_launcher_here>"

    default_apps = ["firefox", "code", "nemo", None, None, "firefox", None, "discord", "pavucontrol", "terminator -e bpytop",]

    keys.extend([
        Key([mod], "t", lazy.function(spawn_default_app, groups, default_apps, unset_default_app=run_launcher), desc="Spawn the default app for the current group")
    ])
"""

from libqtile.lazy import lazy

def spawn_default_app(qtile, groups: list, default_apps: list[str], use_run_as_unset_default: bool = False, unset_default_app: str = None) -> None:
    def get_index(current_group_name: str) -> None:
        if groups:
            for i in range(len(groups)):
                if groups[i].name == current_group_name:
                    return i
            return None
        else:
            return None

    group_index = get_index(qtile.current_group.name) if qtile.current_group is not None else None
    if qtile.current_group is not None and group_index is not None and default_apps is not None and default_apps[group_index] is not None:
        app = default_apps[group_index]
        qtile.cmd_spawn(app)
    else:
        if use_run_as_unset_default or unset_default_app is None:
            lazy.spawncmd()
        else:
            qtile.cmd_spawn(unset_default_app)


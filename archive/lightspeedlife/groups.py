from libqtile.config import Group, ScratchPad, DropDown

TERMUX = "termite -e tmux"

# GROUPS
# 
def init_groups():
	return [
            Group("!nfo", init=True, persist=True, label='!'),
            Group(">kek", init=True, persist=True, label="@"),
            Group("H4XX", init=True, persist=True, label="#"),
            Group("$RIPTZ", init=True, persist=True, label="$"),
            Group(".conf", init=True, persist=True, label="%"),
            Group("X_x", init=True, persist=True, label="🖻🖻^"),
            Group("browse", init=True, persist=True, label="𑙩𑙩𑙩𑙩&"),
            Group(':D', init=True, persist=True, label='*'),
            Group('/3/', init=True, persist=True, label='9'),
            Group('/gd/', init=True, persist=True, label='0'),
            ScratchPad('scratch', [
                    DropDown('term', TERMUX),
                ]),
    ]

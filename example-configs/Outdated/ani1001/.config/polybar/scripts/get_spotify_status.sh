#!/bin/bash

# The name of polybar bar which houses the main spotify module and the control modules.
PARENT_BAR="mainbar-i3"

# Set the source audio player here.
# Players supporting the MPRIS spec are supported.
# Examples: spotify, vlc, chrome, mpv and others.
# Use `playerctld` to always detect the latest player.
# See more here: https://github.com/altdesktop/playerctl/#selecting-players-to-control
PLAYER="spotify"

# Format of the information displayed
# Eg. {{ artist }} - {{ album }} - {{ title }}
# See more attributes here: https://github.com/altdesktop/playerctl/#printing-properties-and-metadata
FORMAT="{{ title }} - {{ artist }}"

PLAYERCTL_STATUS=$(playerctl --player=$PLAYER status 2>/dev/null)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    STATUS=$PLAYERCTL_STATUS
else
    STATUS="No player is running"
fi

if [ "$1" == "--status" ]; then
    echo "$STATUS"
else
    if [ "$STATUS" = "Stopped" ]; then
        echo "No music is playing"
    # A note on hooks:
    # In the polybar config, they are supposed to be zero-indexed.
    # When making IPC calls, 1-based index numbers are to be used.
    # So don't get confused with hook value as 2.
    elif [ "$STATUS" = "Paused"  ]; then
        polybar-msg -p "$(pgrep -f "polybar $PARENT_BAR")" hook spotify-play-pause 2 1>/dev/null 2>&1
        playerctl --player=$PLAYER metadata --format "$FORMAT"
    elif [ "$STATUS" = "No player is running"  ]; then
        echo $STATUS
    else
        polybar-msg -p "$(pgrep -f "polybar $PARENT_BAR")" hook spotify-play-pause 1 1>/dev/null 2>&1
        playerctl --player=$PLAYER metadata --format "$FORMAT"
    fi
fi

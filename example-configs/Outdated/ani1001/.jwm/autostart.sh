#!/bin/bash
# more info on http://joewing.net/projects/jwm/config-2.3.html
function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}
#autorandr horizontal
#change your keyboard if you need it
#setxkbmap -layout be
# start ArcoLinux Welcome  App
#dex $HOME/.config/autostart/arcolinux-welcome-app.desktop
xsetroot -cursor_name left_ptr &
#sxhkd -c ~/.jwm/sxhkd/sxhkdrc &
run volumeicon &
#run variety &
run nm-applet &
#run pamac-tray &
#run xfce4-power-manager &
#numlockx on &
#blueberry-tray &
run picom &
run lxpolkit &
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
#/usr/lib/xfce4/notifyd/xfce4-notifyd &
#run nitrogen --restore &
#run caffeine &
#run vivaldi-stable &
#run firefox &
#run thunar &
#run dropbox &
#run insync start &
#run discord &
#run spotify &
#run atom &
run urxvtd -q -o -f &
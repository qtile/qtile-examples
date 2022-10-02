(in-package :stumpwm)

;; Autostart applications in the background
(run-shell-command "nitrogen --restore")
(run-shell-command "picom -b")
(run-shell-command "lxpolkit")
(run-shell-command "xsetroot -cursor_name left_ptr")
(run-shell-command "urxvtd -q -o -f")
(run-shell-command "emacs --daemon")

;; Bugfix for scrolling doesn't work with an external mouse in GTK+3 apps
(setf (getenv "GDK_CORE_DEVICE_EVENTS") "1")

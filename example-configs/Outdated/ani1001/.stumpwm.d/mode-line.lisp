(in-package :stumpwm)

;; Mode-line format
(setf *screen-mode-line-format* (list " ")
      *screen-mode-line-format* (list "[^B%n^b] %W^>%d")
      *mode-line-position* :bottom
      *mode-line-border-width* 1
      *mode-line-pad-x* 1
      *mode-line-pad-y* 0
      *mode-line-background-color* nord0
      *mode-line-foreground-color* nord4
      *mode-line-border-color* nord13
      *mode-line-timeout* 2
      *window-format* "%m%n%s%c"
      *time-modeline-string* "%a %b %e %k:%M")

;; Starts the mode-line
(enable-mode-line (current-screen) (current-head) t)

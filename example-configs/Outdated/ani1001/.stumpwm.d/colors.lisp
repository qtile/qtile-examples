(defvar nord0 "#2e3440")
(defvar nord1 "#3b4252")
(defvar nord2 "#434c5e")
(defvar nord3 "#4c566a")
(defvar nord4 "#d8dee9")
(defvar nord5 "#e5e9f0")
(defvar nord6 "#eceff4")
(defvar nord7 "#8fbcbb")
(defvar nord8 "#88c0d0")
(defvar nord9 "#81a1c1")
(defvar nord10 "#5e81ac")
(defvar nord11 "#bf616a")
(defvar nord12 "#d08770")
(defvar nord13 "#ebcb8b")
(defvar nord14 "#a3be8c")
(defvar nord15 "#b48ead")

(setq *colors*
      `(,nord1   ;; 0 black
        ,nord11  ;; 1 red
        ,nord14  ;; 2 green
        ,nord13  ;; 3 yellow
        ,nord10  ;; 4 blue
        ,nord14  ;; 5 magenta
        ,nord8   ;; 6 cyan
        ,nord5)) ;; 7 white

(when *initializing*
  (update-color-map (current-screen)))

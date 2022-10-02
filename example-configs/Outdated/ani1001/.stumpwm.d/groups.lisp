(in-package :stumpwm)

;; Rename the default group and define new groups
;; (grename "WWW")
;; (gnewbg "IRC")
;; (gnewbg "Email")
;; (gnewbg "Code")
;; (gnewbg "Shell")

(setf (group-name (first (screen-groups (current-screen)))) "WWW")
  (run-commands "gnewbg IRC" "gnewbg Email" "gnewbg Code" "gnewbg Shell")

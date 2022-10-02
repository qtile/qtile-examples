(in-package :stumpwm)

;; change the prefix key to something else
(set-prefix-key (kbd "C-z"))

;; Read some doc
(define-key *root-map* (kbd "d") "exec gv")
;; Browse somewhere
(define-key *root-map* (kbd "b") "colon1 exec firefox http://duckduckgo.com/?=")
;; Ssh somewhere
(define-key *root-map* (kbd "C-s") "colon1 exec urxvtc -e ssh ")
;; Lock screen
(define-key *root-map* (kbd "C-l") "exec slock")

;; C-t M-s is a terrble binding, but you get the idea.
(define-key *root-map* (kbd "M-s") "duckduckgo")
(define-key *root-map* (kbd "i") "imdb")

;; Quit stumpwm
(define-key *root-map* (kbd "C-q") "quit")
;; Reload stumpwm
(define-key *root-map* (kbd "C-r") "reload")

;; Launch dmenu
(define-key *top-map* (kbd "C-d") "exec dmenu_run")
;; Launch rofi
(define-key *top-map* (kbd "C-RET") "exec rofi -show run")

;; Launch xterm
(define-key *top-map* (kbd "C-X") "exec xterm")
;; Launch rxvt-unicode client
(define-key *top-map* (kbd "C-C") "exec urxvtc")
;; Launch terminal
(define-key *top-map* (kbd "M-RET") "exec alacritty")

;; Launch emacs
(define-key *top-map* (kbd "C-E") "exec emacs")
;; Launch emacsclient
(define-key *top-map* (kbd "C-e") "exec emacsclient -c -a 'emacs'")

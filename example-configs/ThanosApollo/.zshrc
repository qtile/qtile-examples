
# Starting message
starting(){
	neofetch | lolcat
	figlet -c Apo11o | lolcat
}
###
export PATH="$HOME/.emacs.d/bin:$PATH"
fpath=(/home/apollo/.cache/paru/clone/zsh-completions-git/zsh-completions $fpath)
## PROMPT
eval "$(starship init zsh)"
# enable hook method
autoload add-zsh-hook

# enable and configure vcs_info
autoload -Uz vcs_info
add-zsh-hook precmd vcs_info
zstyle ':vcs_info:*' enable hg git cvs svn
zstyle ':vcs_info:*' formats '%s|%b|%a|%i|%R|%r|%S|%m'
export PATH="$HOME/.emacs.d/bin:$PATH"

#Neovim > Vim
alias vim='nvim'
alias vi='nvim'

#git
alias config='/usr/bin/git --git-dir=$HOME/Developer/config/ --work-tree=$HOME'
alias ga='git add'
alias gaa='git add .'
alias gc='git commit -m'
alias gp='git push -u origin'
alias gpm='git push -u origin master'
alias gpd='git push -u origin developer'
alias gs='git status'
alias cpm='config push -u origin master'
alias ca='config add'
alias cs='config status'
alias cc='config commit -m'

#pacman | yay
alias yeet='yay -Rsc'

# weather
alias weather="curl wttr.in"

#aliases
alias ls='ls -la --color=auto'
alias sb='sudo systemctl start bluetooth'
alias mykeys='setxkbmap -option caps:escape'
alias logout='pkill -U $USER'
alias neofetch='neofetch | lolcat'
alias b='bluetoothctl'
alias ba='bluetooth-autoconnect'
alias music='mocp'
alias yt="yt-dlp"
alias c="pavucontrol"
alias r="ranger"

#Autocompletion
autoload -Uz compinit
compinit
zstyle ':completion:*' menu select
zstyle ':completion::complete:*' gain-privileges 1

#Keybindings
typeset -g -A key

key[Home]="${terminfo[khome]}"
key[End]="${terminfo[kend]}"
key[Insert]="${terminfo[kich1]}"
key[Backspace]="${terminfo[kbs]}"
key[Delete]="${terminfo[kdch1]}"
key[Up]="${terminfo[kcuu1]}"
key[Down]="${terminfo[kcud1]}"
key[Left]="${terminfo[kcub1]}"
key[Right]="${terminfo[kcuf1]}"
key[PageUp]="${terminfo[kpp]}"
key[PageDown]="${terminfo[knp]}"
key[Shift-Tab]="${terminfo[kcbt]}"

# setup key accordingly
[[ -n "${key[Home]}"      ]] && bindkey -- "${key[Home]}"       beginning-of-line
[[ -n "${key[End]}"       ]] && bindkey -- "${key[End]}"        end-of-line
[[ -n "${key[Insert]}"    ]] && bindkey -- "${key[Insert]}"     overwrite-mode
[[ -n "${key[Backspace]}" ]] && bindkey -- "${key[Backspace]}"  backward-delete-char
[[ -n "${key[Delete]}"    ]] && bindkey -- "${key[Delete]}"     delete-char
[[ -n "${key[Up]}"        ]] && bindkey -- "${key[Up]}"         up-line-or-history
[[ -n "${key[Down]}"      ]] && bindkey -- "${key[Down]}"       down-line-or-history
[[ -n "${key[Left]}"      ]] && bindkey -- "${key[Left]}"       backward-char
[[ -n "${key[Right]}"     ]] && bindkey -- "${key[Right]}"      forward-char
[[ -n "${key[PageUp]}"    ]] && bindkey -- "${key[PageUp]}"     beginning-of-buffer-or-history
[[ -n "${key[PageDown]}"  ]] && bindkey -- "${key[PageDown]}"   end-of-buffer-or-history
[[ -n "${key[Shift-Tab]}" ]] && bindkey -- "${key[Shift-Tab]}"  reverse-menu-complete

if (( ${+terminfo[smkx]} && ${+terminfo[rmkx]} )); then
	autoload -Uz add-zle-hook-widget
	function zle_application_mode_start { echoti smkx }
	function zle_application_mode_stop { echoti rmkx }
	add-zle-hook-widget -Uz zle-line-init zle_application_mode_start
	add-zle-hook-widget -Uz zle-line-finish zle_application_mode_stop
fi

## Autoload
autoload -Uz up-line-or-beginning-search down-line-or-beginning-search
zle -N up-line-or-beginning-search
zle -N down-line-or-beginning-search

[[ -n "${key[Up]}"   ]] && bindkey -- "${key[Up]}"   up-line-or-beginning-search
[[ -n "${key[Down]}" ]] && bindkey -- "${key[Down]}" down-line-or-beginning-search

#Syntax highlight & autosuggestions
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

starting

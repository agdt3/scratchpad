#Import .bashrc
if [ -f ~/.bashrc ]; then
  source ~/.bashrc
fi

#Functions
branch() {
  git rev-parse --abbrev-ref HEAD
}

# Color
export CLICOLOR=true
export GREP_OPTIONS='--color=auto'
export TERM=xterm-256color

# Aliases
alias l='ls'
alias la='ls -laht'
alias grep='grep ${GREP_OPTIONS}'
alias gco='git checkout'
alias gd='git diff'
alias gl='git log --decorate'
alias gs='git status'
alias pull='git pull origin $(git rev-parse --abbrev-ref HEAD)'
alias push='git push origin $(git rev-parse --abbrev-ref HEAD)'
alias fetch='git fetch origin'
alias python='python3'
alias td='todo.sh'

# Docker aliases
alias dcls='docker container ls -a'
alias dils='docker image ls -a'
alias dvls='docker volume ls'
alias dls='docker container ls -a && echo -e "\n" && docker image ls -a && echo -e "\n" && docker volume ls'
alias dpruneall='yes | docker container prune && yes | docker image prune && yes | docker volume prune'

# Vim
alias v='vim -O'

#!/usr/bin/bash
#
# set-pywal - use pywal on any desktop with any wallpaper application
#
# Copyright (C) 2019 Erik Dubois <erik.dubois@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

shopt -s extglob

declare -r myname='set-pywal'
declare -r myver='1.1.1'

usage() {
	printf "%s v%s\n" "${myname}" "${myver}"
	echo
	printf "%s Pywal will use the wallpaper of variety"
	echo
	echo
	echo "    -h, --help        display this help message and exit"
	echo "    -v, --version     display version information and exit"
	echo
	echo "These options can be passed to the script:"
	echo "    -f,     favorite"
	echo "    -p,     previous"
	echo "    -n,     next"
  echo "    -u,     update"
}

version() {
	printf "%s %s\n" "$myname" "$myver"
	echo 'Copyright (C) 2012-2013 Erik Dubois <erik.dubois@gmail.com>'
}


# Verifies if 'python-pywal' is installed
if ! type "wal" >> /dev/null 2>&1; then
    echo -e \
        "\nThis script requires 'python-pywal' to be installed\n" \
        "\rPlease install it and rerun this script."
fi


# Verifies if 'variety' is installed
if ! type "variety" >> /dev/null 2>&1; then
    echo -e \
        "\nThis script requires 'variety' to be installed\n" \
        "\rPlease install it and rerun this script."
fi

if ! type "wal" >> /dev/null 2>&1 || ! type "variety" >> /dev/null 2>&1  ; then
    exit
fi

find-wallpaper(){
	current_wallpaper=$(cat $HOME/.config/variety/wallpaper/wallpaper.jpg.txt)
}

set-variety() {
	case "$1" in
		-f) variety -f ;;
		-p) variety -p ;;
		-n) variety -n ;;
	esac
}

set-wal(){
	wal -i $current_wallpaper
}

setwal() {
	case "$1" in
		-f) set-variety -f && find-wallpaper && sleep 1 && set-wal && exit;;
		-p) set-variety -p && find-wallpaper && sleep 1 && set-wal && exit;;
		-n) set-variety -n && find-wallpaper && sleep 1 && set-wal && exit;;
		-u) find-wallpaper && set-wal ;;
	esac
}

while (( "$#" )); do
	case "$1" in
		-h|--help) usage; exit ;;
		-v|--version) version; exit ;;
		*) setwal $1; exit  ;;
	esac
done

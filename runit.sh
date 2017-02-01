#! /bin/bash
#
# runit.sh
#
# Copyright © 2017 Mathieu Gaborit (matael) <mathieu@matael.org>
#
#
# Distributed under WTFPL terms
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

# shameless-ly pumped from https://gist.github.com/inexorabletash/9122583
function tstyle {
	while [ $# -gt 0 ]; do
		case "$1" in
			reset)       echo -ne "\E[0m" ;;  # terminal default

			bold)        echo -ne "\E[1m" ;;
			faint)       echo -ne "\E[2m" ;;  # not widely supported (gnome-terminal does)
			italic)      echo -ne "\E[3m" ;;  # not widely supported
			underline)   echo -ne "\E[4m" ;;
			blink)       echo -ne "\E[5m" ;;  # not widely supported
			blinkfast)   echo -ne "\E[6m" ;;  # not widely supported
			negative)    echo -ne "\E[7m" ;;
			conceal)     echo -ne "\E[8m" ;;  # not widely supported (gnome-terminal does)
			strike)      echo -ne "\E[9m" ;;  # not widely supported (gnome-terminal does)

			normal)      echo -ne "\E[22m" ;; # cancel bold/faint
			roman)       echo -ne "\E[23m" ;; # cancel italic
			nounderline) echo -ne "\E[24m" ;; # cancel underline
			noblink)     echo -ne "\E[25m" ;; # cancel blink
			positive)    echo -ne "\E[27m" ;; # cancel negative
			reveal)      echo -ne "\E[28m" ;; # cancel conceal
			nostrike)    echo -ne "\E[29m" ;; # cancel strike

			black)       echo -ne "\E[30m" ;;
			red)         echo -ne "\E[31m" ;;
			green)       echo -ne "\E[32m" ;;
			yellow)      echo -ne "\E[33m" ;;
			blue)        echo -ne "\E[34m" ;;
			magenta)     echo -ne "\E[35m" ;;
			cyan)        echo -ne "\E[36m" ;;
			white)       echo -ne "\E[37m" ;;
			xterm)       echo -ne "\E[38;5;$2m" ; shift ;;

			default)     echo -ne "\E[39m" ;;

			bgblack)     echo -ne "\E[40m" ;;
			bgred)       echo -ne "\E[41m" ;;
			bggreen)     echo -ne "\E[42m" ;;
			bgyellow)    echo -ne "\E[43m" ;;
			bgblue)      echo -ne "\E[44m" ;;
			bgmagenta)   echo -ne "\E[45m" ;;
			bgcyan)      echo -ne "\E[46m" ;;
			bgwhite)     echo -ne "\E[47m" ;;
			bgxterm)     echo -ne "\E[48;5;$2m" ; shift ;;
			bgdefault)   echo -ne "\E[49m" ;;

			*)
				echo -"ne \E[0m"
				echo "Unknown code: $token" 1>&2
				exit 1
				;;
		esac
		shift
	done
}

echo "$(tstyle blue)=>>$(tstyle white) Installing virtualenv $(tstyle reset)"
sudo pip install virtualenv

echo "$(tstyle blue)=>>$(tstyle white) Creating a virtualenv in venv $(tstyle reset)"
virtualenv -ppython3 venv
source venv/bin/activate

echo "$(tstyle blue)=>>$(tstyle white) Installing packages $(tstyle reset)"
pip install -r requirements.txt

echo "$(tstyle blue)=>>$(tstyle white) Creating DB $(tstyle reset)"
./manage.py migrate

echo "$(tstyle blue)=>>$(tstyle white) Loading features $(tstyle reset)"
./manage.py loaddata fixtures/chronology.json

echo "$(tstyle green)OK ! Everything should be fine, to start server use :$(tstyle reset)"
echo "    $(tstyle white)source venv/bin/activate; ./manage.py runserver$(tstyle reset)"

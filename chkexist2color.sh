#!/bin/sh
# ex) fontforge -script chkexist.pe build/UDEAWH-Regular.ttf|./chkexist2color.sh
n=0
while read -r ucode isexist char
do
	if [ "${isexist}" = "1" ]; then
		echo -n "$char"
	else
		# gray color
		#tput setaf 8 && echo -n "$char" && tput sgr0
		# background gray
		tput setaf 7 && tput setab 8 && echo -n "$char" && tput sgr0
	fi
	n=$(($n+1))
	if [ $n -eq 39 ]; then
		echo
		n=0
	fi
done
echo

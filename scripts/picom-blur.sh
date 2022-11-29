#!/bin/bash
if pgrep -x "picom" > /dev/null
then
	killall picom
else
	picom --blur-method=dual_kawase --backend glx
fi

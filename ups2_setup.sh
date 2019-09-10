#!/bin/bash
CONFIG="/boot/config.txt"
TITLE="GEEKWORM WORKSHOP UPS2"
BACKTITLE="GEEKWORM WORKSHOP [ GEEKWORM.COM ]"
GPIO_POWEROFF="22"
HINT="Poweroff option has been enabled!"

#dtoverlay=gpio-poweroff,gpio_pin=22
function get_gpio(){
	TEST_STRING=$(cat /boot/config.txt | grep poweroff)
	GPIO_TEMP="${TEST_STRING/dtoverlay=gpio-poweroff,gpio_pin=/}"
	if [ -n "$GPIO_TEMP" ]; then 
		GPIO_POWEROFF=$GPIO_TEMP
	fi
}
function disable_poweroff(){
	sed -i '/gpio-poweroff/d' $CONFIG
	HINT="Poweroff option has been disabled!"
}
function enable_poweroff(){
	#disable pitft overlay
	disable_poweroff
	echo "dtoverlay=gpio-poweroff,gpio_pin=$GPIO_POWEROFF" >> $CONFIG
	HINT="Poweroff option has been enabled!"
	
}

function menu_reboot(){
	if (whiptail --title "$TITLE" \
		--yes-button "Reboot" \
		--no-button "Exit" \
		--yesno "Reboot system to apply new settings?" 10 60) then
		reboot
	else
		exit 1
	fi
}
function menu_ok(){
	whiptail --title "$TITLE" --msgbox "$HINT" 10 60
	menu_main
}
function menu_gpio(){
	OPTION_BLANKING=$(whiptail --title "GPIO SELECTION" \
	--menu "Select the appropriate options:" \
	--backtitle "$BACKTITLE" \
	--nocancel \
	--default-item "1" \
	14 60 2 \
	"1" "Broadcom GPIO  #6(GPIO.22)" \
	"2" "Broadcom GPIO #13(GPIO.23)" 3>&1 1>&2 2>&3)
	return $OPTION_BLANKING
}

function menu_main(){
	OPTION=$(whiptail --title "$TITLE" \
	--menu "Select the appropriate options:" \
	--backtitle "$BACKTITLE" \
	--nocancel \
	14 60 6 \
	"1" "Select Poweroff GPIO(#6 OR #13)" \
	"2" "Enable Poweroff function" \
	"3" "Disable Poweroff function" \
	"4" "Exit"  3>&1 1>&2 2>&3)
	return $OPTION
}

if [ $UID -ne 0 ]; then
	whiptail --title "GEEKWORM WORKSHOP" \
	--msgbox "root privileges are required to run this script.\ne.g. \"sudo $0\"" 10 60
    exit 1
fi

while true
do
menu_main
case $? in
	1)
	menu_gpio
	case $? in
		1)
		GPIO_POWEROFF="22"
		;;
		2)
		GPIO_POWEROFF="23"
		;;
	esac
	;;
	2)
	enable_poweroff
	menu_ok
	;;
	3)
	disable_poweroff
	menu_ok
	;;
	4)
	menu_reboot
	echo "     [ GEEKWORM.COM ]"
	echo "https://geekworm.com/"
	exit 1
	;;
esac
done

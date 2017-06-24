#!/bin/bash

TIMEOUT=30

have_internet=$(ping -c 1 yahoo.com &>/dev/null; echo $?)

if [[ ${have_internet} -eq 0 ]]; then
        notify-send "have wifi, starting.."
else
        notify-send "sleeping ${TIMEOUT}s; no wifi"
        sleep ${TIMEOUT}s
fi

google-chrome-stable --incognito --kiosk http://localhost:8080/ &

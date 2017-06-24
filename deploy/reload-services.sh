#!/bin/bash
HOST=192.168.1.13
USER=h

ssh ${USER}@${HOST} '
  cd ${HOME}/statusboard/contrib
  ./reload.sh
  cd ${HOME}/statusboard/brightness-control
  ./reload.sh
'

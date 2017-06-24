#!/bin/bash
HOST=192.168.1.13
USER=h

scp deploy/initial_setup.sh ${USER}@${HOST}:~/
ssh ${USER}@${HOST} ./initial_setup.sh
scp -r brightness-control contrib docker-compose.yml frontend mta-service-status mta-static Makefile statusboard.env weather ${USER}@${HOST}:~/statusboard/
ssh ${USER}@${HOST} '
  cd ${HOME}/statusboard
  make build
  cd contrib/
'
scp contrib/google-chrome-stable.desktop ${USER}@${HOST}:/home/${USER}/.config/autostart/

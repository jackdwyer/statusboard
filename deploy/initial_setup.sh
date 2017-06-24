#!/bin/bash

if ! [[ -f /.done-initial-setup ]]; then
  mkdir -p "${HOME}/statusboard/"
  sudo apt-get update -y
  sudo apt-get remove -y docker docker-engine
  sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
  sudo apt-get update -y
  sudo apt-get install -y docker-ce
  sudo groupadd docker
  sudo usermod -aG docker "${USER}"
  sudo pip install --upgrade pip
  sudo pip install docker-compose
  sudo touch /.done-initial-setup
else
  echo "Initial Setup already complete, passing..."
fi

#!/bin/bash
sudo cp dimmer.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dimmer
sudo systemctl stop dimmer
sudo systemctl start dimmer

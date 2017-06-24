#!/bin/bash
sudo cp statusboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable statusboard
sudo systemctl stop statusboard
sudo systemctl start statusboard

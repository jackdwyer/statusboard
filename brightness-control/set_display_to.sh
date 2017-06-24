#!/bin/bash

if [[ -z ${1} ]]; then
  echo "Must pass first arg"
  exit 1
fi

echo ${1} > /sys/class/backlight/intel_backlight/brightness

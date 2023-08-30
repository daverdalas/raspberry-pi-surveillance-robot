#!/bin/bash

if [[ "$GPIOZERO_PIN_FACTORY" == "pigpio" && "$ENVIRONMENT" == "production" ]]; then
  echo "Starting pigpiod..."
  pigpiod -s 10
fi

exec "$@"

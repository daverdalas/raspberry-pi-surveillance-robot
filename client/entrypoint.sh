#!/bin/bash

pigpiod -g -s 10

tail -f /dev/null

exec "$@"

#!/bin/bash
pactl load-module module-null-sink sink_name=inputs
pactl load-module module-loopback sink=inputs
pactl load-module module-loopback sink=inputs

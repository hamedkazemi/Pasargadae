#!/bin/bash

# Install required packages if not present
if ! command -v wayland-scanner &> /dev/null; then
    echo "Installing wayland-scanner..."
    sudo apt-get install wayland-protocols libwayland-dev
fi

# Generate protocol headers
wayland-scanner client-header \
    /usr/share/wayland-protocols/unstable/wlr-screencopy-unstable-v1/wlr-screencopy-unstable-v1.xml \
    wlr-screencopy-unstable-v1-client-protocol.h

wayland-scanner private-code \
    /usr/share/wayland-protocols/unstable/wlr-screencopy-unstable-v1/wlr-screencopy-unstable-v1.xml \
    wlr-screencopy-unstable-v1-client-protocol.c

# Compile the program
gcc -o screen_capture screen_capture.c wlr-screencopy-unstable-v1-client-protocol.c \
    `sdl2-config --cflags --libs` -lwayland-client

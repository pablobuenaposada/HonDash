#!/bin/bash

export XAUTHORITY=/home/pi/.Xauthority
export DISPLAY=:0

# Desired window title when the page is fully loaded
EXPECTED_TITLE="hondash.local/"

# Loop until the window title contains the expected text
while : ; do
  # Get the active window's title
  WINDOW_TITLE=$(xdotool search --onlyvisible --class "chromium" getwindowname 2>/dev/null)

  # Check if the title matches the expected page title
  if [[ "$WINDOW_TITLE" == *"$EXPECTED_TITLE"* ]]; then
    echo "Page loaded successfully!"
    break
  else
    # If not, send an F5 to refresh the page and retry
    echo "Page not loaded yet. Current title: $WINDOW_TITLE. Retrying..."
    xdotool key F5
  fi

  sleep 5
done
#!/bin/sh
# Short, easy-to-type alias for bridge-send (handy on mobile): bg.s /clear
# Delegates to bridge-send (same plugin bin/, on PATH) so there's one implementation.
exec bridge-send "$@"

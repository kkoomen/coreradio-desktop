#!/usr/bin/env bash

# For more info about the 'set' command, see
# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
set -e
set -u

ROOT_DIR=$(cd "$(dirname "$0")/.."; pwd -P)

pyside2-rcc -g python "$ROOT_DIR/src/resources.qrc" > "$ROOT_DIR/src/resources_rc.py"

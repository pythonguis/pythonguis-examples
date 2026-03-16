#!/bin/bash

# Black the SOURCE files to limit subsequent reformatting.
black -l 128 $1

# PyQt6 (built from PyQt5) --------------------------------------------------
find $1 -type f -name "*.py" -print0 | xargs -0 sed -i 's/PyQt5/PyQt6/g'
find $1 -type f -name "*.py" -print0 | xargs -0 sed -i 's/exec_/exec/g'
find $1 -type f -name "*.py" -print0 | xargs -0 sed -i 's/qt-5/qt-6/g'

black -l 128 $1

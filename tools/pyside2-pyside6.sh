#!/bin/bash

# Black the SOURCE files to limit subsequent reformatting (highlights possible issues).
black -l 128 $1

# PySide6 (built from PySide2) --------------------------------------------------
find $1 -type f -name "*.py" -print0 | xargs -0 sed -i 's/PySide2/PySide6/g'
find $1 -type f -name "*.py" -print0 | xargs -0 sed -i 's/backend_qt5agg/backend_qtagg/g'
find $1 -type f -name "*.py" -print0 | xargs -0 sed -i 's/exec_/exec/g'
find $1 -type f -name "*.py" -print0 | xargs -0 sed -i 's/qt-5/qt-6/g'

black -l 128 $1

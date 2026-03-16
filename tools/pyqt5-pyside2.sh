#!/bin/bash

# Black the SOURCE files to limit subsequent reformatting (highlights possible issues).
black -l 128 $1

# PySide2 (built from PyQt5) --------------------------------------------------
find $1 -type f -name "*.py" -print0 | xargs -0 sed -i 's/PyQt5/PySide2/g'
find $1 -type f -name "*.py" -print0 | xargs -0 sed -i 's/pyqtSignal/Signal/g'
find $1 -type f -name "*.py" -print0 | xargs -0 sed -i 's/pyqtProperty/Property/g'
find $1 -type f -name "*.py" -print0 | xargs -0 sed -i 's/pyqtSlot/Slot/g'

black -l 128 $1

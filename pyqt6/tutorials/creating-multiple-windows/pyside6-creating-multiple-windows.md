---
Title: Creating additional windows
Subtitle: Opening new windows for your application
Date: 2021-08-30 10:07
Republish: 2021-11-26 09:00
RepublishNote: updated for PySide6
Author: Martin Fitzpatrick
Description: In this tutorial we'll step through how to create and open a new window, and how to show and hide external windows on demand.
SeoTitle: Create multiple windows in PySide6
NavTitle: Multi-window PySide6
SearchComments: multiple windows
Image: images/articles/multiple-windows.jpg
Tags: window,windows,qt,pyside,pyside6,foundation
---

In an earlier tutorial we've already covered how to open *dialog* windows. These are special windows which (by default) grab the focus of the user, and run their own event loop, effectively blocking the execution of the rest of your app.

However, quite often you will want to open a second window in an application, without interrupting the main window -- for example, to show the output of some long-running process, or display graphs or other visualizations. Alternatively, you may want to create an application that allows you to work on multiple documents at once, in their own windows.

It's relatively straightforward to open new windows but there are a few things to keep in mind to make sure they work well.  In this tutorial we'll step through how to create a new window, and how to show and hide external windows on demand.

[TOC]

## Creating a new window

In Qt any widget without a parent is a window. This means, to show a new window you just need to create a new instance of a widget. This can be any widget type (technically any subclass of `QWidget`) including another `QMainWindow` if you prefer.


NOTE: There is no restriction on the number of `` QMainWindow `` instances you can have. If you _need_ toolbars or menus on your second window you will have to use a `` QMainWindow `` to achieve this. This can get confusing for users however, so make sure it's necessary.


As with your main window, *creating* a window is not sufficient, you must also show it.

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        w = AnotherWindow()
        w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
```

![A main window with a button to launch a child window,]({static}window1.jpg)
*A main window with a button to launch a child window,*


If you run this, you'll see the main window. Clicking the button *may* show the second window, but if you see it it will only be visible for a fraction of a second. What's happening?

```python
    def show_new_window(self, checked):
        w = AnotherWindow()
        w.show()
```

Inside this method, we are creating our window (widget) object, storing it in the variable `w` and showing it. However, once we leave the method we no longer have a reference to the `w` variable (it is a *local* variable) and so it will be cleaned up – and the window destroyed. To fix this we need to keep a reference to the window *somewhere*, for example on the `self` object.

```python
    def show_new_window(self, checked):
        self.w = AnotherWindow()
        self.w.show()
```

Now, when you click the button to show the new window, it will persist.

However, what happens if you click the button again? The window will be re-created! This new window will replace the old in the `self.w` variable, and – because there is now no reference to it – the previous window will be destroyed.

You can see this in action if you change the window definition to show a random number in the label each time it is created.

```python
from random import randint


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)
```

The `__init__` block is only run when *creating* the window. If you keep clicking the button the number will change, showing that the window is being re-created.

One solution is to simply check whether the window has already being created before creating it. The example below shows this in action.

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from random import randint


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        if self.w is None:
            self.w = AnotherWindow()
        self.w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
```

![Child window with a label randomly generated on creation.]({static}window2.jpg)
*Child window with a label randomly generated on creation.*


Using the button you can pop up the window, and use the window controls to close it. If you click the button again, the same window will re-appear.

This approach is fine for windows that you create temporarily – for example if you want to pop up a window to show a particular plot, or log output. However, for many applications you have a number of standard windows that you want to be able to show/hide them on demand.

In the next part we'll look at how to work with these types of windows.

## Toggling a window

Often you'll want to toggle the display of a window using an action on a toolbar or in a menu. As we previously saw, if no reference to a window is kept, it will be discarded (and closed). We can use this behaviour to close a window, replacing the `show_new_window` method from the previous example with –

```python
    def show_new_window(self, checked):
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()

        else:
            self.w = None  # Discard reference, close window.
```

By setting `self.w` to `None` the reference to the window will be lost, and the window will close.


NOTE: If we set it to any other value that `` None `` the window will still close, but the `` if self.w is None `` test will not pass the next time we click the button and so we will not be able to recreate a window.


This will only work if you have not kept a reference to this window somewhere else. To make sure the window closes regardless, you may want to explicitly call `.close()` on it. The full example is shown below.

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from random import randint


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
```

## Persistent windows

So far we've looked at how to create new windows on demand. However, sometimes you have a number of standard application windows. In this case rather than create the windows when you want to show them, it can often make more sense to create them at start-up, then use `.show()` to display them when needed.

In the following example we create our external window in the `__init__` block for the main window, and then our `show_new_window` method simply calls `self.w.show()` to display it.


```python
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from random import randint


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = AnotherWindow()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        self.w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
```

If you run this, clicking on the button will show the window as before. However, note that the window is only created once and calling `.show()` on an already visible window has no effect.

### Showing & hiding persistent windows

Once you have created a persistent window you can show and hide it without recreating it. Once hidden the window still exists, but will not be visible and accept mouse/other input. However you can continue to call methods on the window and update it's state -- including changing it's appearance. Once re-shown any changes will be visible.

Below we update our main window to create a `toggle_window` method which checks, using `.isVisible()` to see if the window is currently visible. If it is not, it is shown using `.show()` , if it is already visible we hide it with `.hide()`.

```python
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = AnotherWindow()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.toggle_window)
        self.setCentralWidget(self.button)

    def toggle_window(self, checked):
        if self.w.isVisible():
            self.w.hide()

        else:
            self.w.show()

```

The complete working example of this persistent window and toggling the show/hide state is shown below.


```python
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from random import randint


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = AnotherWindow()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.toggle_window)
        self.setCentralWidget(self.button)

    def toggle_window(self, checked):
        if self.w.isVisible():
            self.w.hide()

        else:
            self.w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
```

Note that, again, the window is only created once -- the window's `__init__` block is not re-run (so the number in the label does not change) each time the window is re-shown.

## Multiple windows

You can use the same principle for creating multiple windows -- as long as you keep a reference to the window, things will work as expected. The simplest approach is to create a separate method to toggle the display of each of the windows.


```python
import sys
from random import randint

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window1 = AnotherWindow()
        self.window2 = AnotherWindow()

        l = QVBoxLayout()
        button1 = QPushButton("Push for Window 1")
        button1.clicked.connect(self.toggle_window1)
        l.addWidget(button1)

        button2 = QPushButton("Push for Window 2")
        button2.clicked.connect(self.toggle_window2)
        l.addWidget(button2)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def toggle_window1(self, checked):
        if self.window1.isVisible():
            self.window1.hide()

        else:
            self.window1.show()

    def toggle_window2(self, checked):
        if self.window2.isVisible():
            self.window2.hide()

        else:
            self.window2.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
```

![A mainwindow with two child windows.]({static}window7.jpg)
*A mainwindow with two child windows.*


However, you can also create a generic method which handles toggling for all windows -- see [transmitting extra data with Qt signals](/pyside-transmitting-extra-data-qt-signals/) for a detailed explanation of how this works. The example below shows that in action, using a `lambda` function to intercept the signal from each button and pass through the appropriate window. We can also discard the `checked` value since we aren't using it.


```python
import sys
from random import randint

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window1 = AnotherWindow()
        self.window2 = AnotherWindow()

        l = QVBoxLayout()
        button1 = QPushButton("Push for Window 1")
        button1.clicked.connect(
            lambda checked: self.toggle_window(self.window1)
        )
        l.addWidget(button1)

        button2 = QPushButton("Push for Window 2")
        button2.clicked.connect(
            lambda checked: self.toggle_window(self.window2)
        )
        l.addWidget(button2)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def toggle_window(self, window):
        if window.isVisible():
            window.hide()

        else:
            window.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
```

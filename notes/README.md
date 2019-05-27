# Brown Note — A desktop Post-it note application in PyQt

Take temporary notes on your desktop, with this floating-note app. Notes
are stored locally in a SQLite database.

![Brown note](screenshot-notes.jpg)

This app is very simple, but demonstrates creation of decoration-less windows in PyQt. Removing the window
decorations removes the means to drag windows around, so we must re-implement this behaviour ourselves.

> If you think this app is neat and want to learn more about
PyQt in general, take a look at my [free PyQt tutorials](https://www.learnpyqt.com)
which cover everything you need to know to start building your own applications with PyQt.
# Mozzarella Ashbadger — Upgrade your browsing with tabs

Mozarella Ashbadger is the latest revolution in web
browsing! Go back and forward! Print! Save files! Get help!
(you’ll need it). Any similarity to other browsers is entirely
coincidental.

![Browser tabbed](screenshot-browser-tabbed.jpg)

> If you want to learn more about build GUI applications with Python,
take a look at my [PyQt5 tutorials](https://www.pythonguis.com)
which covers everything you need to know to start building your own applications with PyQt5.

## Code notes

### Tabbing

Adding tab support complicates the internals of the browser a bit, since we
now need to keep track of the currently active browser view, both to update
UI elements (URL bar, HTTPs icon) to changing state in the currently active
window, and to ensure the UI events are dispatched to the correct web view.

This is achieved by using intermediate slots which filter events, and by
adding signal redirection (using lamba functions to keep it short).

## Other licenses

Icons used in the application are by [Yusuke Kamiyaman](http://p.yusukekamiyamane.com/).

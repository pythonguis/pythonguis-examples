# Translatarrrr — Instant translation from any language to Pirate

A translator from any language (supported by Google translate) to pirate.
This uses a remote API from http://api.funtranslations.com for English 
to Pirate translation, and a unofficial Python wrapper around Google translate
for other languages to English.
 
![Translatarrrr](screenshot-translate1.jpg)

The *to English* part uses a Python library built on the web interface,
rather than an official API client since it's a faff to set up + non-free.
This means this part of the application is not guaranteed to work.

![Translatarrrr](screenshot-translate2.jpg)
 
The *to Pirate* part uses a public API that is heavily throttled. You'll
usually get about 5 translations before the limit kicks in. You can 
pay for an API key to get more.

This is, therefore, very useless.

> If you think this app is neat and want to learn more about
PyQt in general, take a look at my [free PyQt tutorials](https://www.learnpyqt.com)
which cover everything you need to know to start building your own applications with PyQt.

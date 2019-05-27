# Doughnut — An exchange rate tracker for people nuts about dough, in PyQt.

This is a simple currency exchange rate tracker implemented in PyQt, using the [fixer.io](http://fixer.io) API
for data. The default setup shows currency data for the preceding 180 days.

![Doughnut](screenshot-currency1.jpg)

Data is loaded progressively, with increasing resolution. Currency rates for a given date are shown in the right
hand panel and updated to follow the position of the mouse.

![Doughnut](screenshot-currency2.jpg)

> If you think this app is neat and want to learn more about
PyQt in general, take a look at my [free PyQt tutorials](https://www.learnpyqt.com)
which cover everything you need to know to start building your own applications with PyQt.

## Code notes

### Data handling

The interface presents a tracking plot (using PyQtGraph) of rates over the past 180 days. Since we don't want to 
spam a free service, requests to the API are rate-limited to 1-per-second, giving a full-data-load time of 180s (3 min).

To avoid waiting each time, we use `requests_cache` which uses a local sqlite database to store the result of recent
requests. The requests for data use a progressive 'search' approach: where there is a gap in the data, the middle 
point is filled first, and it prefers to load the most recent timepoints first. This means the whole plot gradually
increases in resolution over time, rather than working backwards only.

### Conversions

By default the app retrieves EUR rates and shows conversions to this base currency. If you change base currency
it will retrieve all data again for that new currency. This is daft, since if we have rates vs. EUR we can calculate
any other currency->currency conversion via EUR (with a small loss of accuracy).



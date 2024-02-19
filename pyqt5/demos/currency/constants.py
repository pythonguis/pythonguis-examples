# Base currency is used to retrieve rates from fixer.io.
# If we change currency we re-request, though it would
# be possible to calculate any rates *through* the base.
DEFAULT_BASE_CURRENCY = "EUR"
DEFAULT_DISPLAY_CURRENCIES = [
    "CAD",
    "CYP",
    "AUD",
    "USD",
    "EUR",
    "GBP",
    "NZD",
    "SGD",
]
HISTORIC_DAYS_N = 180

# Colour sets.
BREWER12PAIRED = [
    "#a6cee3",
    "#1f78b4",
    "#b2df8a",
    "#33a02c",
    "#fb9a99",
    "#e31a1c",
    "#fdbf6f",
    "#ff7f00",
    "#cab2d6",
    "#6a3d9a",
    "#ffff99",
    "#b15928",
]

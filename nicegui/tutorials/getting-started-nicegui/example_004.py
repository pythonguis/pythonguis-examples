# Getting Started With NiceGUI for Web UI Development in Python
# https://www.pythonguis.com/tutorials/getting-started-nicegui/

from matplotlib import pyplot as plt

from nicegui import ui

# Data elements
time = [1, 2, 3, 4, 5, 6]
temperature = [30, 32, 34, 32, 33, 31]

columns = [
    {
        "name": "time",
        "label": "Time (min)",
        "field": "time",
        "sortable": True,
        "align": "right",
    },
    {
        "name": "temperature",
        "label": "Temperature (ºC)",
        "field": "temperature",
        "required": True,
        "align": "right",
    },
]
rows = [
    {"temperature": temperature, "time": time}
    for temperature, time in zip(temperature, time)
]
ui.table(columns=columns, rows=rows, row_key="name")

with ui.pyplot(figsize=(5, 4)):
    plt.plot(time, temperature, "-o", color="blue", label="Temperature")
    plt.title("Temperature vs Time")
    plt.xlabel("Time (min)")
    plt.ylabel("Temperature (ºC)")
    plt.ylim(25, 40)
    plt.legend()

ui.run(title="NiceGUI Data Elements")

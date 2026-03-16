# Getting Started With NiceGUI for Web UI Development in Python
# https://www.pythonguis.com/tutorials/getting-started-nicegui/

from nicegui import ui

# Text elements
ui.label("Label")

ui.link("PythonGUIs", "https://pythonguis.com")

ui.chat_message("Hello, World!", name="PythonGUIs Chatbot")

ui.markdown(
    """
    # Markdown Heading 1
    **bold text**
    *italic text*
    `code`
    """
)

ui.restructured_text(
    """
    ==========================
    reStructuredText Heading 1
    ==========================
    **bold text**
    *italic text*
    ``code``
    """
)

ui.html("<strong>bold text using HTML tags</strong>")

ui.run(title="NiceGUI Text Elements")

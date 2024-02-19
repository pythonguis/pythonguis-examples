def build_font(config):
    """
    Construct a complete font from the configuration options
    :param self:
    :param config:
    :return: QFont
    """
    font = config["font"]
    font.setPointSize(config["fontsize"])
    font.setBold(config["bold"])
    font.setItalic(config["italic"])
    font.setUnderline(config["underline"])
    return font

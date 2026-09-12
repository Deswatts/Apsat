# Apsat  Copyright (C) 2026  Deswatts<Deswatts_Cre@outlook.com>
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.


__version__ = "1.0.0"
__title__ = "Apsat"
__description__ = "This Package is core of the Apsat"
__license__ = "GNU GPLv3"
__author__ = "Deswatts<Deswatts_Cre@outlook.com>"
__copyright__ = "DeswattsTools  Copyright (C) 2026  Deswatts<Deswatts_Cre@outlook.com>"


def get_version() -> dict[str, str]:
    """
    此函数用于获取包版本
    :return: 包版本号
    """
    version_digital = ""
    for i in __version__.split("."):
        version_digital += i
    return {"source": __version__, "digital": version_digital}


def get_name() -> str:
    """
    此函数用于获取包名
    :return: 包名
    """
    return __title__

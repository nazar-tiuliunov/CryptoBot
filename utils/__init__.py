"""
Initialization file for the keyboards' module.

This file defines the __all__ variable, which specifies the list of symbols
exported by this module, and imports the get_main_menu_keyboard function from
the keyboards' module.
"""

__all__ = ['get_main_menu_keyboard']

from .keyboards import get_main_menu_keyboard

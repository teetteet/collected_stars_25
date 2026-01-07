"""
BulletML Pattern Generator
A comprehensive tool for creating and managing BulletML patterns
"""

__version__ = '1.0.0'
__author__ = 'BulletML Pattern Generator Team'

from .bulletml_core import BulletMLGenerator
from .gui import BulletMLGUI, create_gui

__all__ = ['BulletMLGenerator', 'BulletMLGUI', 'create_gui']

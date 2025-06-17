"""
Low-level utility functions.
"""
import os
import sys


def get_resource_path(relative_path: str) -> str:
    """Get the absolute path to a resource file."""
    if getattr(sys, 'frozen', False) and relative_path == "config.yaml":
        return os.path.join(os.path.dirname(sys.executable), relative_path)
    elif hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
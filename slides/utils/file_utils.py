"""
File operation utilities
"""

import os


def ensure_config_directory():
    """Ensure configuration directory exists"""
    config_dir = os.path.expanduser("~/.config/glider")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return config_dir


def read_file(file_path):
    """Read file content"""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def write_file(file_path, content):
    """Write content to file"""
    # Ensure directory exists
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # Write content to file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def file_exists(file_path):
    """Check if file exists"""
    return os.path.isfile(file_path)

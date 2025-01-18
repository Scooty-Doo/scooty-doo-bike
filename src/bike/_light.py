"""
Module for the Light class.
"""

class Light:
    """Class representing the light of the bike."""
    def __init__(self):
        self.color = 'red'

    def set(self, mode):
        """Set the light color based on the mode."""
        if mode == 'maintenance':
            self.red()
        else:
            self.green()

    def green(self):
        """Set the light to green."""
        self.color = 'green'

    def red(self):
        """Set the light to red."""
        self.color = 'red'

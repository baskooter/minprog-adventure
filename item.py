"""
# Bas Kooter
#
# item.py
#
# keeps track of information about the items
"""

class Item:
    def __init__(self, name, description):
        self._name = name
        self._description = description

    # return the complete description of an item
    def getItemDescription(self):
        return f"{self._name}: {self._description}"

"""
# Bas Kooter
#
# room.py
#
# keeps track of information about the rooms and allows adventure.py to acces this information using functions
"""

class Room:
    def __init__(self, descriptionShort, descriptionLong):
        self._descriptionShort = descriptionShort
        self._descriptionLong = descriptionLong
        self._isVisited = False
        self._connections = {}
        self._isForced = False
        self._items = {}

    # adds a new connection to the room
    def add_connection(self, direction, connectingRoom, condition):
        # check if a room has multiple rooms connected in a certain direction
        if direction in self._connections.keys():
            self._connections[direction].append(connectingRoom)
            self._connections[direction].append(condition)
        else:
            self._connections[direction] = [connectingRoom, condition]
        
        # check if there is a forced connection in the room 
        if direction == "FORCED": 
            self._isForced = True

    # check if the room has a connection in a certain direction
    def has_connection(self, direction):
        if direction in self._connections.keys():
            return True
        return False

    # return all items in the current room
    def get_items_in_room(self):
        return self._items
    
    # return the connecting room of certain direction
    def get_connection(self, direction, inventory):
        counter = 1
        
        # check if the condition of moving to a certain room is met by comparing the inventory to the condition
        while self._connections[direction][i] != False:
            if self._connections[direction][i] in inventory.keys():
                    return self._connections[direction][counter - 1]
            counter += 2

        return self._connections[direction][i - counter]

    # return the description 
    def description(self):
        if self._isVisited and not self._isForced:
            return self._descriptionShort
        return self._descriptionLong
        
    # returns the long description of a room
    def descriptionLong(self):
        return self._descriptionLong
    
    # keeps track of whether a room has been visited or not
    def set_visited(self):
        self._isVisited = True

    # remove the item out of a room after it was taken
    def takeItem(self, item):
        return self._items.pop(item)
        
    # drop an item in a room
    def dropItem(self, item, itemObj):
        self._items[item] = itemObj

    # check if a certain item is in the current room
    def isItemInRoom(self, item):
        if item in self._items.keys():
            return True
        return False
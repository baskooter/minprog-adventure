"""
# Bas Kooter
#
# adventure.py
#
# let user play a text adventure game
"""

import loader

class Adventure():

    # create rooms and items for the game that was specified at the command line
    def __init__(self, filename):
        self._current_room = loader.load_room_graph(filename)
        self._inventory = {}
        self._synonyms = loader.loadSynonyms()

    # pass along the description of the current room, be it short or long
    def room_description(self):
        room_desc = self._current_room.description()
        room_desc = room_desc + self.get_items_room()
        return room_desc

    # get all the descriptions of the items in the current room
    def get_items_room(self):
        room_desc = ""
        items_in_room = self._current_room.get_items_in_room()
        for keys in items_in_room.keys():
            room_desc += "\n" + items_in_room[keys].getItemDescription()
        return room_desc

    # get the long description of the room
    def get_description_long(self):
        return self._current_room.descriptionLong() + self.get_items_room()

    # get descriptions of all the items in inventory
    def get_inventory_description(self):
        inventory_desc = []
        # loop through all items in inventory
        for keys in self._inventory:
            # add the description of an item to the description of the inventory
            inventory_desc.append(self._inventory[keys].getItemDescription())
        return inventory_desc

    # move to a different room by changing "current" room, if possible
    def move(self, direction):
        if self._current_room.has_connection(direction):
            self._current_room.set_visited()
            # move to the next room
            self._current_room = self._current_room.get_connection(direction, self._inventory)
            return True
        return False
        pass

    # move player to the forced room
    def move_forced(self):
        self._current_room = self._current_room.get_connection("FORCED", self._inventory)

    # check if the room has a forced connection
    def check_forced(self):
        if (self._current_room.has_connection("FORCED")):
            return True
        else:
            return False

    # take or drop an item if it's in the room or inventory
    def moveItem(self, command, item):
        if command == "TAKE":
            # check if the item to be taken is present in the room
            if self._current_room.isItemInRoom(item):
                action = item + " taken"
                self._inventory[item] = self._current_room.takeItem(item)
                return action
            else:
                return "No such item"
        elif command == "DROP":
            # check if the item to be dropped is currently in the inventory
            if item in self._inventory.keys():
                action = item + " dropped"
                self._current_room.dropItem(item, self._inventory[item])
                del self._inventory[item]
                return action
            else:
                return "No such item"
        return False

    # returns the corresponding synonym of a command
    def getCommand(self, key):
        return self._synonyms[key].getCommand()

    # returns all synonyms that are loaded
    def getSynonyms(self):
        return self._synonyms

if __name__ == "__main__":
    from sys import argv

    # check command line arguments
    if len(argv) not in [1,2]:
        print("Usage: python3 adventure.py [name]")
        exit(1)

    # load the requested game or else Tiny
    print("Loading...")
    if len(argv) == 2:
        game_name = argv[1]
    elif len(argv) == 1:
        game_name = "Tiny"
    filename = f"data/{game_name}Adv.dat"
    # create game
    adventure = Adventure(filename)

    # welcome user
    print("Welcome to Adventure.\n")

    # print very first room description
    print(adventure.room_description())

    # prompt the user for commands until they type QUIT
    while True:

        # prompt, converting all input to upper case
        command = input("> ").upper()

        command = command.split(" ")
        synonyms = adventure.getSynonyms()
        
        # check if the first word of the command corresponds to a synonym
        for keys in synonyms.keys():
            if command[0] == keys:
                # change the first word of the command to the corresponding synonym
                command = [adventure.getCommand(keys)]

        # check for certain commands
        if (command[0] == "HELP"):
            print("You can move by typing directions such as EAST/WEST/IN/OUT\nQUIT quits the game.\nHELP prints instructions for the game.\nLOOK lists the complete description of the room and its contents.\nINVENTORY lists all items in your inventory.")
        elif (command[0] == "LOOK"):
            print(adventure.get_description_long())
        elif (command[0] == "INVENTORY"):
            inventory_desc = adventure.get_inventory_description()
            # check if inventory is empty
            if len(inventory_desc) == 0:
                print("Your inventory is empty")
            for i in range(len(inventory_desc)):
                print(inventory_desc[i])

        # perform a move
        elif len(command) == 1:
            move = adventure.move(command[0])
            if move == False:
                print("Invalid command.")
            
            # check if a move has been forced
            elif adventure.check_forced() == False:
                print(adventure.room_description())
            else:
                # if a move is forced, two descriptions need to be printed
                while adventure.check_forced():
                    print(adventure.room_description())
                    adventure.move_forced()
                    print(adventure.room_description())
                
        # pick an item up or drop it
        else:
            action = adventure.moveItem(command[0], command[1])
            if action == False:
                print("Invalid command")
            else:
                print(action)

        # allows player to exit the game loop
        if command[0] == "QUIT":
            break

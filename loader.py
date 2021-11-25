"""
# Bas Kooter
#
# loader.py
#
# loads the rooms, items, connections and synonyms for the adventure game
"""

from room import Room
from item import Item

# keep the synonyms of commands stored in a synonym class
class Synonym:
    def __init__(self, short, command):
        self._short = short
        self._command = command

    def getCommand(self):
        return self._command

rooms = {}

# load all room information
def load_room_graph(fileName):
    dataLoad = 0
    with open(fileName) as file:
        for line in file:
            roomData = line.strip().split("\t")
            # keep track of whether the section of room descriptions, room connections or room items is being read
            if line == "\n":
                dataLoad += 1
                assert 1 in rooms
                assert rooms[1]._descriptionShort == "Outside building"

            # load the rooms with description
            if dataLoad == 0:
                rooms[int(roomData[0])] = Room(roomData[1], roomData[2].strip())

            # link the rooms together
            elif line != "\n" and dataLoad == 1:
                # set the source room to the current room in the line
                source_room = int(roomData[0])
                for i in range(1, len(roomData), 2):
                    # set the destination room to the next number in line
                    destination_room = int(roomData[i + 1].split("/")[0])
                    condition = False
                    
                    # check if there is a confition to be met when entering the room, add this condition
                    if len(roomData[i + 1].split("/")) > 1:
                        condition = roomData[i + 1].split("/")[1]
                    direction = roomData[i]

                    rooms[source_room].add_connection(direction, rooms[destination_room], condition)

            # load items and place them in the correct room
            elif line != "\n" and dataLoad == 2:
                rooms[int(roomData[2])]._items[roomData[0]] = (Item(roomData[0], roomData[1]))


        assert rooms[1].has_connection("WEST")
        assert rooms[2].get_connection("EAST", {})._descriptionShort == "Outside building"
        return rooms[1]

# load the synonyms of commands
def loadSynonyms():
    synonymLib = {}
    dataLoad = 0
    # load all synonyms from the file into a library
    with open("data/Synonyms.dat") as file:
        for line in file:
            synonym = line.strip().split("=")
            synonymLib[synonym[0]] = Synonym(synonym[0], synonym[1])
        return synonymLib



import csv
import os


class ObjParse:
    def __init__(self):
        self.objects = []

        # Array structure = objects[EntryNum][0 = Name, 1 = xPos, 2 = yPos, 3 = Data[]]

    def ReadObj(self, filename):

        # Open the selected object file
        o = open('./stage/object' + filename + '.csv', 'rt', encoding='shiftjis', errors='ignore')
        readObjects = csv.reader(o)

        # Open the object types file
        t = open('./Resource/ObjectTypes.csv', 'rt', encoding='shiftjis', errors='ignore')
        readTypes = csv.reader(t)

        # Store all types into an array for convenience
        types = []
        for row in readTypes:
            types.append(row)

        t.close()

        # Define Variables
        name = ""
        linesToRead = 0

        # Used to prevent the first line of an object being read more than once
        firstLine = True

        # Workaround to prevent a broken test level from crashing the editor
        if filename != "00_00_02":
            # Loop through each row of the objects file
            for row in readObjects:

                # Read First line of an entry
                if row[0] != "" and firstLine is True:
                    # Create a temp array to store the current object into
                    currentObject = [0, 0, 0, 0]

                    # Create a temp array to hold the entry data
                    data = []

                    name = row[0]
                    xPos = int(row[1])
                    yPos = int(row[2])

                    # Add The object name and X/Y Positions to the object array
                    currentObject[0] = name
                    currentObject[1] = xPos
                    currentObject[2] = yPos

                    # Now that the first line has been read, prevent it from being read again
                    firstLine = False

                # Loop through the object types and find how long the entry should be
                if linesToRead == 0:
                    i = 0
                    while i < 183:
                        if name == types[i][0]:
                            linesToRead = int(types[i][1])
                        i += 1

                # Read the remaining lines of the object
                if row[0] == "" and linesToRead > 0 and firstLine is False:
                    data.append(row)
                    linesToRead -= 1
                    if linesToRead < 0:
                        linesToRead = 0

                # Put everything into the objects array
                if linesToRead == 0 and firstLine is False:
                    currentObject[3] = data
                    self.objects.append(currentObject)

                    # Reset stuff for next entry
                    firstLine = True
                    linesToRead = 0
                    del currentObject
                    del data

        o.close()


class ColParse:
    def __init__(self):
        self.collision = []

    def ReadCol(self, filename):

        # Open the selected file
        c = open('./stage/cmap' + filename + '.csv', 'rt', encoding='shiftjis', errors='ignore')
        readCollision = csv.reader(c)

        # Create variables
        count = 0
        col = [0, 0, 0, 0, 0, 0, 0, 0]

        # Loop through each line in the collision file
        for row in readCollision:

            # Each entry starts with a '#' if we hit a '#' we reset the count
            if row[0] == "#":
                count = 0
                col = [0, 0, 0, 0, 0, 0, 0, 0]

            # Store the first line of a collision entry
            if count == 1:
                x1 = float(row[0])
                y1 = float(row[1])

                col[0] = x1
                col[1] = y1

            # Store the second line of a collision entry
            if count == 2:
                x2 = float(row[0])
                y2 = float(row[1])

                col[2] = x2
                col[3] = y2

            # Store the third line of a collision entry
            if count == 3:
                unk1 = float(row[0])
                unk2 = float(row[1])

                col[4] = unk1
                col[5] = unk2

            # Store the fourth line of a collision entry
            if count == 4:
                unk3 = float(row[0])

                col[6] = unk3

            # Store the fifth line of a collision entry
            if count == 5:
                unk4 = float(row[0])

                col[7] = unk4

                # Append the current collision entry to the collision array
                self.collision.append(col)
                del col

            count += 1

        c.close()


class AreaParse:
    def __init__(self):
        self.areas = []

    def ReadAreas(self, filename):
        # Open the selected area file
        a = open('./stage/area' + filename + '.csv', 'rt', encoding='shiftjis', errors='ignore')
        readAreas = csv.reader(a)

        # Loop through each row of the area file
        for row in readAreas:
            # Create an array to hold the current area
            area = [0, 0, 0, 0, 0]

            # Store current area into the array
            area[0] = int(row[0])
            area[1] = float(row[1])
            area[2] = float(row[2])
            area[3] = float(row[3])
            area[4] = float(row[4])

            # Append current area to areas array
            self.areas.append(area)

            del area

        a.close()


class PathParse:
    def __init__(self):
        self.paths = []

    def ReadPath(self, filename):

        # Open selected path file
        p = open('./stage/path' + filename + '.csv', 'rt', encoding='shiftjis', errors='ignore')
        readPaths = csv.reader(p)

        # define variables
        pathId = 0
        pos = []

        count = 0

        # Loop through each row in the path file
        for row in readPaths:

            # Workaround for some paths having no data
            if row:

                # Check if current row is the start of a new path entry
                if row[0] == "start":

                    # If count is greater than 0, append the previous entry to the paths array and reset count
                    if count > 0:
                        path = [pathId, pos]
                        self.paths.append(path)
                        del path
                        del pos

                        count = 0
                        pos = []

                    # Store the path id
                    pathId = row[1]

                # If the count is greater than 0, read the row and store the x and y coords
                if count > 0:
                    x = float(row[0])
                    y = float(row[1])

                    coords = [x, y]

                    # Append coords to the pos array
                    pos.append(coords)

                    del coords

                count += 1

        # Workaround for the last entry in a file not being appended
        if count > 0:
            path = [pathId, pos]
            self.paths.append(path)
            del path
            del pos


class LoadLevelData:
    def __init__(self, filename):
        self.Data = [[], [], [], []]

        # Read Collision

        # Read a collision file if it exists
        if os.path.isfile('./stage/cmap' + filename + '.csv'):
            # Setup Collision Reader
            c = ColParse()
            c.ReadCol(filename)
            self.Data[0] = c.collision

            # Debug output
            print("Collision loaded")

        # Read Objects

        # Read a objects file if it exists
        if os.path.isfile('./stage/object' + filename + '.csv'):
            # Setup Object Reader
            o = ObjParse()
            o.ReadObj(filename)
            self.Data[1] = o.objects

            # Debug output
            print("Objects loaded")

        # Read Areas

        # Read a area file if it exists
        if os.path.isfile('./stage/area' + filename + '.csv'):
            # Setup Area Reader
            a = AreaParse()
            a.ReadAreas(filename)
            self.Data[2] = a.areas

            # Debug Output
            print("Areas loaded")

        # Read Paths

        # Read a path file if it exists
        if os.path.isfile('./stage/path' + filename + '.csv'):
            # Setup Path Reader
            p = PathParse()
            p.ReadPath(filename)
            self.Data[3] = p.paths

            # Debug Output
            print("Paths loaded")

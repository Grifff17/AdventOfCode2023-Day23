from gettext import find
from turtle import pos


allDirs = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1)
}

def solvepart1():
    #read in data
    data = fileRead("input.txt")
    global grid
    grid = [ list(row.strip()) for row in data ]
    grid[0][1] = "v"
    grid[len(grid)-2][len(grid[0])-2] = "v"

    #find path through maze
    global pathCache
    pathCache = {} # key = start of path, val = (end of path, list of coords in path)
    valid, maxRoute = findRoute((0,1), [])
    print(maxRoute-1)

    


#recursively find the longest path through the maze without visiting the same path twice
def findRoute(currPos, visitedSpaces):
    #traverse until a intersection is reached
    if currPos in pathCache.keys():
        newPos, newVisitedSpaces =  pathCache[currPos]
    else:
        newPos, newVisitedSpaces = navigatePath(currPos)
        pathCache[currPos] = (newPos, newVisitedSpaces)
    #check if current intersection is already visited
    if newPos in visitedSpaces:
        return False, 0
    #check if end of maze has been reached
    totalSpaces = visitedSpaces + newVisitedSpaces
    if newPos == (len(grid)-1, len(grid[0])-2):
        return True, len(totalSpaces)
    #recurse in each valid direction at the intersection
    greatestLen = 0
    anyFound = False
    for symbol,dir in allDirs.items():
        adjacent = posAdd( newPos, dir )
        if grid[adjacent[0]][adjacent[1]] == symbol:
            valid, amount = findRoute(adjacent, totalSpaces)
            if valid and amount > greatestLen:
                greatestLen = amount
                anyFound = True
    return anyFound, greatestLen

#navigate along a path until an intersection is reached
def navigatePath(startPos):
    prev = startPos
    curr = posAdd(prev, allDirs[ grid[prev[0]][prev[1]] ] )
    visitedSpaces = [prev]
    while (grid[curr[0]][curr[1]] not in allDirs.keys()):
        visitedSpaces.append(curr)
        for newDir in allDirs.values():
            newPos = posAdd(curr, newDir)
            if inGrid(newPos, grid) and newPos != prev and grid[newPos[0]][newPos[1]] != "#":
                prev = curr
                curr = newPos
                break
    visitedSpaces.append(curr)
    finalSpace = posAdd(curr, allDirs[ grid[curr[0]][curr[1]] ])
    visitedSpaces.append(finalSpace)
    return finalSpace, visitedSpaces
        
#adds two coordinates together
def posAdd(pos1, pos2):
    return tuple([ sum(coords) for coords in zip(pos1, pos2) ])

#checks if a coordinate is in a grid
def inGrid(pos, grid):
    return pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[0])

def fileRead(name):
    data = []
    f = open(name, "r")
    for line in f:
        data.append(line);
    return data

solvepart1()
from time import sleep
import os
import sys
h,v,bt,tb = "Horizontal", "Vertical", "BottomTop", "TopBottom"
H,V,BT,TB = h,v,bt,tb

grid = []
clear = lambda : os.system("cls")

class Connect:
  def __init__(self,spaces,direction):
    self.Spaces = spaces
    for i in range(len(self.Spaces)):
      space = self.Spaces[i]
      if space.Connect[direction] != None:
        for thing in space.Connect[direction].Spaces:
          self.Spaces.append(thing)
    self.Spaces = set(self.Spaces)
    self.Length = len(self.Spaces)
    self.Player = spaces[0].Display
    for space in self.Spaces:
      space.Connect[direction] = self
      
class Space:
  def __init__(self,y,x):
    self.Display = "|   "
    self.X = x
    self.Y = y
    self.Connect = {
      "Horizontal":None,
      "Vertical":None,
      "BottomTop":None,
      "TopBottom":None
    }
    self.Adjacent = {
      "Horizontal":[],
      "Vertical":[],
      "BottomTop":[],
      "TopBottom":[]
    }

  def __str__(self):
    return self.Display

  def updateAdjacentSpaces(self):
    for i in range(-1,2,2):
      if self.Y + i in range(0,len(grid)):
        self.Adjacent[V].append(grid[self.Y+i][self.X])
      if self.X + i in range(0,len(grid[self.Y])):
        self.Adjacent[H].append((grid[self.Y][self.X+i]))  
      if self.X + i in range(0,len(grid[self.Y])) and self.Y - i in range(0,len(grid)):
        self.Adjacent[BT].append((grid[self.Y-i][self.X+i]))
      if self.X + i in range(0,len(grid[self.Y])) and self.Y + i in range(0,len(grid)):
        self.Adjacent[TB].append((grid[self.Y+i][self.X+i]))

  def updateConnect(self,Display):
    for value in self.Adjacent:
      for thing in self.Adjacent[value]:
        if thing.Display == Display:
          Connect([self,thing],value)
    return self

def printGrid(user=None):
  clear()
  if user != None:
    print(f"Player {user}, choose a place to drop a counter:\n")
  for i in range(len(grid[0])):
    sys.stdout.write("  "+ str(i+1)+ " ")
  print("")
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      addon = ""
      if j == len(grid[i])-1:
        addon = "|"
      sys.stdout.write(str(grid[i][j])+addon)
    print("\n-----------------------------")

def addToGrid(counter, column):
  i=0
  if grid[i][column].Display != "|   ":
    return "Error"
  while True:
    if i+1 >= len(grid):
      grid[i][column].Display = counter
      return grid[i][column].Y,grid[i][column].X
    elif grid[i+1][column].Display != "|   ":
      grid[i][column].Display = counter
      return grid[i][column].Y,grid[i][column].X
    else:
      i += 1

length = 7
height = 6
for i in range(height):
  grid.append([])
  for j in range(length):
    grid[i].append(Space(i,j))
for i in range(len(grid)):
  for j in range(len(grid[i])):
    grid[i][j].updateAdjacentSpaces()

playing = True
players = {
  -1: "| X ",
  1: "| O "
}
step = -1
while playing:
  global currentPlayer
  currentPlayer = str(int((1/4)*((step+1)**2)+1)) #Quadratic where x=-1 y=1, x=1 y=2
  playerCounter = players[step]
  printGrid(currentPlayer)
  try:
    choice = int(input())
    if type(choice)!= int or choice < 1 or choice > len(grid[0]):
      continue
  except ValueError:
    continue
  c = addToGrid(playerCounter,choice-1)
  if c != "Error":
    newSpace = grid[c[0]][c[1]]
    newSpace.updateConnect(playerCounter)
    for i in newSpace.Connect:
      if newSpace.Connect[i] != None: #Combine into one if statement?
        if newSpace.Connect[i].Length >= 4:
          printGrid()
          print(f"Player {currentPlayer} wins!!!!")
          quit()
    step *= -1
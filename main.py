import time
import os
h,v,bt,tb = "Horizontal", "Vertical", "BottomTop", "TopBottom"
H,V,BT,TB = h,v,bt,tb
grid = [
  ["|  ","|  ","|  ","|  ","|  ","|  ","|  "],
  ["|  ","|  ","|  ","|  ","|  ","|  ","|  "],
  ["|  ","|  ","|  ","|  ","|  ","|  ","|  "],
  ["|  ","|  ","|  ","|  ","|  ","|  ","|  "],
  ["|  ","|  ","|  ","|  ","|  ","|  ","|  "],
  ["|  ","|  ","|  ","|  ","|  ","|  ","|  "],
]

clear = lambda : os.system("clear")

class Connect:
  def __init__(self,spaces,direction):
    self.Spaces = spaces
    for i in range(len(self.Spaces)):
      space = self.Spaces[i]
      if space.Connect[direction] != None:
        for thing in space.Connect[direction].Spaces:
          self.Spaces.append(thing)
    self.Spaces = set(self.Spaces)
    self.Length = len(spaces)
    for space in self.Spaces:
      space.Connect[direction] = self
      
class Space:
  def __init__(self,y,x):
    self.Player = None
    self.X = x
    self.Y = y
    self.Connect = {
      "Horizontal":None,
      "Vertical":None,
      "BottomTop":None,
      "TopBottom":None
    }

  def __str__(self):
    return str(self.Y) + "," + str(self.X)

  def returnAdjacentSpaces(self):
    self.Adjacent = {
      "Horizontal":[],
      "Vertical":[],
      "BottomTop":[],
      "TopBottom":[]
    }
    for i in range(-1,2,2):
      if self.Y + i in range(0,len(grid)):
        self.Adjacent[V].append(grid[self.Y+i][self.X])
      if self.X + i in range(0,len(grid[self.Y])):
        self.Adjacent[H].append((grid[self.Y][self.X+i]))  
      if self.X + i in range(0,len(grid[self.Y])) and self.Y - i in range(0,len(grid)):
        self.Adjacent[BT].append((grid[self.Y-i][self.X+i]))
      if self.X + i in range(0,len(grid[self.Y])) and self.Y + i in range(0,len(grid)):
        self.Adjacent[TB].append((grid[self.Y+i][self.X+i]))
    return self

  def updateConnect(self,player):
    for value in self.Adjacent:
      for thing in self.Adjacent[value]:
        if thing.Player == player:
          Connect([self,thing],value)
    return self

grid = [[Space(j,i) for i in range(len(grid[j]))] for j in range(len(grid))]
grid = [[grid[j][i].returnAdjacentSpaces() for i in range(len(grid[j]))] for j in range(len(grid))]

connectSpaces = grid[3][2].updateConnect(True).Connect[TB].Spaces
connectSpaces = grid[4][3].Connect[TB].Spaces
for i in connectSpaces:
  print(i)

BigBadWolf
==========
import math, random, pylab, numpy, matplotlib
import Vizu

class Position(object):
    """
    Represents location on the grid.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPos(self, speed):
        direction  = random.uniform(0, 360)
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(direction))
        delta_x = speed * math.sin(math.radians(direction))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)
    

class Grid(object):
    def __init__(self, width, length, predList, preyList):
        self.width = width
        self.length = length
        self.tiles = {}
        self.tiles2 = []
        self.predList = predList
        self.preyList = preyList
        for i in range(width):
           for j in range(length):
                "First represents predator, second prey"
                "If first is 1, third is the object predator"
                self.tiles[(i,j)] = [0,0, None]
        #Make list of positions of predators
        for p in self.predList:
            self.predAtPosition(p.position)
        #Make list op positions of preys
        for p in self.preyList:
            self.preyAtPosition(p.position)
        self.freeList = []
        #Make list of tiles which are not occupied
        for tile in self.tiles.keys():
            if self.tiles[tile][0] == [0,0]:
                self.freeList.append(tile)
                #Initialize numbers to plot
        self.sheepEaten = 0
        self.sheepBorn = 0
        self.wolfBorn = 0
        self.wolfStarved = 0

    def predAtPosition(self, pos):
        "Updates dictionary for tile if predator is on tile at position pos"
        x = int(math.floor(pos.getX()))
        y = int(math.floor(pos.getY()))
        self.tiles[(x,y)][0] = 1
    
    def preyAtPosition(self, pos):
        "Updates dictionary for tile if prey is on tile at position pos"
        x = int(math.floor(pos.getX()))
        y = int(math.floor(pos.getY()))
        self.tiles[(x,y)][1] = 1
    
    def updateTiles(self):
        "Updates dictionary for each tile"
        for p in self.predList:
            self.predAtPosition(p.position)
        for p in self.preyList:
            self.preyAtPosition(p.position)
    
    def eatTile(self, tile):
        "Returns True if predator and prey are both present at tile"
        if self.tiles[ tile ][0] == 1:
            return True
        else:
            return False
        
    def getRandomPosition(self):
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        return Position(x, y)

    def update(self):
        self.updateTiles()
        for animal in self.predList:
            animal.updateHealth()
            pos = animal.position
            discPos = discretePos(pos)
            self.tiles[ (discPos) ][0] = 0
            #Die if health is low
            if animal.starve():
                self.predList.remove(animal)
                if discPos not in self.freeList:
                    self.freeList.append(discPos)
                self.wolfStarved += 1
            #Else move
            else:
                positionx, positiony = discretePos(animal.updateRandomPosition())
                #If moved to occupied tile, move to free tile
                if (self.tiles[ (positionx, positiony) ][0] == 1 and self.freeList != []):
                        index = random.randint(0, len(self.freeList)-1)
                        positionx, positiony = self.freeList[index]
                        posit = Position(positionx+.5, positiony+.5)
                        animal.updateFreePosition(posit)
                        self.freeList.pop(index)
                #If there is no free tile move back to original position
                elif self.freeList == []:
                    animal.position = pos
                self.tiles[ discretePos(animal.position) ][0] = 1
                self.tiles[ discretePos(animal.position) ][2] = animal
                #update Lists and Dicts
                if discPos not in self.freeList:
                    self.freeList.append(discPos)
                self.tiles[ discretePos(Position(animal.position.x, animal.position.y)) ][0] = 1
                self.tiles[ discretePos(Position(animal.position.x, animal.position.y)) ][2] = animal
                #Give birth if health is high
                if (animal.birth() and self.freeList != []):
                    child = Predator(animal.speed, animal.health/2, animal.loss,
                                     animal.birthHealth, animal.width, animal.length)
                    index = random.randint(0, len(self.freeList)-1)
                    positionx, positiony = self.freeList[index]
                    posit = Position(positionx+.5, positiony+.5)
                    child.updateFreePosition(posit)
                    self.predList.append(child)
                    animal.health = animal.health/2
                    self.freeList.pop(index)
                    self.wolfBorn += 1
                    self.tiles[ discretePos(child.position) ][0] = 1
                    self.tiles[ discretePos(child.position) ][2] = child

                    
        for animal in self.preyList:
            animal.updateHealth()
            pos = animal.position
            discPos = discretePos(pos)
            self.tiles[ discretePos(animal.position) ][1] == 0
            #Move
            positionx, positiony = discretePos(animal.updateRandomPosition())
            #If moved to occupied tile, move to free tile
            if (self.tiles[ (positionx, positiony) ][1] == 1 and self.freeList != []):
                    index = random.randint(0, len(self.freeList)-1)
                    positionx, positiony = self.freeList[index]
                    posit = Position(positionx+.5, positiony+.5)
                    animal.updateFreePosition(posit)
                    self.freeList.pop(index)
            #If there is no free tile move back to original position
            elif self.freeList == []:
                animal.position = pos
            self.tiles[ discretePos(animal.position) ][1] == 1
            #update Lists and Dicts
            self.freeList.append(discPos)
            if discretePos(Position(animal.position.x, animal.position.y)) in self.freeList:
                self.freeList.remove(discretePos(Position(animal.position.x, animal.position.y)))
            self.tiles[ discretePos(Position(animal.position.x, animal.position.y)) ][1] = 1
            tile = discretePos(animal.position)
            if self.eatTile(tile):
                pred = self.tiles[tile][2]
                pred.health += animal.health  
                self.preyList.remove(animal)
                self.sheepEaten +=1
            #Give birth if health is high
            if (animal.birth() and self.freeList != []):
                child = Prey(animal.speed, animal.health/3, animal.loss,
                                 animal.birthHealth, animal.width, animal.length)
                index = random.randint(0, len(self.freeList)-1)
                positionx, positiony = self.freeList[index]
                posit = Position(positionx+.5, positiony+.5)
                child.updateFreePosition(posit)
                self.preyList.append(child)
                animal.health = animal.health/2
                self.freeList.pop(index)
                self.sheepBorn += 1
                self.tiles[ discretePos(child.position) ][1] == 1

##        for tile in self.tiles:
##            if self.eatTile(tile):
##                print self.tiles[tile]
##                print tile
        return self.sheepEaten, self.sheepBorn, self.wolfBorn, self.wolfStarved
    
def discretePos(pos):
    x = int(math.floor(pos.getX()))
    y = int(math.floor(pos.getY()))
    return (x,y)

def positionToIndice(self, pos):
    coordinatex, coordinatey = self.discretePos(pos)
    indice = 0
    return indice
            
class Animal(object):
    def __init__(self, speed, health, dHealth, birthHealth, width, length):
        self.speed = speed
        self.position = Position(random.uniform(0,width), random.uniform(0,length))
        self.health = health
        self.loss = loss
        self.width = width
        self.length = length
        self.birthHealth = birthHealth
        self.dHealth = dHealth
        
    def getAnimalPosition(self):
        return self.position

    def setAnimalPosition(self, position):
        self.position = position

    def updateRandomPosition(self):
        updated_position = self.getAnimalPosition().getNewPos(self.speed)
        if updated_position.x > self.width:
            updated_position.x = updated_position.x - self.width
        elif updated_position.x < 0:
            updated_position.x = updated_position.x + self.width
        if updated_position.y > self.length:
            updated_position.y = updated_position.y - self.length
        elif updated_position.y < 0:
            updated_position.y = updated_position.y + self.length
        self.position = updated_position
        return Position(updated_position.x, updated_position.y)

    def updateFreePosition(self, pos):
        self.position = pos

    def starve(self):
        if self.health < 0:
            return True
        else:
            return False

    def birth(self):
        if self.health > self.birthHealth:
            return True
        else:
            False
 

class Predator(Animal):
    def reproduce(self, r_health):
            newPredator = Predator(self.grid, self.speed, self.health,
                                   self.energy/2, self. width, self.length)
            self.health = self.health/2
            return newPredator

    def updateHealth(self):
        self.health = self.health - self.dHealth

        
class Prey(Animal):
    def reproduce(self, r_health):
            newPrey = Prey(self.grid, self.speed, self.health, self.energy/2)   
            self.health = self.health/2
            return newPrey

    def updateHealth(self):
        self.health = self.health + self.dHealth
        
        
def runSim(n_pred, n_prey, speed, width, length, n_steps,
           s_health, w_rep_health, s_rep_health, loss, gain):
    """
    s_health: starting health value
    w_rep_health: health value to reproduce wolf
    s_rep_health: health value to reproduce sheep
    """
    predList = []
    preyList = []
    NPred = []
    NPrey = []
    eatenSheepList = []
    bornWolfList = []
    bornSheepList = []
    starvedList = []
    for i in range(n_pred):
        predList.append(Predator(speed, 20*numpy.random.normal()+s_health, loss, w_rep_health, width, length))
    for i in range(n_prey):
        preyList.append(Prey(speed, numpy.random.normal()+50, gain, s_rep_health, width, length))

    grid = Grid(width, length, predList, preyList)

    #anim = Vizu.FoodVisualization(n_pred, n_prey, width, length)
    timeList = []

    for t in range(n_steps):
        timeList.append(t)
        sheepEaten, sheepBorn, wolfBorn, wolfStarved = grid.update()
        #print "T=", t, "Eaten:", sheepEaten, "SBorn:", sheepBorn, "WBorn:", wolfBorn, "WStarved:", wolfStarved
        NPred.append(len(grid.predList))
        NPrey.append(len(grid.preyList))
        eatenSheepList.append(sheepEaten)
        bornWolfList.append(wolfBorn)
        bornSheepList.append(sheepBorn)
        starvedList.append(wolfStarved)
        if t%100==0:
            print "T=", t
        if len(grid.predList) == 0 or len(grid.preyList) == 0:
            break
        #anim.update(grid.predList, grid.preyList)
    print True

    #anim.done()
    pylab.plot(timeList, NPred, label = 'Number of predators')
    pylab.plot(timeList, NPrey, label = 'Number of preys')
##    pylab.plot(timeList, eatenSheepList, label = 'Number of sheeps eaten')
##    pylab.plot(timeList, bornSheepList, label = 'Number of sheep born')
##    pylab.plot(timeList, bornWolfList, label = 'Number of wolf born')
##    pylab.plot(timeList, starvedList, label = 'Number of wolfs starved')

    title = 'Pd= ' + str(n_pred) + ' Py= ' + str(n_prey) + \
            'S= ' + str(width) + '*' + str(length) +' H= ' + \
            str(s_health) + ' Sr= ' + str(s_rep_health) + \
            ' Wr= ' + str(w_rep_health) + 'L= ' + str(loss) + \
            'G=' + str(gain) + ' St= ' + str(speed)
    pylab.title(title) 
    pylab.ylabel('Number of animals') 
    pylab.xlabel('Time steps')
    pylab.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                     fancybox=True, shadow=True, ncol=5)
    pylab.show()

        
    
n_pred = 1; n_prey = 100; speed = 0.5; width = 100; length = 100; n_steps = 5000;
s_health = 600; w_rep_health = 2000; s_rep_health = 200; loss = 10; gain = 0.5;
runSim(n_pred, n_prey, speed, width, length, n_steps, s_health, w_rep_health, s_rep_health, loss, gain)

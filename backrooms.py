# imports
import pygame
import random
import time
import math
import settings as s

# classes

class map():


    def __init__(self,tileMap):
        self.tileMap = tileMap
        self.blocks = map.getBlocks(tileMap)
        self.visibleBlocks = []

        self.scrollX = 0
        self.scrollY = 0

        self.xOffset = 0
        self.yOffset = 0

        self.veloX = 0
        self.veloY = 0
        
        self.friction = 0.1
        self.collisions = self.getPlayerCollision()


    def updateScrollFromInput(self,keys,dir):

        if keys[pygame.K_UP]:
            self.veloY += s.moveA * dt * 60

        if keys[pygame.K_LEFT]:
            self.veloX += s.moveA * dt * 60

        if keys[pygame.K_DOWN]:
            self.veloY -= s.moveA * dt * 60

        if keys[pygame.K_RIGHT]:
            self.veloX -= s.moveA * dt * 60


        if keys[pygame.K_w]:
            self.veloX -= s.moveK * math.cos(math.radians(dir)) * dt * 60
            self.veloY -= s.moveK * math.sin(math.radians(dir)) * dt * 60

        if keys[pygame.K_a]:
            self.veloX += s.moveK * math.cos(math.radians(dir+90)) * dt * 60
            self.veloY += s.moveK * math.sin(math.radians(dir+90)) * dt * 60

        if keys[pygame.K_s]:
            self.veloX += s.moveK * math.cos(math.radians(dir)) * dt * 60
            self.veloY += s.moveK * math.sin(math.radians(dir)) * dt * 60

        if keys[pygame.K_d]:
            self.veloX -= s.moveK * math.cos(math.radians(dir+90)) * dt * 60
            self.veloY -= s.moveK * math.sin(math.radians(dir+90)) * dt * 60


        if abs(self.veloX) > s.maxAccel:
            self.veloX = (self.veloX/abs(self.veloX)) * s.maxAccel
        if abs(self.veloY) > s.maxAccel:
            self.veloY = (self.veloY/abs(self.veloY)) * s.maxAccel

        if abs(self.veloX) < s.minVelo:
            self.veloX = 0
        if abs(self.veloY) < s.minVelo:
            self.veloY = 0

        self.veloX -= self.veloX * self.friction
        self.veloY -= self.veloY * self.friction

        self.scrollX += self.veloX
        self.scrollY += self.veloY

        self.xOffset = self.scrollX % s.blockSize
        self.yOffset = self.scrollY % s.blockSize

        if abs(self.xOffset) > s.blockSize:
            self.xOffset = 0
        
        if abs(self.yOffset) > s.blockSize:
            self.yOffset = 0


    # returns index of all blocks in tilemap
    def getBlocks(tileMap):
        blocks = []
            
        for r in range(len(tileMap)):
            for c in range(len(tileMap[r])):
                if tileMap[r][c] == 1:
                    blocks.append((c,r))
        return blocks
    

    # draws the outline of where all blocks can be
    def drawGridLines(self):
        columns = s.screenX//s.blockSize
        rows = s.screenY//s.blockSize

        lineColour = "black"

        for i in range(columns):
            inc = i*s.blockSize + self.xOffset
            lineStart = (inc,0)
            lineEnd = (inc,s.screenY)
            pygame.draw.line(screen,lineColour,lineStart,lineEnd,1)

        for i in range(rows):
            inc = i*s.blockSize + self.yOffset
            lineStart = (0,inc)
            lineEnd = (s.screenX,inc)
            pygame.draw.line(screen,lineColour,lineStart,lineEnd,1)


    def isBlockVisible(blockX,blockY):

        #if blockX > 200 and blockX < 600:
            #if blockY > 200 and blockY < 600:

        if blockX > -s.blockSize and blockX < s.screenX + s.blockSize:
            if blockY > -s.blockSize and blockY < s.screenY + s.blockSize:

                return True
            else:
                return False
        else:
            return False


    def getVisibleBlocks(self):

        visBlocks = []
        
        for block in self.blocks:
            blockPos = self.getBlockPos(block)

            blockX = blockPos[0]
            blockY = blockPos[1]

            if map.isBlockVisible(blockX,blockY):
                visBlocks.append(block)
        
        return visBlocks

    
    # gets the pygame position of a block from its index
    def getBlockPos(self,blockIndex):
        blockX = blockIndex[0]*s.blockSize + self.scrollX
        blockY = blockIndex[1]*s.blockSize + self.scrollY
        return (blockX,blockY)


    # draws the map
    def draw2DMap(self):
        #map.drawGridLines(self)

        for block in self.visibleBlocks:
            pos = self.getBlockPos(block)
            pygame.draw.rect(screen,s.blockColor,((pos),(s.blockSize,s.blockSize)))


    def draw3DMap(self,rays):
        
        distances = []
        wallX = 0
        i = 0
        
        for ray in rays:
            i += 1
            wallX = (s.screenX/len(rays)) * i
            # +1 for no 0 division error
            distance = euclidianDistance((s.playerX,s.playerY),(ray)) + 1
            relHeight = s.wallHeight / distance

            # rgb value
            rgb = 255 * (s.brightness/distance)
            rgb = clamp(0,150,rgb)

            wallColour = (rgb,rgb,rgb)

            startY = math.ceil((s.screenY/2 + relHeight/2)+1/2)
            endY = math.ceil((s.screenY/2 - relHeight/2)+1/2)

            pygame.draw.line(screen,wallColour,(wallX,startY),(wallX,endY),s.lineThickness3D)

            
    # gets the tileMap index of a pygame coordinate point
    def getPointBlockIndex(self,point):
        pointX = (point[0] - self.scrollX) // s.blockSize
        pointY = (point[1] - self.scrollY) // s.blockSize
        return (pointX,pointY)

        
    # checks if a point is colliding with a block on the map
    def isPointCollision(self,point):
        
        pointBlockIndex = self.getPointBlockIndex(point)

        if r2D:
            if pointBlockIndex in self.visibleBlocks:
                return True
            else:
                return False
            
        elif r3D:
            if pointBlockIndex in self.blocks:
                return True
            else:
                return False
        

    def getPlayerCollision(self):
        collisions = []
        sides = ["L","R","T","B"]

        for point in s.playerSides:
            if self.isPointCollision(point):
                collisions.append(sides[s.playerSides.index(point)])
        
        return collisions
    

    def handlePlayerCollision(self):

        while len(self.collisions) > 0:
            for collision in self.collisions:
                
                if collision == "L":
                    self.scrollX -= 1

                if collision == "R":
                    self.scrollX += 1

                if collision == "T":
                    self.scrollY -= 1

                if collision == "B":
                    self.scrollY += 1

            self.collisions = self.getPlayerCollision()


class player():

    def __init__(self,pos,dir):
        self.pos = pos
        self.dir = dir

        self.playerX = pos[0]
        self.playerY = pos[1]
        self.rays = []


    def drawPlayer(self):
        dirX = self.playerX + s.maxRayDepth * math.cos(math.radians(self.dir))
        dirY = self.playerY + s.maxRayDepth * math.sin(math.radians(self.dir))

        pygame.draw.rect(screen,s.playerColour,((s.playerX,s.playerX),(s.playerSize,s.playerSize)))
        pygame.draw.line(screen,s.playerColour,(s.rayStartX,s.rayStartY),(dirX,dirY),s.dirPointerWidth)


    def setDirToMouse(self,mousePos):

        if r2D:
            # x and y distance between the player and mouse
            delta_x = mousePos[0] - self.pos[0]
            delta_y = mousePos[1] - self.pos[1]

            # stops division by 0
            if delta_x == 0:
                delta_x = 1

            # trigonometry to get direction
            dir = math.degrees(math.atan((delta_y) / (delta_x)))
            # fix for inversion on left side of the screen
            if mousePos[0] < self.pos[0]: dir = dir + 180
            self.dir = dir
        
        elif r3D:
            
            mouseX = mousePos[0]
            mouseY = mousePos[1]

            self.dir = (360/(s.r3DRightX-s.r3DLeftX)) * mouseX

            if mouseX < s.r3DLeftX: pygame.mouse.set_pos(s.r3DRightX,mouseY)
            elif mouseX > s.r3DRightX: pygame.mouse.set_pos(s.r3DLeftX,mouseY)
        
        else:
            self.dir = 0


    def rayCast(self,map):
        
        # the furthest left and right dir the player can see
        leftFOV = self.dir - (s.fov / 2)
        rightFOV = self.dir + (s.fov / 2)

        # list of all coordinates rays collided
        cast = []
        rays = math.floor((s.fov*s.rayDensity)+0.5)
        startPos = (s.rayStartX,s.rayStartY)

        # how many rays to cast
        for i in range(rays):

            rayDir = leftFOV + (i/s.rayDensity)

            dx = s.rayStep*math.cos(math.radians(rayDir))
            dy = s.rayStep*math.sin(math.radians(rayDir))

            rayCasting = True
            rayDepth = 0

            rayX = s.rayStartX
            rayY = s.rayStartY

            while rayCasting:

                if map.isPointCollision((rayX,rayY)) or rayDepth > s.maxRayDepth:
                    rayCasting = False
                    cast.append((rayX,rayY))
                    break

                

                rayX += dx
                rayY += dy

                # how far the ray has travelled from the player
                rayDepth = math.sqrt((self.playerX-rayX)**2+(self.playerY-rayY)**2)

        return cast
    

    def draw2DRays(self):
        for point in self.rays:
            pygame.draw.line(screen,s.rayColour,(s.rayStartX,s.rayStartY),(point[0],point[1]),s.rayThickness)


# functions

# returns a positive displacement
def euclidianDistance(p1,p2):
    deltaX = abs(p2[0]-p1[0])
    deltaY = abs(p2[1]-p1[1])
    dist = math.sqrt(deltaX**2+deltaY**2)
    return dist


def clamp(min,max,n):
    if n < min: n = min
    elif n > max: n = max
    return n

# variables


# pygame setup

pygame.init()

bg = pygame.image.load("bg.png")
screen = pygame.display.set_mode(s.screenSize)
clock = pygame.time.Clock()
running = True
dt = 0

r2D = False
r3D = True


tileMap = s.tileMap
map1 = map(tileMap)

adam = player(s.playerPos,s.playerDir)



# main loop
while running:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # switches between 2d and 3d
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if r2D:
                    r2D = False
                    r3D = True
                elif r3D:
                    r3D = False
                    r2D = True
                else:
                    r2D = True
                    r3D = False

    # loop setup

    map1.visibleBlocks = map1.getVisibleBlocks()

    # game stuff here

    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    map1.updateScrollFromInput(keys,adam.dir)
    map1.collisions = map1.getPlayerCollision()
    map1.handlePlayerCollision()

    adam.rays = adam.rayCast(map1)
    adam.setDirToMouse(mousePos)

    if r2D:
        screen.fill(s.bgColor)
        map1.draw2DMap()
        adam.draw2DRays()
        adam.drawPlayer()
    elif r3D:
        screen.blit(bg,(0,0))
        map1.draw3DMap(adam.rays)


    # screen update
    pygame.display.flip()
    dt = clock.tick(s.fps) / s.dtm

# game end
pygame.quit()
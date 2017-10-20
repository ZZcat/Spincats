import pygame
from pygame import *
import string, sys, os, random
from settings import *
WIN_WIDTH = width
WIN_HEIGHT = height
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self, up, down, left, right, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print "collide right"
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print "collide left"
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom


class Platform(Entity):
    def __init__(self, x, y, imagePath):
        Entity.__init__(self)

        self.image = get_image(imagePath)
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))

_image_library = {}
def get_image(path):
  global _image_library
  image = _image_library.get(path)
  if image == None:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    image = pygame.image.load(canonicalized_path)
    _image_library[path] = image
  return image


def load_map(path):
  # Map
  try:
      f = open(path, 'r+')
      map = f.read()
      f.close()
  except:
      print "can't read map.csv"
      sys.exit()
  return map

# The sprite for our Cat avatar

class Avatar(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = get_image("avatar.png")
        self.rect = Rect(x, y, 32, 32)

    def update(self, up, down, left, right, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)
    def move(self, x, y):
     self.rect.x += x
     self.rect.y += y
     def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print "collide right"
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print "collide left"
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom


def TestBlock(Char, blockedGroupList):
  for blockedGroup in blockedGroupList:
    if pygame.sprite.spritecollide(Char, blockedGroup, False):
      return True
# Fake sprite, doesn't have an image.
# We are just using this sprite for collision detection
# In the future, we might want to put blocking tiles on a layer above the background
class Blocked(pygame.sprite.Sprite):
  def __init__(self, x, y, width, height):
    pygame.sprite.Sprite.__init__(self)
    self.rect = pygame.Rect(x, y, width, height)


def main():

  
  pygame.init()
  map = load_map(MapName)

  map_split = map.split("\n")
  WIN_WIDTH = width
  WIN_HEIGHT = height
  HALF_WIDTH = int(WIN_WIDTH / 2)
  HALF_HEIGHT = int(WIN_HEIGHT / 2)

  DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
  DEPTH = 32
  FLAGS = 0
  CAMERA_SLACK = 30
  screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)


  pygame.mixer.music.load("music.mp3")
  pygame.mixer.music.set_volume(musicVolume)
  pygame.mixer.music.play(-1, 0.0)

  # Tile Information
  info = {"w": {"image": "wall.png",#w: wall
                   "block": True},
          "g": {"image": "gray.png",#w: gray block
                   "block": False},
          "p": {"image": "point.png",#w: black point
                   "block": True},
          "f": {"image": "floor.png",#f: floor
                   "block": False}}

  # Group of Fake Sprites, we'll use this group to detect collisions with the Avatar
  blockedGroup = pygame.sprite.RenderPlain()
  blockedPoints = pygame.sprite.RenderPlain()
  entities = pygame.sprite.Group()
  blockedPlayer = pygame.sprite.RenderPlain()
  

  # Draw Background
  background = pygame.Surface(screen.get_size())
  background = background.convert()

  rows = string.split(map, "\n")
  
  for x, row in enumerate(rows):
    
    tiles = string.split(row, ",")
    
    for y, tile in enumerate(tiles):
      
      tileInfo = info[tile]
      imagePath = tileInfo["image"]
   #   background.blit(get_image(imagePath), (x * 32, y * 32))
      p = Platform(x*32, y*32, imagePath)
      entities.add(p)
      isBlocked = tileInfo["block"]
      if (isBlocked):
        blockedGroup.add(Blocked(x * 32, y * 32, 32, 32))

      

  # Starting Coordinates, based on tiles.
  # TODO: Load player data from a file when we add more attributes
  x, y = playerX, playerY
  avatar = Avatar(x, y)

  blockedPlayer.add(avatar)

  allSprites = pygame.sprite.RenderPlain((avatar))

  move_right = False
  move_left = False
  move_up = False
  move_down = False
  
  # Event Loop
  done = False
  clock = pygame.time.Clock()

  #Charractor moving settings
  total_level_width  = len(map.split("\n"))*32
  total_level_height = len((map.split("\n"))[0])*32-32
  camera = Camera(complex_camera, total_level_width, total_level_height)
  entities.add(avatar)
  print entities
  while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print "Quiting..."
            done = True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                move_right = True
            elif event.key == pygame.K_a:
                move_left = True
            elif event.key == pygame.K_w:
                move_up = True
            elif event.key == pygame.K_s:
                move_down = True
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                move_right = False
            elif event.key == pygame.K_a:
                move_left = False
            elif event.key == pygame.K_w:
                move_up = False
            elif event.key == pygame.K_s:
                move_down = False
    
    camera.update(avatar)

    delta = [0, 0]
    
    if move_up == True:
        delta[1] = -playerDelta
    if move_down == True:
        delta[1] = playerDelta
    if move_left == True:
        delta[0] = -playerDelta
    if move_right == True:
        delta[0] = playerDelta

    avatar.move(delta[0], delta[1]) # Move the player
    
    if TestBlock(avatar, [blockedGroup]): # Check player for colitions
      avatar.move(0, -delta[1])
      if TestBlock(avatar, [blockedGroup]):
          avatar.move(-delta[0], delta[1])
          if TestBlock(avatar, [blockedGroup]):
              avatar.move(0, -delta[1])

    
    # Update the screen
    count = 0
    for e in entities:
      screen.blit(e.image, camera.apply(e))
    screen.blit(avatar.image, camera.apply(avatar))
    pygame.display.update()
    clock.tick(clockTick)
  pygame.quit()



if __name__ == "__main__":
  main()

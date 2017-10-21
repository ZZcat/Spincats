import pygame
from pygame import *
import string, sys, os, random
from settings import *
HALF_WIDTH = int(width / 2)
HALF_HEIGHT = int(height / 2)
class Camera(object):
    def __init__(self, width, height):
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        camera = self.state
        target_rect = target.rect
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width-width), l)   # stop scrolling at the right edge
        t = max(-(camera.height-height), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        self.state = Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


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
      print "Can't read map.csv"
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

    def move(self, x, y):
     self.rect.x += x
     self.rect.y += y



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

  total_level_width  = len(map.split("\n"))*32
  total_level_height = len((map.split("\n"))[0])*16+16
  print total_level_height/32
  screen = pygame.display.set_mode((width, height), 0, 32)

  pygame.mixer.music.load(musicFile)
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

  # Group of Sprites.
  blockedGroup = pygame.sprite.RenderPlain() #we'll use this group to detect collisions with the Avatar
  entities = pygame.sprite.Group()
  

  # Draw Background
  background = pygame.Surface(screen.get_size())
  background = background.convert()

  rows = string.split(map, "\n")
  
  for x, row in enumerate(rows):
    
    tiles = string.split(row, ",")
    
    for y, tile in enumerate(tiles):
      tileInfo = info[tile]
      imagePath = tileInfo["image"]
      p = Platform(x*32, y*32, imagePath)
      entities.add(p)
      isBlocked = tileInfo["block"]
      if (isBlocked):
        blockedGroup.add(Blocked(x * 32, y * 32, 32, 32))
      

  # Set avatar starting location to (x,y)
  x,y = playerX, playerY
  avatar = Avatar(x, y)

  move_right = False
  move_left = False
  move_up = False
  move_down = False
  
  # Event Loop
  done = False
  clock = pygame.time.Clock()

  #Charractor moving settings
  camera = Camera(total_level_width, total_level_height)
  entities.add(avatar)
  
  while not done:
    for event in pygame.event.get(): # Get keypresses
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
    
    camera.update(avatar) # Update camera position.

    delta = [0, 0]
    
    if move_up == True: # Calculate distance to move charractor
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
    for e in entities: # Add entities to screen
      screen.blit(e.image, camera.apply(e))
    screen.blit(avatar.image, camera.apply(avatar))
    pygame.display.update()
    clock.tick(clockTick)
  pygame.quit()



if __name__ == "__main__":
  main()

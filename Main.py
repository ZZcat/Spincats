import pygame
import string, sys, os

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
class Avatar(pygame.sprite.Sprite): # Inherit Sprite functions
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self) # Set up Sprite object internals

    self.image = get_image("avatar.png")
    self.rect = self.image.get_rect()
    self.rect.topleft = x, y

  def move(self, x, y):
    self.rect.x += x
    self.rect.y += y


# Fake sprite, doesn't have an image.
# We are just using this sprite for collision detection
# In the future, we might want to put blocking tiles on a layer above the background
class Blocked(pygame.sprite.Sprite):
  def __init__(self, x, y, width, height):
    pygame.sprite.Sprite.__init__(self)
    self.rect = pygame.Rect(x, y, width, height)


def main():
  pygame.init()
  
  size = width, height = 480,416
  screen = pygame.display.set_mode(size)

  map = load_map('map.csv')

  # Tile Information
  info = {"w": {"image": "wall.png",#w: wall
                   "block": True},
          "f": {"image": "floor.png",#f: floor
                    "block": False}}

  # Group of Fake Sprites, we'll use this group to detect collisions with the Avatar
  blockedGroup = pygame.sprite.RenderPlain()

  # Draw Background
  background = pygame.Surface(screen.get_size())
  background = background.convert()

  rows = string.split(map, "\n")
  
  for x, row in enumerate(rows):
    
    tiles = string.split(row, ",")
    
    for y, tile in enumerate(tiles):
      
      tileInfo = info[tile]
      imagePath = tileInfo["image"]
      background.blit(get_image(imagePath), (x * 32, y * 32))

      isBlocked = tileInfo["block"]
      if (isBlocked):
        blockedGroup.add(Blocked(x * 32, y * 32, 32, 32))

      

  # Starting Coordinates, based on tiles.
  # TODO: Load player data from a file when we add more attributes
  x, y = 32,32
  avatar = Avatar(x, y)

  allSprites = pygame.sprite.RenderPlain((avatar))

  move_right = False
  move_left = False
  move_up = False
  move_down = False
  
  # Event Loop
  done = False
  clock = pygame.time.Clock()
  
  while  not done:
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

    delta = [0, 0]

    if move_up == True:
        delta[1] = -3
    if move_down == True:
        delta[1] = 3
    if move_left == True:
        delta[0] = -3
    if move_right == True:
        delta[0] = 3

    avatar.move(delta[0], delta[1])
    if pygame.sprite.spritecollide(avatar, blockedGroup, False):
      avatar.move(-delta[0], -delta[1])

    #allSprites.update()
    # Update the screen
    screen.blit(background, (0, 0))
    allSprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    
  pygame.quit()



if __name__ == "__main__":
  main()

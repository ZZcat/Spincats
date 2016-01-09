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
     # map = map[:-1] #remove extra /n
      f.close()
  except:
      print "can't read map.csv"
      sys.exit()
  return map



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

  # Draw Map
  rows = string.split(map, "\n")
  
  for x, row in enumerate(rows):
    
    tiles = string.split(row, ",")
    
    for y, tile in enumerate(tiles):
      
      tileInfo = info[tile]
      imagePath = tileInfo["image"]
      screen.blit(get_image(imagePath), (x * 32, y * 32))

  # Starting Coordinates, based on tiles.
  # TODO: Load player data from a file when we add more attributes
  x, y = 32,32
  avatar = get_image("avatar.png")
  print "Setting up keys"
  key_d = False
  key_a = False
  key_w = False
  key_s = False
  print "Set all keys presses to False\n"
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
                key_d = True
            elif event.key == pygame.K_a:
                key_a = True
            elif event.key == pygame.K_w:
                key_w = True
            elif event.key == pygame.K_s:
                key_s = True
                
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                key_d = False
            elif event.key == pygame.K_a:
                key_a = False
            elif event.key == pygame.K_w:
                key_w = False
            elif event.key == pygame.K_s:
                key_s = False
    if key_w == True:
        y = y - 1
    if key_s == True:
        y = y + 1
    if key_a == True:
        x = x - 1
    if key_d == True:
        x = x + 1
    screen.blit(get_image(imagePath), (x * 32, y * 32))
    screen.blit(avatar, (x, y))
      
    pygame.display.flip()
    clock.tick(60)


if __name__ == "__main__":
  main()

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
      map = map #remove extra /n
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


  # Event Loop
  done = False
  while  not done:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: done = True
      
    pygame.display.flip()


if __name__ == "__main__":
  main()

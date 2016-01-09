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
  
  size = width, height = 250,250
  screen = pygame.display.set_mode(size)

  map = load_map('map.csv')

  # Tile Information
  info = {"wall": {"image": "wall.png",
                   "block": True},
          "floor": {"image": "floor.png",
                    "block": False}}

  # Draw Map
  rows = string.split(map, "\n")
  
  for x, row in enumerate(rows):
    
    tiles = string.split(row, ",")
    
    for y, tile in enumerate(tiles):
      
      tileInfo = info[tile]
      imagePath = tileInfo["image"]
      screen.blit(get_image(imagePath), (x * 50, y * 50))


  # Starting Coordinates, based on tiles.
  # TODO: Load player data from a file when we add more attributes
  x, y = 1, 1
  avatar = get_image("avatar.png")

  # Event Loop
  done = False
  clock = pygame.time.Clock()
  while  not done:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True
      elif event.type == pygame.KEYDOWN:
        delta = [0, 0]
        if event.key == pygame.K_UP:
          delta[1] = -1
        elif event.key == pygame.K_DOWN:
          delta[1] = 1
        elif event.key == pygame.K_RIGHT:
          delta[0] = 1
        elif event.key == pygame.K_LEFT:
          delta[0] = -1

        if (delta[0] or delta[1]):
          x += delta[0]
          y += delta[1]
          screen.blit(avatar, (x * 50, y * 50))
          print("Coords: ",x,y)
      
    pygame.display.flip()
    clock.tick(60)


if __name__ == "__main__":
  main()

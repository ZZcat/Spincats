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

    if move_up == True:
        y = y - 3
    if move_down == True:
        y = y + 3
    if move_left == True:
        x = x - 3
    if move_right == True:
        x = x + 3

    screen.blit(avatar, (x, y))
    pygame.display.flip()
    clock.tick(60)
    
  pygame.quit()



if __name__ == "__main__":
  main()

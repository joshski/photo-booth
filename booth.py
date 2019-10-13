import pygame, sys
from pygame.locals import *
from math import floor

# screenWidth = 1920
# screenHeight = 1080

screenWidth = 800
screenHeight = 450

clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight), HWSURFACE | DOUBLEBUF | RESIZABLE)

pygame.display.set_caption('Photo Booth')

cam = None

if sys.platform != 'darwin':
  cam = pygame.camera.Camera('/dev/video0', (screenWidth, screenHeight))
  cam.start()

gameState = 'idle'

cameraImage = None

def captureCamera(name):
  if sys.platform == 'darwin':
    import subprocess
    subprocess.call(['imagesnap', name])
  else:
    cameraImage = cam.get_image()
    pygame.image.save(cameraImage, name)

def showImage(name):
  picture = pygame.image.load(name)
  picture = pygame.transform.scale(picture, (screenWidth, screenHeight))
  rect = picture.get_rect()
  screen.blit(picture, rect)

def showSnapshotsUpTo(photoNumber):
  showImage('images/4up-background.png')
  for n in range(1, photoNumber + 1):
    tile = pygame.image.load('tmp/snapshot-' + str(n) + '.jpg')
    tile = pygame.transform.scale(tile, (floor(screenWidth / 2), floor(screenHeight / 2)))
    x = 0
    y = 0
    if n == 2 or n == 4:
      x = floor(screenWidth / 2)
    if n == 3 or n == 4:
      y = floor(screenHeight / 2)
    
    screen.blit(tile, (x, y))
    pygame.display.update()

def takePictures(step):
  print("take-pictures " + str(step))

  photoNumber = 1

  if step > 10:
    photoNumber = floor(step / 10) + 1
    step = step % 10

  if step == 1:
    showImage('images/photo-' + str(photoNumber) + '.png')
  
  if step == 3:
    showImage('images/countdown-3.png')

  if step == 4:
    showImage('images/countdown-2.png')

  if step == 5:
    showImage('images/countdown-1.png')

  if step == 6:
    showImage('images/cheese.png')
    pygame.display.flip()
    captureCamera('tmp/snapshot-' + str(photoNumber) + '.jpg')
  
  if step == 7:
    showImage('tmp/snapshot-' + str(photoNumber) + '.jpg')
  
  if step == 8:
    showSnapshotsUpTo(photoNumber)
    if photoNumber == 4:
      return 'idle'
  
  return 'taking-pictures'

def idle():
  gameState = 'idle'
  showImage('images/press-the-button.png')

idle()
step = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameState == 'idle':
                step = 0
                gameState = 'taking-pictures'
    
    if gameState == 'taking-pictures':
      step += 1
      gameState = takePictures(step)
      pygame.display.flip()
      clock.tick(1)
    else:
      pygame.display.flip()
      clock.tick(10)

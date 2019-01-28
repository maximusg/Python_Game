""" GUI is used for all visual operations for the game.
Displays the screen, maps skins/graphics to locations on screen"""

import sys
import pygame 

pygame.init()
pygame.mixer.init() #alllows for sounds

WINDOW_HEIGHT = 1024
WINDOW_WIDTH = 786

WINDOWSIZE = (WINDOW_HEIGHT, WINDOW_WIDTH) # bottom right corner of window is position WINDOW_HEIGHT,WINDOW_WIDTH

SCREEN = pygame.display.set_mode(WINDOWSIZE)

#working with Text
FONT = pygame.font.SysFont("Myriad Pro",48)
HELLO = FONT.render("Hello World",1, (255,0,255), (255,255,255))
HELLOsize = HELLO.get_size()

#loading an image
image = pygame.image.load("SweetShip.png")
imageSize = image.get_size()

#for sound
sound = pygame.mixer.Sound("explosn.wav") #needs to be .wavfile I think
pygame.mixer.music.load("roboCop3NES.mp3")

x,y =1,100
directionX = 1
directionY = 1
clock = pygame.time.Clock()
#pygame.mouse.set_visible(0) #removes the visibility of the mouse
pygame.key.set_repeat(1000,10)

pygame.mixer.music.play(1,0.0)#starts the music

while 1:
	clock.tick(60)#runs # of times per second. More times means faster

	
	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_UP]:
		y -= 10
	if keys[pygame.K_DOWN]:
		y += 10
	if keys[pygame.K_LEFT]:
		x -= 10
	if keys[pygame.K_RIGHT]:
		x += 10


	for event in pygame.event.get():	
		if event.type == pygame.QUIT:
			sys.exit()
#KEYBOARD COMMANDS
#		if event.type == pygame.KEYDOWN:
#			if event.key == pygame.K_RIGHT:
#				x += 5
#			if event.key == pygame.K_LEFT:
#				x -= 5
#			if event.key == pygame.K_DOWN:
#				y += 5
#			if event.key == pygame.K_UP:
#				y -= 5


	SCREEN.fill((0,0,0))
	#SCREEN.blit(HELLO,(x,y))
	SCREEN.blit(image,(x,y))
	
	#working with Mouse:
	#mousePosition = pygame.mouse.get_pos()
	#x,y = mousePosition
	if x +imageSize[0]>WINDOW_HEIGHT :
		x=WINDOW_HEIGHT-imageSize[0]
		sound.stop()
		pygame.mixer.Channel(0).play(sound, maxtime=1000)# allows to play over top of music in background
	if y +imageSize[1]>WINDOW_WIDTH :
		y=WINDOW_WIDTH-imageSize[1]
		sound.stop()
		pygame.mixer.Channel(0).play(sound, maxtime=1000)
	if x<=0:
		x=1
		sound.stop()
		pygame.mixer.Channel(0).play(sound, maxtime=1000)
	if y<=0:
		y=1
		sound.stop()
		pygame.mixer.Channel(0).play(sound, maxtime=1000)

	

	#Bouncing Hellow world
	# x +=directionX
	# y += directionY
	# if x + HELLOsize[0]>800 or x<=0:
	#     directionX *=-1
	# if y + HELLOsize[1]>600 or y<=0:
	#     directionY *=-1
		
	
   
	pygame.display.update()

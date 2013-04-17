import sys
import pygame
pygame.init()

size = width, height = 600, 300
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode( size )
ball = pygame.image.load( 'ball.gif' )
ballRect = ball.get_rect()
print ballRect
while 1:
    pygame.time.delay( 3 )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ballRect = ballRect.move( speed )
    if ballRect.left < 0 or ballRect.right > width:
        speed[0] = -speed[0]
    if ballRect.top < 0 or ballRect.bottom > height:
         speed[1] = -speed[1]
         
    screen.fill( black )
    screen.blit( ball, ballRect )
    pygame.display.flip()

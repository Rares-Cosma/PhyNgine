from classes.renderer import *
from classes.body import *
from classes.vertex import *
from classes.collisions import *
import pygame
import random

#fix origin scaling issue

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Pygame Window")
background_color = (0, 0, 0) 

ver=Vertex(random.randint(0,300),random.randint(0,300),0)
ver2=Vertex(random.randint(0,300),random.randint(0,300),0)
ver3=Vertex(random.randint(0,300),random.randint(0,300),0)
bod1=Body([ver,ver2,ver3],Vertex(0,0,0))
bod1._set_origin(collision.get_centeroid(bod1.vertices))

ver_2=Vertex(random.randint(0,300),random.randint(0,300),0)
ver2_2=Vertex(random.randint(0,300),random.randint(0,300),0)
ver3_2=Vertex(random.randint(0,300),random.randint(0,300),0)
bod1_2=Body([ver_2,ver2_2,ver3_2],Vertex(0,0,0))
bod1_2._set_origin(collision.get_centeroid(bod1_2.vertices))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    bod1.rotate(100,0,0)
    bod1_2.rotate(100,0,0)
    
    screen.fill(background_color)
    render_body([0,0,0],bod1,screen)
    draw_trigon(screen,bod1.vertices,pygame.image.load("assets\\black_rook.png"))
    render_body([0,0,0],bod1_2,screen)
    draw_trigon(screen,bod1_2.vertices,pygame.image.load("assets\\black_rook.png"))

    pygame.display.flip()

pygame.quit()
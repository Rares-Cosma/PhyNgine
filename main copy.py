from classes.renderer import *
from classes.body import *
from classes.vertex import *
from classes.collisions import *
import pygame
import random

cam_pos=[0,0,0]

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Pygame Window")
background_color = (0, 0, 0) 

bod1=Body([],Vertex(0,0,0),True)
bod1.load_custom_files("assets\square.ver")
bod1._set_origin(collision.get_centeroid(bod1.vertices))

bod1_2=Body([],Vertex(0,0,0),True)
bod1_2.load_custom_files("assets\square.ver")
bod1_2._set_origin(collision.get_centeroid(bod1_2.vertices))
bod1_2.translate(120,0,0)

bod1_2._set_world_list([bod1,bod1_2])
bod1._set_world_list([bod1,bod1_2])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    bod1.rotate(0,0,1)
    bod1_2.rotate(0,0,1)
    
    screen.fill(background_color)
    render_body(cam_pos,bod1,screen)
    render_body(cam_pos,bod1_2,screen)

    pygame.display.flip()

pygame.quit()
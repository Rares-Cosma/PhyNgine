from classes.renderer import *
from classes.body import *
from classes.vertex import *
from classes.collisions import *
import pygame
import random
import numpy as np

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("phynengine")
background_color = (0, 0, 0) 

bod1=Body([],Vertex(0,0,0),True)
bod1.load_obj("assets\\sphere.obj")
bod1._set_origin(collision.get_centeroid(bod1.vertices))
bod1.scale(220,220,220)
bod1.translate(0,0,200)
bod1._set_origin(collision.get_centeroid(bod1.vertices))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    bod1.rotate(100,0,0)
    #bod1.scale(2,2,2)

    screen.fill(background_color)
    render_body(60,bod1,screen)
    faces=[]
    for i in bod1.faces:
        faces.append(project(60,i.vertices,screen))
    render_faces(screen,faces,pygame.image.load("assets\\black_rook.png"),[0,0,0])
    
    #draw_quad(screen,project(60,bod1.faces[0].vertices,screen),pygame.image.load("assets\\black_rook.png"))
    pygame.display.flip()

pygame.quit()
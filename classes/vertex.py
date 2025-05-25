from numpy import *

class Face:
    def __init__(self, vertices):
        self.vertices = vertices

class Vertex:
    def __init__(self,x,y,z) -> None:
        self.x=x
        self.y=y
        self.z=z
        self.coords=[x,y,z]
    
    def out(self):
        print(self.x,self.y,self.z)

    def translate(self,x,y,z):
        self.x+=x
        self.y+=y
        self.z+=z
        self.coords=[x,y,z]

    def scale(self,x,y,z):
        self.x*=x
        self.y*=y
        self.z*=z
        self.coords=[x,y,z]

    def rotate(self,x,y,z,origin):
        x*=0.0174
        y*=0.0174
        z*=0.0174
        coords = [[self.x-origin.x,self.y-origin.y,self.z-origin.z]]
        r_x =  [[1,      0,       0], 
                [0, cos(x), -sin(x)], 
                [0, sin(x), cos(x)]]
        r_y = [[cos(y),  0, sin(y)],
               [0,       1,     0],
               [-sin(y), 0, cos(y)]]
        r_z =  [[cos(z), -sin(z), 0],
                [sin(z), cos(z),  0], 
                [0,   0,          1]]
        coords=dot(coords,r_x)
        coords=dot(coords,r_y)
        coords=dot(coords,r_z)
        self.x=coords[0][0]+origin.x
        self.y=coords[0][1]+origin.y
        self.z=coords[0][2]+origin.z
        self.coords=[x,y,z]
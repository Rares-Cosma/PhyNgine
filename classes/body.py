from classes.collisions import *
from classes.vertex import *
from numpy import *

class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)

class Body:
    def __init__(self,vertices,origin,use_collision:bool=False,world_list:list=[]):
        self.vertices=vertices
        self.faces=None
        self.is_colliding=False
        self.origin=origin
        self.use_collision=use_collision
        self.centeroid=None
        self.world_list=world_list
        self.shown=True
        for i in self.world_list:
            if i==self:
                self.world_list.remove(i)
        if vertices:
            self.centeroid=collision.get_centeroid(self.vertices)
        self.linedict={}

    #transforms
    
    def translate(self,x:int,y:int,z:int):
        y=-y
        for i in self.vertices:
            i.translate(x,y,z)
        self.origin.translate(x,y,z)
        if self.vertices and self.centeroid:
            self.centeroid.translate(x,y,z)
        
        self.is_colliding=False

        if self.use_collision:
            for i in self.world_list:
                if collision.check_collision(collision,self,i):
                    for i in self.vertices:
                        i.translate(-x,-y,-z)
                        self.origin.translate(-x,-y,-z)
                        if self.vertices and self.centeroid:
                            self.centeroid.translate(-x,-y,-z)
                    self.is_colliding=True
    
    def scale(self,x:int,y:int,z:int):
        for i in self.vertices:
            i.scale(x,y,z)
        self.origin.scale(x,y,z)
        if self.vertices and self.centeroid:
            self.centeroid.scale(x,y,z)
        
        self.is_colliding=False

        if self.use_collision:
            for i in self.world_list:
                if collision.check_collision(collision,self,i):
                    for i in self.vertices:
                        i.scale(-x,-y,-z)
                        self.origin.scale(-x,-y,-z)
                        if self.vertices and self.centeroid:
                            self.centeroid.scale(-x,-y,-z)
                    self.is_colliding=True

    def rotate(self,x,y,z):
        x*=0.0174
        y*=0.0174
        z*=0.0174
        for i in self.vertices:
            i.rotate(x,y,z,self.origin)
        
        #regres if collided

        self.is_colliding=False
        
        if self.use_collision:
            for i in self.world_list:
                if collision.check_collision(collision,self,i):
                    for j in self.vertices:
                        j.rotate(-x,-y,-z,self.origin)
                        self.is_colliding=True

    #other

    def show(self):
        self.shown=True

    def hide(self):
        self.shown=False

    def _set_origin(self,origin):
        self.origin=origin
    
    def _set_line_dict(self,linedict):
        self.linedict=linedict
    
    def _set_world_list(self,world_list:list):
        self.world_list=world_list
        for i in self.world_list:
            if i==self:
                self.world_list.remove(i)

    def load_custom_files(self,filepath:str):
        self.vertices=[]
        with open(filepath,'r') as f:
            text=f.readlines()
            for i in text:
                if not i.startswith('{'):
                    x=i.split(' ')
                    self.vertices.append(Vertex(int(x[0]),int(x[1]),int(x[2])))
                else:
                    keys=[]
                    values=[]
                    i=i.replace('{','')
                    i=i.replace('}','')
                    i=i.split(',')
                    for j in i:
                        d=j.split(':')
                        keys.append(self.vertices[int(d[0])])
                        values.append(self.vertices[int(d[1])])
                    x=Dictlist()
                    ind=-1
                    for i in keys:
                        ind+=1
                        x[i]=values[ind]
                    self._set_line_dict(x)
        self.centeroid=collision.get_centeroid(self.vertices)
        self.origin=self.centeroid
    
    def load_obj(self,filename:str):
        self.vertices = []
        self.faces = []

        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    # Vertex line
                    parts = line.split()
                    x, y, z = map(float, parts[1:])
                    self.vertices.append(Vertex(x, y, z))
                elif line.startswith('f '):
                    # Face line
                    parts = line.split()
                    face_vertices = []
                    for part in parts[1:]:
                        # Face vertices can be in the format 'v' or 'v/t/n'
                        vertex_index = int(part.split('/')[0]) - 1
                        face_vertices.append(self.vertices[vertex_index])
                    self.faces.append(Face(face_vertices))

        
from .vertex import *

class line:
    def __init__(self,A:Vertex,B:Vertex) -> None:
        self.a=A
        self.b=B
        self.vertices=[self.a,self.b]
    
    def __str__(self):
        return self.vertices

class collision:
    def ccw(self,A:Vertex,B:Vertex,C:Vertex):
        return (C.coords[1]-A.coords[1])*(B.coords[0]-A.coords[0]) > (B.coords[1]-A.coords[1])*(C.coords[0]-A.coords[0])
    def intersect(self,AB:line,CD:line):
        return self.ccw(self,AB.a,CD.a,CD.b) != self.ccw(self,AB.b,CD.a,CD.b) and self.ccw(self,AB.a,AB.b,CD.a) != self.ccw(self,AB.a,AB.b,CD.b)
    
    def get_centeroid(vertices:list[Vertex]):
        all_x=[]
        all_y=[]
        all_z=[]
        for i in vertices:
            all_x.append(i.coords[0])
            all_y.append(i.coords[1])
            all_z.append(i.coords[2])
        m_x=(max(all_x)+min(all_x))/2
        m_y=(max(all_y)+min(all_y))/2
        m_z=(max(all_z)+min(all_z))/2
        return Vertex(m_x,m_y,m_z)
    
    def all_comb(self,list:list):
        fl=[]
        for i in list:
            for x in list:
                fl.append(line(i,x))
        return fl
    
    
    def check_collision(self,body1, body2):
        def get_bounding_box(vertices):
            min_x = min(vertex.x for vertex in vertices)
            max_x = max(vertex.x for vertex in vertices)
            min_y = min(vertex.y for vertex in vertices)
            max_y = max(vertex.y for vertex in vertices)
            min_z = min(vertex.z for vertex in vertices)
            max_z = max(vertex.z for vertex in vertices)
            return min_x, max_x, min_y, max_y, min_z, max_z

        box1 = get_bounding_box(body1.vertices)
        box2 = get_bounding_box(body2.vertices)

        return not (box1[1] < box2[0] or box1[0] > box2[1] or
                    box1[3] < box2[2] or box1[2] > box2[3] or
                    box1[5] < box2[4] or box1[4] > box2[5])
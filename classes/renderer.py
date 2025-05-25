from pygame import *
import numpy as np
from .vertex import *
from .body import *
from .collisions import *
    
def triangulate_face(face):
    if len(face) < 3:
        return []
    if len(face) == 3:
        return [face]
    
    triangles = []
    for i in range(1, len(face) - 1):
        triangles.append([face[0], face[i], face[i + 1]])
    
    return triangles


def compute_face_normal(face):
    v1 = np.array([face[1][0] - face[0][0], face[1][1] - face[0][1], face[1][2] - face[0][2]])
    v2 = np.array([face[2][0] - face[0][0], face[2][1] - face[0][1], face[2][2] - face[0][2]])
    normal = np.cross(v1, v2)
    return normal

def get_face_depth(face):
    vfaces=[]
    tface=[]
    for i in face:
        x=Vertex(i[0],i[1],i[2])
        tface.append(x)
    vfaces.append(tface)
    tface=[]

    tcents=[]
    col=collision
    for i in vfaces:
        tcents.append(col.get_centeroid(i))
    print(tcents)
    
    return sum(vertex[2] for vertex in face) / len(face)

def render_faces(surface, faces, texture, camera_pos):
    visible_faces = []
    for face in faces:
        triangles = triangulate_face(face)
        for triangle in triangles:
                depth = get_face_depth(triangle)
                visible_faces.append((depth, triangle))
    
    visible_faces.sort(key=lambda item: item[0], reverse=True)
    
    ct=0
    for _, triangle in visible_faces:
        if ct<6:
            draw_trigon(surface, triangle, texture)
            ct+=1

def new_render_vert(fov, vert_arr, screen):
    width, height = screen.get_size()
    for vertex in vert_arr:
        # Perspective projection
        factor = fov / (fov + vertex.z)
        x = vertex.x * factor + width / 2
        y = -vertex.y * factor + height / 2
        draw.circle(screen, (45, 255, 90), (int(x), int(y)), 3)

def project(fov,vert_arr,screen):
    width, height = screen.get_size()
    verts=[]
    for vertex in vert_arr:
        # Perspective projection
        factor = fov / (fov + vertex.z)
        x = vertex.x * factor + width / 2
        y = -vertex.y * factor + height / 2
        verts.append([x,y,0])
    return verts

def render_body(fov,body,screen):
    if body.shown:
        new_render_vert(fov,body.vertices,screen)

def lerp2d(p1, p2, f):
    return [lerp(p1.x, p2.x, f), lerp(p1.y, p2.y, f), lerp(p1.z, p2.z, f)]
def lerp2d_vertex(p1, p2, f):
    return [lerp(p1[0], p2[0], f), lerp(p1[1], p2[1], f), lerp(p1[2], p2[2], f)]

def lerp(a, b, f):
    return a + f * (b - a)

def draw_trigon(surface, trigon, img):
    points = dict()

    for i in range(img.get_size()[1] + 1):
        b = lerp2d_vertex(trigon[0], trigon[2], i / img.get_size()[1])
        a = lerp2d_vertex(trigon[1], trigon[2], i / img.get_size()[1])
        c = lerp2d_vertex(trigon[1], trigon[0], i / img.get_size()[1])

        for u in range(img.get_size()[0] + 1):
            v = lerp2d_vertex(b, a, u / img.get_size()[0])
            points[(u, i)] = v

    for x in range(img.get_size()[0]):
        for y in range(img.get_size()[1]):
            draw.polygon(
                surface,
                img.get_at((x, y)),
                [tuple(map(int, (points[(a, b)][0], points[(a, b)][1]))) for a, b in [(x, y), (x, y+1), (x+1, y+1), (x+1, y)]]
            )

def draw_quad(surface, quad, img):
    points = dict()

    # Interpolating points for the quad
    for i in range(img.get_size()[1] + 1):
        left_edge = lerp2d_vertex(quad[0], quad[3], i / img.get_size()[1])
        right_edge = lerp2d_vertex(quad[1], quad[2], i / img.get_size()[1])

        for u in range(img.get_size()[0] + 1):
            v = lerp2d_vertex(left_edge, right_edge, u / img.get_size()[0])
            points[(u, i)] = v

    # Drawing the interpolated points as polygons
    for x in range(img.get_size()[0]):
        for y in range(img.get_size()[1]):
            draw.polygon(
                surface,
                img.get_at((x, y)),
                [tuple(map(int, (points[(a, b)][0], points[(a, b)][1]))) for a, b in [(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y)]]
            )

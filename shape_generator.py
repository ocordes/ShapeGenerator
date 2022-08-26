# shape_generator.py
#
# written by: Oliver Cordes 2022-08-24
# changed by: Oliver Cordes 2022-08-24

import bpy

import bmesh
import datetime
from math import sqrt, radians, pi, cos, sin
from mathutils import Vector, Matrix
from random import random, seed, uniform, randint, randrange
from enum import IntEnum
from colorsys import hls_to_rgb



def ShapeGen1(dimX=1, dimY=1, subdivX=1, subdivY=1):
    # Let's start with a unit BMesh cube scaled randomly
    bm = bmesh.new()
    #bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.create_grid(bm, x_segments=subdivX, y_segments=subdivY, size=1, calc_uvs=True) 
    scale_vec = Vector((dimX, dimY, 1))
    bmesh.ops.scale(bm, vec=scale_vec, verts=bm.verts)
    
    # Finish up, write the bmesh into a new mesh
    me = bpy.data.meshes.new('Mesh')
    bm.to_mesh(me)
    bm.free()

    # Add the mesh to the scene
    scene = bpy.context.scene
    obj = bpy.data.objects.new('ShapeGen1', me)
    # scene.objects.link(obj)
    scene.collection.objects.link(obj)

    # Select and make active
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    # scene.objects.active = obj
    # obj.select = True



def main(context):
    ShapeGen1()
    
    for ob in context.scene.objects:
        print(ob)


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    # works only after registrations
    #bpy.ops.object.simple_operator()
    ShapeGen1(dimX=2, dimY=4, subdivX=2, subdivY=8)

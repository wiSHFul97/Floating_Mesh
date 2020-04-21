import bpy
import bmesh
from mathutils import Vector
import math
from .float_mesh_data import Float_Mesh_Date
  
class MESH_OT_set_segment(bpy.types.Operator):
    """Assign Segment to Selected Verts"""
    bl_idname = "mesh.set_segment"
    bl_label = "Assign Segment"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        print(dir(context))
        obj = context.active_object
        b_obj = bmesh.from_edit_mesh(obj.data)
        selected_verts = [v for v in b_obj.verts if v.select]
        print(selected_verts)
        # find active_vert --> last vert of segment
        active_vert = None
        for active_vert in reversed(b_obj.select_history):
            if isinstance(active_vert, bmesh.types.BMVert):
                print("Active vertex:", active_vert)
                break
        # TODO if active_vert is none: maybe cycle (handle cycles) requires origin
        # find first vert 
        first_vert = None
        for first_vert in selected_verts:
            if first_vert != active_vert and (len(first_vert.link_edges) == 1 or first_vert.link_edges[0].select != first_vert.link_edges[1].select):
                print(first_vert)
                break
        
        # find second vert (for direction)
        second_vert = first_vert.link_edges[0]
        
        # TODO momkene ke dadeye ra's ha az bein bere! bayad update shan ba avaz shodane subdiv lvl? 
        # TODO validate new segement
        # Float_Mesh_Date.segments.append()
        # elem.select = False
        # bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MESH_OT_set_segment)


def unregister():
    bpy.utils.unregister_class(MESH_OT_set_segment)


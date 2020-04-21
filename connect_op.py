import bpy
import bmesh
from mathutils import Vector
import math
# import os, sys
# directory = os.path.dirname(bpy.data.filepath)
# if not directory in sys.path:
#     sys.path.append(directory)
# from importlib import reload
# from dyn_mesh_utils import *
# reload(sys.modules['dyn_mesh_utils'])
from .dyn_mesh_utils import (convert_index, calculate_part_subdiv_lvl, slide_verts,
    add_additional_verts, slide_last_verts, get_line_vectors, out_slide_verts)
	
class MESH_OT_connect(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.connect"
    bl_label = "Connect"
    bl_options = {'REGISTER', 'UNDO'}
    connect_type: bpy.props.IntProperty(
        name='connect_type',
        description='connection type',
        default=1,
		min=1, max=2,
    )
    
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        # initialize
        wire = context.active_object
        b_wire = bmesh.from_edit_mesh(wire.data)
        origin = [v for v in b_wire.verts if v.select][0]
        prev_vert = origin
        current_vert = prev_vert.link_edges[0].other_vert(prev_vert)
        move_constant = (1 - 1/self.subdiv_lvl)

        if move_constant > 0:
            # slide existing verts
            move_percentage, last_vert, second_last_vert, line_vectors = slide_verts(len(b_wire.verts)-2,
                                                                    prev_vert, current_vert, move_constant, -2)
            # last vert and additional verts:
            move_percentage += move_constant
            additional_vert_count = math.ceil(move_percentage/(1-move_constant))
            second_last_vert, last_vert = add_additional_verts(last_vert, second_last_vert, additional_vert_count, b_wire)
            bmesh.update_edit_mesh(wire.data)
            
            # sliding additional verts into proper position
            slide_last_verts(additional_vert_count, second_last_vert, last_vert,
                                move_constant, move_percentage, -1, line_vectors)        
        else:
            line_vectors = get_line_vectors(len(b_wire.verts)-1, prev_vert, current_vert)
            out_slide_verts(line_vectors, prev_vert, current_vert, move_constant)

        # revert selection
        bpy.ops.mesh.select_all(action='DESELECT')
        # origin.select = True
        bmesh.update_edit_mesh(wire.data)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MESH_OT_connect)


def unregister():
    bpy.utils.unregister_class(MESH_OT_connect)


# if __name__ == "__main__":
#     register()


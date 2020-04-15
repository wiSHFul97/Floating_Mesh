import bpy
import bmesh
from mathutils import Vector
import math
import os, sys
directory = os.path.dirname(bpy.data.filepath)
if not directory in sys.path:
    sys.path.append(directory)
from importlib import reload
from dyn_mesh_utils import *
reload(sys.modules['dyn_mesh_utils'])

# todo think: har vaght move_percentage > 1 beshe dige az oonja be ba'd > 1 hast...
# todo bug: if subdiv_lvl == 1: ye vert ezafe mishe alaki ...
         
class MESH_OT_float_subdiv(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.subdiv_float"
    bl_label = "Float Subdivide"
    bl_options = {'REGISTER', 'UNDO'}
    subdiv_lvl: bpy.props.FloatProperty(
        name='subdiv_lvl',
        description='float subdivision level',
        default=1.2,
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
            second_last_vert, last_vert = add_additional_verts(last_vert, second_last_vert, additional_vert_count, wire, b_wire)
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
    bpy.utils.register_class(MESH_OT_float_subdiv)


def unregister():
    bpy.utils.unregister_class(MESH_OT_float_subdiv)


if __name__ == "__main__":
    register()


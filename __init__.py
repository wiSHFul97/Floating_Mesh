bl_info = {
    "name": "Floating Mesh",
    "author": "Hossein Fatemi",
    "version": (1, 0),
    "blender": (2, 82, 0),
    "category": "Mesh",
    "location": "N bar",
    "description": "Floating Meshes!",
}

modulesNames = ['float_subdiv', 'dyn_mesh_utils', 'connect_op', 'float_mesh_ui', 'set_segment_op']

import sys
import importlib

modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)
 
def register():
    print('register')
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()
 
def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    print('hello1')
    register()


# modulesNames = ['float_subdiv']
# import bpy
# from ./operators import float_subdiv
# # from float_subdiv import MESH_OT_float_subdiv
# def register():
#     print('registered')
#     bpy.utils.register_class(float_subdiv.MESH_OT_float_subdiv)
# def unregister():
#     bpy.utils.unregister_class(float_subdiv.MESH_OT_float_subdiv)

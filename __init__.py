bl_info = {
    "name": "Render what I see",
    "author": "Ian Zelbo",
    "version": (1, 0),
    "blender": (4, 3, 0),
    "location": "View3D > Sidebar > Render Tab",
    "description": "Sync render visibility with viewport visibility.",
}

import bpy

class OBJECT_OT_sync_visibility(bpy.types.Operator):
    bl_idname = "object.sync_visibility"
    bl_label = "Render what I see"
    bl_description = "Sync render visibility with viewport visibility."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # If an object is visible in the viewport, set its render visibility (hide_render)
        for obj in context.view_layer.objects:
            obj.hide_render = not obj.visible_get()
        
        # We need to recursively sync the render visibility of collections with their viewport visibility bc of collections
        def sync_collection(layer_collection, parent_visible=True):
            # True ONLY if both the parent is visible and the current collection is not hidden in the viewport
            effective_visible = parent_visible and (not layer_collection.hide_viewport)
            layer_collection.collection.hide_render = not effective_visible
            for child in layer_collection.children:
                sync_collection(child, effective_visible)
        
        root = context.view_layer.layer_collection
        for child in root.children:
            sync_collection(child, True)
        
        self.report({'INFO'}, "Render visibility synced with viewport visibility.")
        return {'FINISHED'}

# Adds a reload button to the Outliner header. Due to Blender API limitations, it's always at the end
def draw_outliner_header(self, context):
    self.layout.operator("object.sync_visibility", icon="FILE_REFRESH", text="")

def register():
    bpy.utils.register_class(OBJECT_OT_sync_visibility)
    bpy.types.OUTLINER_HT_header.append(draw_outliner_header)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_sync_visibility_panel)
    bpy.types.OUTLINER_HT_header.remove(draw_outliner_header)

if __name__ == "__main__":
    register()

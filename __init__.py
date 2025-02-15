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

class VIEW3D_PT_sync_visibility_panel(bpy.types.Panel):
    bl_label = "Render what I see"
    bl_idname = "VIEW3D_PT_sync_visibility_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Render'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.sync_visibility", text="Sync Camera Visibility")

def register():
    bpy.utils.register_class(OBJECT_OT_sync_visibility)
    bpy.utils.register_class(VIEW3D_PT_sync_visibility_panel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_sync_visibility_panel)
    bpy.utils.unregister_class(OBJECT_OT_sync_visibility)

if __name__ == "__main__":
    register()
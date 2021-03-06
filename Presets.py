import bpy

from bl_operators.presets import AddPresetBase

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty,
                       FloatProperty,
                       )

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList,
                       Menu,
                       )

# -------------------------------------------------------------------
#   Operators
# -------------------------------------------------------------------

class PRESETS_OT_Length_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_length.list_action"
    bl_label = "Actions"
    bl_description = "Move items up and down or remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            # ('ADD', "Add", "")
            )
            )

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.presets_length_index

        try:
            item = scn.presets_length[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.presets_length) - 1:
                # item_next = scn.presets_length[idx+1].name
                scn.presets_length.move(idx, idx+1)
                scn.presets_length_index += 1

            elif self.action == 'UP' and idx >= 1:
                # item_prev = scn.presets_length[idx-1].name
                scn.presets_length.move(idx, idx-1)
                scn.presets_length_index -= 1
            elif self.action == 'REMOVE':
                # info = 'Item "%s" removed from list' % (scn.presets_length[idx].name)
                scn.presets_length_index -= 1
                scn.presets_length.remove(idx)

            # bpy.context.scene.presets_length_save = 1

        # if self.action == 'ADD':
        #     if context.object:

        #         # def ret(self):
        #         #     return bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")

        #         # context.window_manager.invoke_popup(self, width = 190)
                
        #         # def draw(self, context):

        #         # idx = context.scene.presets_length_index
        #         # scn = bpy.context.scene.presets_length[idx]

        #         item = scn.presets_length.add()
        #         # ret(self)
        #         # bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")
        #         # item.name = bpy.context.scene.presets_length[idx].name
        #         item.name = context.object.name
        #         item.obj_type = context.object.type
        #         item.obj_id = len(scn.presets_length)
        #         item.unit = bpy.context.window_manager.setprecisemesh.length
        #         scn.presets_length_index = len(scn.presets_length)-1
        #     else:
        #         self.report({'INFO'}, "Nothing selected in the Viewport")


        return {"FINISHED"}
class PRESETS_OT_Length_actions_add(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_length.list_action_add"
    bl_label = "Add"
    bl_description = "Add item"
    bl_options = {'REGISTER'}
    # bl_options = {'BLOCKING'}
    # bl_options = {'INTERNAL'}

    name_input: StringProperty(
        name = "Name")
    unit_input: FloatProperty(
        name="Length",
        description="Length of the edge",
        default=1.0,
        step = 100.0,
        unit='LENGTH',
        precision = 6,)

    def draw(self, context):
        layout = self.layout

        # row = layout.row()
        # row.alignment = "RIGHT"
        # row.scale_x = 1.7
        layout.prop(self, "unit_input", text = "")

        layout.prop(self, "name_input", text = "Name")


    def invoke(self, context, event):
        self.unit_input = bpy.context.window_manager.setprecisemesh.length
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scn = context.scene
        idx = scn.presets_length_index

        try:
            item = scn.presets_length[idx]
        except IndexError:
            pass
            
        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_length) - 1):
                if scn.presets_length[i].name == self.name_input and i != len(scn.presets_length) - 1:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break

            item = scn.presets_length.add()

            item.name = self.name_input
            item.unit = self.unit_input


            # item.obj_id = len(scn.presets_length)
            scn.presets_length_index = len(scn.presets_length) - 1

            # bpy.context.scene.presets_length_save = 1
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}
class PRESETS_OT_Length_actions_refresh(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_length.list_action_refresh"
    bl_label = "Export"
    bl_description = "Export item"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        bpy.context.scene.presets_length_index = self.my_index

        scn = context.scene
        idx = scn.presets_length_index

        try:
            item = scn.presets_length[idx]
        except IndexError:
            pass
            
        if bpy.context.active_object:
    
            bpy.context.window_manager.setprecisemesh.length = item.unit

            # bpy.context.region.tag_redraw()
            # context.area.tag_redraw()
            # bpy.context.scene.update()

            # for region in context.area.regions:
            #     if region.type == "UI":
            #         region.tag_redraw()

            # bpy.data.scenes.update()

            
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
            print("Warning because of Set Precise Mesh")



            # bpy.ops.wm.redraw_timer(type = "UNDO", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW", iterations = 1, time_limit = 0.0)

        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}
class PRESETS_OT_Length_actions_import(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_length.list_action_import"
    bl_label = "Import"
    bl_description = "Import item"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        scn = context.scene
        idx = scn.presets_length_index

        try:
            item = scn.presets_length[self.my_index]
        except IndexError:
            pass
            
        if bpy.context.active_object:
    
            item.unit = bpy.context.window_manager.setprecisemesh.length

            # bpy.context.region.tag_redraw()
            # context.area.tag_redraw()
            # bpy.context.scene.update()

            # for region in context.area.regions:
            #     if region.type == "UI":
            #         region.tag_redraw()

            # bpy.data.scenes.update()

            
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
            print("Warning because of Set Precise Mesh")



            # bpy.ops.wm.redraw_timer(type = "UNDO", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)

        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}
class PRESETS_OT_Length_Rename(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_length.rename"
    bl_label = "Rename"
    bl_description = "Rename item"
    bl_options = {'INTERNAL'}

    name_input: StringProperty()
    my_index: IntProperty()

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):

        scn = context.scene

        try:
            item = scn.presets_length[self.my_index]
        except IndexError:
            pass

        self.name_input = item.name

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        scn = context.scene

        try:
            item = scn.presets_length[self.my_index]
        except IndexError:
            pass

        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_length) - 1):
                if scn.presets_length[i].name == self.name_input and i != self.my_index:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break
            
            item.name = self.name_input

            # bpy.context.scene.presets_length_save = 1
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")



        return {"FINISHED"}
class PRESETS_OT_Length_Change_unit(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_length.change_unit"
    bl_label = "Change unit"
    bl_description = "Rename item"
    bl_options = {'INTERNAL'}

    name_input: StringProperty()
    my_index: IntProperty()

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):

        scn = context.scene

        try:
            item = scn.presets_length[self.my_index]
        except IndexError:
            pass

        self.name_input = item.name

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        scn = context.scene

        try:
            item = scn.presets_length[self.my_index]
        except IndexError:
            pass

        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_length) - 1):
                if scn.presets_length[i].name == self.name_input and i != self.my_index:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break
            
            item.name = self.name_input

            # bpy.context.scene.presets_length_save = 1
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")



        return {"FINISHED"}
class PRESETS_OT_Length_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_length.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.presets_length)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.presets_length):
            context.scene.presets_length.clear()
            self.report({'INFO'}, "All items removed")
            # bpy.context.scene.presets_length_save = 1
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}

# class PRESETS_OT_removeDuplicates(Operator):
#     """Remove all duplicates"""
#     bl_idname = "presets_length.remove_duplicates"
#     bl_label = "Remove Duplicates"
#     bl_description = "Remove all duplicates"
#     bl_options = {'INTERNAL'}

#     def find_duplicates(self, context):
#         """find all duplicates by name"""
#         name_lookup = {}
#         for c, i in enumerate(context.scene.presets_length):
#             name_lookup.setdefault(i.name, []).append(c)
#         duplicates = set()
#         for name, indices in name_lookup.items():
#             for i in indices[1:]:
#                 duplicates.add(i)
#         return sorted(list(duplicates))

#     @classmethod
#     def poll(cls, context):
#         return bool(context.scene.presets_length)

#     def execute(self, context):
#         scn = context.scene
#         removed_items = []
#         # Reverse the list before removing the items
#         for i in self.find_duplicates(context)[::-1]:
#             scn.presets_length.remove(i)
#             removed_items.append(i)
#         if removed_items:
#             scn.presets_length_index = len(scn.presets_length)-1
#             info = ', '.join(map(str, removed_items))
#             self.report({'INFO'}, "Removed indices: %s" % (info))
#         else:
#             self.report({'INFO'}, "No duplicates")
#         return{'FINISHED'}

#     def invoke(self, context, event):
#         return context.window_manager.invoke_confirm(self, event)

class PRESETS_OT_Angle_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_angle.list_action"
    bl_label = "Actions"
    bl_description = "Move items up and down or remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            # ('ADD', "Add", "")
            )
            )

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.presets_angle_index

        try:
            item = scn.presets_angle[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.presets_angle) - 1:
                # item_next = scn.presets_angle[idx+1].name
                scn.presets_angle.move(idx, idx+1)
                scn.presets_angle_index += 1

            elif self.action == 'UP' and idx >= 1:
                # item_prev = scn.presets_angle[idx-1].name
                scn.presets_angle.move(idx, idx-1)
                scn.presets_angle_index -= 1
            elif self.action == 'REMOVE':
                # info = 'Item "%s" removed from list' % (scn.presets_angle[idx].name)
                scn.presets_angle_index -= 1
                scn.presets_angle.remove(idx)

        # if self.action == 'ADD':
        #     if context.object:

        #         # def ret(self):
        #         #     return bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")

        #         # context.window_manager.invoke_popup(self, width = 190)
                
        #         # def draw(self, context):

        #         # idx = context.scene.presets_angle_index
        #         # scn = bpy.context.scene.presets_angle[idx]

        #         item = scn.presets_angle.add()
        #         # ret(self)
        #         # bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")
        #         # item.name = bpy.context.scene.presets_angle[idx].name
        #         item.name = context.object.name
        #         item.obj_type = context.object.type
        #         item.obj_id = len(scn.presets_angle)
        #         item.unit = bpy.context.window_manager.setprecisemesh.length
        #         scn.presets_angle_index = len(scn.presets_angle)-1
        #     else:
        #         self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}
class PRESETS_OT_Angle_actions_add(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_angle.list_action_add"
    bl_label = "Add"
    bl_description = "Add item"
    bl_options = {'REGISTER'}
    # bl_options = {'BLOCKING'}
    # bl_options = {'INTERNAL'}

    name_input: StringProperty(
        name = "Name")
    unit_input: FloatProperty(
        name="Angle",
        description="Angle",
        min=-360.0, max=360.0,
        default=0.0,
        step = 100.0,
        unit="ROTATION",
        precision = 6,)

    def draw(self, context):
        layout = self.layout

        # row = layout.row()
        # row.alignment = "RIGHT"
        # row.scale_x = 1.7
        layout.prop(self, "unit_input", text = "")

        layout.prop(self, "name_input", text = "Name")


    def invoke(self, context, event):
        self.unit_input = bpy.context.window_manager.setprecisemesh.angle
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scn = context.scene
        idx = scn.presets_angle_index

        try:
            item = scn.presets_angle[idx]
        except IndexError:
            pass
            
        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_angle) - 1):
                if scn.presets_angle[i].name == self.name_input and i != len(scn.presets_angle) - 1:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break

            item = scn.presets_angle.add()

            item.name = self.name_input
            item.unit = self.unit_input


            # item.obj_id = len(scn.presets_angle)
            scn.presets_angle_index = len(scn.presets_angle) - 1
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}
class PRESETS_OT_Angle_actions_refresh(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_angle.list_action_refresh"
    bl_label = "Export"
    bl_description = "Export item"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        bpy.context.scene.presets_angle_index = self.my_index

        scn = context.scene
        idx = scn.presets_angle_index

        try:
            item = scn.presets_angle[idx]
        except IndexError:
            pass
            
        if bpy.context.active_object:
    
            bpy.context.window_manager.setprecisemesh.angle = item.unit

            # bpy.context.region.tag_redraw()
            # context.area.tag_redraw()
            # bpy.context.scene.update()

            # for region in context.area.regions:
            #     if region.type == "UI":
            #         region.tag_redraw()

            # bpy.data.scenes.update()

            
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
            print("Warning because of Set Precise Mesh")



            # bpy.ops.wm.redraw_timer(type = "UNDO", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW", iterations = 1, time_limit = 0.0)

        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}
class PRESETS_OT_Angle_actions_import(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_angle.list_action_import"
    bl_label = "Import"
    bl_description = "Import item"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        scn = context.scene
        idx = scn.presets_angle_index

        try:
            item = scn.presets_angle[self.my_index]
        except IndexError:
            pass
            
        if bpy.context.active_object:
    
            item.unit = bpy.context.window_manager.setprecisemesh.angle

            # bpy.context.region.tag_redraw()
            # context.area.tag_redraw()
            # bpy.context.scene.update()

            # for region in context.area.regions:
            #     if region.type == "UI":
            #         region.tag_redraw()

            # bpy.data.scenes.update()

            
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
            print("Warning because of Set Precise Mesh")



            # bpy.ops.wm.redraw_timer(type = "UNDO", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)

        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}
class PRESETS_OT_Angle_Rename(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_angle.rename"
    bl_label = "Rename"
    bl_description = "Rename item"
    bl_options = {'INTERNAL'}

    name_input: StringProperty()
    my_index: IntProperty()

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):

        scn = context.scene

        try:
            item = scn.presets_angle[self.my_index]
        except IndexError:
            pass

        self.name_input = item.name

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        scn = context.scene

        try:
            item = scn.presets_angle[self.my_index]
        except IndexError:
            pass


        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_angle) - 1):
                if scn.presets_angle[i].name == self.name_input and i != self.my_index:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break
            
            item.name = self.name_input
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")


        return {"FINISHED"}
class PRESETS_OT_Angle_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_angle.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.presets_angle)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.presets_angle):
            context.scene.presets_angle.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}




class PRESETS_OT_Area_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_area.list_action"
    bl_label = "Actions"
    bl_description = "Move items up and down or remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            # ('ADD', "Add", "")
            )
            )

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.presets_area_index

        try:
            item = scn.presets_area[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.presets_area) - 1:
                # item_next = scn.presets_area[idx+1].name
                scn.presets_area.move(idx, idx+1)
                scn.presets_area_index += 1

            elif self.action == 'UP' and idx >= 1:
                # item_prev = scn.presets_area[idx-1].name
                scn.presets_area.move(idx, idx-1)
                scn.presets_area_index -= 1
            elif self.action == 'REMOVE':
                # info = 'Item "%s" removed from list' % (scn.presets_area[idx].name)
                scn.presets_area_index -= 1
                scn.presets_area.remove(idx)

            # bpy.context.scene.presets_area_save = 1

        # if self.action == 'ADD':
        #     if context.object:

        #         # def ret(self):
        #         #     return bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")

        #         # context.window_manager.invoke_popup(self, width = 190)
                
        #         # def draw(self, context):

        #         # idx = context.scene.presets_area_index
        #         # scn = bpy.context.scene.presets_area[idx]

        #         item = scn.presets_area.add()
        #         # ret(self)
        #         # bpy.ops.wm.menu_setprecisemesh_operator_2("INVOKE_DEFAULT")
        #         # item.name = bpy.context.scene.presets_area[idx].name
        #         item.name = context.object.name
        #         item.obj_type = context.object.type
        #         item.obj_id = len(scn.presets_area)
        #         item.unit = bpy.context.window_manager.setprecisemesh.area
        #         scn.presets_area_index = len(scn.presets_area)-1
        #     else:
        #         self.report({'INFO'}, "Nothing selected in the Viewport")


        return {"FINISHED"}
class PRESETS_OT_Area_actions_add(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_area.list_action_add"
    bl_label = "Add"
    bl_description = "Add item"
    bl_options = {'REGISTER'}
    # bl_options = {'BLOCKING'}
    # bl_options = {'INTERNAL'}

    name_input: StringProperty(
        name = "Name")
    unit_input: FloatProperty(
        name="area",
        description="area of the edge",
        default=1.0,
        step = 100.0,
        unit='LENGTH',
        precision = 6,)

    def draw(self, context):
        layout = self.layout

        # row = layout.row()
        # row.alignment = "RIGHT"
        # row.scale_x = 1.7
        layout.prop(self, "unit_input", text = "")

        layout.prop(self, "name_input", text = "Name")


    def invoke(self, context, event):
        self.unit_input = bpy.context.window_manager.setprecisemesh.area
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scn = context.scene
        idx = scn.presets_area_index

        try:
            item = scn.presets_area[idx]
        except IndexError:
            pass
            
        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_area) - 1):
                if scn.presets_area[i].name == self.name_input and i != len(scn.presets_area) - 1:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break

            item = scn.presets_area.add()

            item.name = self.name_input
            item.unit = self.unit_input


            # item.obj_id = len(scn.presets_area)
            scn.presets_area_index = len(scn.presets_area) - 1

            # bpy.context.scene.presets_area_save = 1
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}
class PRESETS_OT_Area_actions_refresh(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_area.list_action_refresh"
    bl_label = "Export"
    bl_description = "Export item"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        bpy.context.scene.presets_area_index = self.my_index

        scn = context.scene
        idx = scn.presets_area_index

        try:
            item = scn.presets_area[idx]
        except IndexError:
            pass
            
        if bpy.context.active_object:
    
            bpy.context.window_manager.setprecisemesh.area = item.unit

            # bpy.context.region.tag_redraw()
            # context.area.tag_redraw()
            # bpy.context.scene.update()

            # for region in context.area.regions:
            #     if region.type == "UI":
            #         region.tag_redraw()

            # bpy.data.scenes.update()

            
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
            print("Warning because of Set Precise Mesh")



            # bpy.ops.wm.redraw_timer(type = "UNDO", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW", iterations = 1, time_limit = 0.0)

        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}
class PRESETS_OT_Area_actions_import(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "presets_area.list_action_import"
    bl_label = "Import"
    bl_description = "Import item"
    bl_options = {'REGISTER'}

    my_index: IntProperty()

    def execute(self, context):

        scn = context.scene
        idx = scn.presets_area_index

        try:
            item = scn.presets_area[self.my_index]
        except IndexError:
            pass
            
        if bpy.context.active_object:
    
            item.unit = bpy.context.window_manager.setprecisemesh.area

            # bpy.context.region.tag_redraw()
            # context.area.tag_redraw()
            # bpy.context.scene.update()

            # for region in context.area.regions:
            #     if region.type == "UI":
            #         region.tag_redraw()

            # bpy.data.scenes.update()

            
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)
            bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1)
            print("Warning because of Set Precise Mesh")



            # bpy.ops.wm.redraw_timer(type = "UNDO", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_SWAP", iterations = 1, time_limit = 0.0)
            # bpy.ops.wm.redraw_timer(type = "DRAW", iterations = 1, time_limit = 0.0)

            # bpy.ops.wm.redraw_timer(type = "DRAW_WIN_SWAP", iterations = 1, time_limit = 0.0)

        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")

        return {"FINISHED"}
class PRESETS_OT_Area_Rename(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_area.rename"
    bl_label = "Rename"
    bl_description = "Rename item"
    bl_options = {'INTERNAL'}

    name_input: StringProperty()
    my_index: IntProperty()

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):

        scn = context.scene

        try:
            item = scn.presets_area[self.my_index]
        except IndexError:
            pass

        self.name_input = item.name

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        scn = context.scene

        try:
            item = scn.presets_area[self.my_index]
        except IndexError:
            pass

        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_area) - 1):
                if scn.presets_area[i].name == self.name_input and i != self.my_index:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break
            
            item.name = self.name_input

            # bpy.context.scene.presets_area_save = 1
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")



        return {"FINISHED"}
class PRESETS_OT_Area_Change_unit(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_area.change_unit"
    bl_label = "Change unit"
    bl_description = "Rename item"
    bl_options = {'INTERNAL'}

    name_input: StringProperty()
    my_index: IntProperty()

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):

        scn = context.scene

        try:
            item = scn.presets_area[self.my_index]
        except IndexError:
            pass

        self.name_input = item.name

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        scn = context.scene

        try:
            item = scn.presets_area[self.my_index]
        except IndexError:
            pass

        if bpy.context.active_object:

            for i in range(-1, len(scn.presets_area) - 1):
                if scn.presets_area[i].name == self.name_input and i != self.my_index:
                    text = "A preset with this name already exists"
                    war = "WARNING"
                    self.report({war}, text)
                    break
            
            item.name = self.name_input

            # bpy.context.scene.presets_area_save = 1
        else:
            self.report({'INFO'}, "Nothing selected in the Viewport")



        return {"FINISHED"}
class PRESETS_OT_Area_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_area.clear_list"
    bl_label = "Clear List"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.presets_area)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.presets_area):
            context.scene.presets_area.clear()
            self.report({'INFO'}, "All items removed")
            # bpy.context.scene.presets_area_save = 1
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}


# -------------------------------------------------------------------
#   Drawing
# -------------------------------------------------------------------
        
class PRESETS_UL_items_Angle(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        scn = context.scene
        idx = scn.presets_angle_index

        # if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # split = layout.split(factor=0.3)
            # split.label(text="Index: %d" % (index))
            # custom_icon = "OUTLINER_OB_%s" % item.obj_type
            #split.prop(item, "name", text="", emboss=False, translate=False, icon=custom_icon)
        row = layout.row(align = 0)

        # name
        # print("\n")
        # print(1111111111111111111111111111111111111)
        # print(layout)
        # print(data)
        # print(item)
        # print(icon)
        # print(active_data)
        # # self.active_data = item.name
        # # active_propname = item.name
        # print(active_propname)
        # print(111111111111111111111111111111111111111)

        row.scale_y = 1.1

        row.operator("presets_angle.list_action_refresh", text = item.name, emboss = 0, depress=0).my_index = index
        # row.prop(item, "name", emboss=False, text = "")
        row.prop(item, "unit", emboss=0, text = "", expand = 1)

        row.operator("presets_angle.list_action_import", text = "", icon = "IMPORT", emboss = 0).my_index = index
        row.operator("presets_angle.rename", text = "", icon = "SORTALPHA", emboss = 0).my_index = index

        # template_input_status()

    # def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
    #     scn = context.scene
    #     idx = scn.presets_angle_index

        # if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # split = layout.split(factor=0.3)
            # split.label(text="Index: %d" % (index))
            # custom_icon = "OUTLINER_OB_%s" % item.obj_type
            #split.prop(item, "name", text="", emboss=False, translate=False, icon=custom_icon)
        # row = layout.row(align = 0)

        # row.scale_y = 1.1
        # row.scale_x = 1.1
        # row.label(text=item.name, icon=custom_icon) # avoids renaming the item by accident
class PRESETS_PT_presets_List_Angle(Panel):
    """Adds a custom panel to the TEXT_EDITOR"""
    
    bl_idname = 'SCENE_PT_presets_angle'
    bl_label = "Angle Presets"
    bl_options = {'DEFAULT_CLOSED'}

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    # bl_context = "mesh_edit"

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object != None\
            and bpy.context.active_object.mode in {'EDIT'}


    def draw_header(self, context):
        layout = self.layout
        layout.label(icon = "DRIVER_ROTATIONAL_DIFFERENCE")

    def draw(self, context):
        if bpy.context.active_object != None:
            if bpy.context.active_object.mode in {'EDIT'}:
            
                layout = self.layout
                scn = bpy.context.scene

                rows = 5
                row = layout.row()
                row.template_list("PRESETS_UL_items_Angle", "", scn, "presets_angle", scn, "presets_angle_index", rows=rows)

                col = row.column(align=True)
                col.scale_x = 1.1
                col.scale_y = 1.2

                # col.operator("presets_angle.list_action", icon='ADD', text="").action = 'ADD'
                col.operator("presets_angle.list_action_add", icon='ADD', text="")
                col.operator("presets_angle.list_action", icon='REMOVE', text="").action = 'REMOVE'
                
                col.separator(factor = 0.4)

                col.operator("presets_angle.list_action", icon='TRIA_UP', text="").action = 'UP'
                col.operator("presets_angle.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

                col.separator(factor = 0.4)
                # row = layout.row()
                # col = row.column(align=True)
                # row = col.row(align=True)
                col.operator("presets_angle.clear_list", icon="TRASH", text = "")
                # row.operator("presets_angle.remove_duplicates", icon="GHOST_ENABLED")


class PRESETS_UL_items_Length(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        scn = context.scene
        idx = scn.presets_length_index

        # if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # split = layout.split(factor=0.3)
            # split.label(text="Index: %d" % (index))
            # custom_icon = "OUTLINER_OB_%s" % item.obj_type
            #split.prop(item, "name", text="", emboss=False, translate=False, icon=custom_icon)
        row = layout.row(align = 0)

        # name
        # print("\n")
        # print(1111111111111111111111111111111111111)
        # print(layout)
        # print(data)
        # print(item)
        # print(icon)
        # print(active_data)
        # # self.active_data = item.name
        # # active_propname = item.name
        # print(active_propname)
        # print(111111111111111111111111111111111111111)

        row.scale_y = 1.1

        row.operator("presets_length.list_action_refresh", text = item.name, emboss = 0, depress=0).my_index = index
        # row.operator("presets_length.change_unit", text = str(item.unit), emboss = 0, depress=0).my_index = index
        # row.prop(item, "name", emboss=False, text = "")
        row.prop(item, "unit", emboss=0, text = "", expand = 0,  icon_only= 1 )
        # row.label(text = str(item.unit) )

        row.operator("presets_length.list_action_import", text = "", icon = "IMPORT", emboss = 0).my_index = index
        row.operator("presets_length.rename", text = "", icon = "SORTALPHA", emboss = 0).my_index = index

        # template_input_status()

    # def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
    #     scn = context.scene
    #     idx = scn.presets_length_index

        # if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # split = layout.split(factor=0.3)
            # split.label(text="Index: %d" % (index))
            # custom_icon = "OUTLINER_OB_%s" % item.obj_type
            #split.prop(item, "name", text="", emboss=False, translate=False, icon=custom_icon)
        # row = layout.row(align = 0)

        # row.scale_y = 1.1
        # row.scale_x = 1.1
        # row.label(text=item.name, icon=custom_icon) # avoids renaming the item by accident
class PRESETS_PT_presets_List_Length(Panel):
    """Adds a custom panel to the TEXT_EDITOR"""
    
    bl_idname = 'SCENE_PT_presets_length'
    bl_label = "Length / Distance Presets"
    bl_options = {'DEFAULT_CLOSED'}

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    # bl_context = "mesh_edit"

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object != None\
            and bpy.context.active_object.mode in {'EDIT'}

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon = "DRIVER_DISTANCE")

    def draw(self, context):

        if bpy.context.active_object != None:
            if bpy.context.active_object.mode in {'EDIT'}:
            
                layout = self.layout
                scn = bpy.context.scene

                rows = 5
                row = layout.row()
                row.template_list("PRESETS_UL_items_Length", "", scn, "presets_length", scn, "presets_length_index", rows=rows)

                col = row.column(align=True)
                col.scale_x = 1.1
                col.scale_y = 1.2

                # col.operator("presets_length.list_action", icon='ADD', text="").action = 'ADD'
                col.operator("presets_length.list_action_add", icon='ADD', text="")
                col.operator("presets_length.list_action", icon='REMOVE', text="").action = 'REMOVE'
                
                col.separator(factor = 0.4)

                col.operator("presets_length.list_action", icon='TRIA_UP', text="").action = 'UP'
                col.operator("presets_length.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

                col.separator(factor = 0.4)
                # row = layout.row()
                # col = row.column(align=True)
                # row = col.row(align=True)
                col.operator("presets_length.clear_list", icon="TRASH", text = "")
                # row.operator("presets_length.remove_duplicates", icon="GHOST_ENABLED")


class PRESETS_UL_items_Area(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        scn = context.scene
        idx = scn.presets_angle_index

        # if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # split = layout.split(factor=0.3)
            # split.label(text="Index: %d" % (index))
            # custom_icon = "OUTLINER_OB_%s" % item.obj_type
            #split.prop(item, "name", text="", emboss=False, translate=False, icon=custom_icon)
        row = layout.row(align = 0)

        # name
        # print("\n")
        # print(1111111111111111111111111111111111111)
        # print(layout)
        # print(data)
        # print(item)
        # print(icon)
        # print(active_data)
        # # self.active_data = item.name
        # # active_propname = item.name
        # print(active_propname)
        # print(111111111111111111111111111111111111111)

        row.scale_y = 1.1

        row.operator("presets_angle.list_action_refresh", text = item.name, emboss = 0, depress=0).my_index = index
        # row.prop(item, "name", emboss=False, text = "")
        row.prop(item, "unit", emboss=0, text = "", expand = 1)

        row.operator("presets_angle.list_action_import", text = "", icon = "IMPORT", emboss = 0).my_index = index
        row.operator("presets_angle.rename", text = "", icon = "SORTALPHA", emboss = 0).my_index = index

        # template_input_status()

    # def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
    #     scn = context.scene
    #     idx = scn.presets_angle_index

        # if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # split = layout.split(factor=0.3)
            # split.label(text="Index: %d" % (index))
            # custom_icon = "OUTLINER_OB_%s" % item.obj_type
            #split.prop(item, "name", text="", emboss=False, translate=False, icon=custom_icon)
        # row = layout.row(align = 0)

        # row.scale_y = 1.1
        # row.scale_x = 1.1
        # row.label(text=item.name, icon=custom_icon) # avoids renaming the item by accident
class PRESETS_PT_presets_List_Area(Panel):
    """Adds a custom panel to the TEXT_EDITOR"""
    
    bl_idname = 'SCENE_PT_presets_angle'
    bl_label = "Angle Presets"
    bl_options = {'DEFAULT_CLOSED'}

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    # bl_context = "mesh_edit"

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object != None\
            and bpy.context.active_object.mode in {'EDIT'}


    def draw_header(self, context):
        layout = self.layout
        layout.label(icon = "DRIVER_ROTATIONAL_DIFFERENCE")

    def draw(self, context):
        if bpy.context.active_object != None:
            if bpy.context.active_object.mode in {'EDIT'}:
            
                layout = self.layout
                scn = bpy.context.scene

                rows = 5
                row = layout.row()
                row.template_list("PRESETS_UL_items_Angle", "", scn, "presets_angle", scn, "presets_angle_index", rows=rows)

                col = row.column(align=True)
                col.scale_x = 1.1
                col.scale_y = 1.2

                # col.operator("presets_angle.list_action", icon='ADD', text="").action = 'ADD'
                col.operator("presets_angle.list_action_add", icon='ADD', text="")
                col.operator("presets_angle.list_action", icon='REMOVE', text="").action = 'REMOVE'
                
                col.separator(factor = 0.4)

                col.operator("presets_angle.list_action", icon='TRIA_UP', text="").action = 'UP'
                col.operator("presets_angle.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

                col.separator(factor = 0.4)
                # row = layout.row()
                # col = row.column(align=True)
                # row = col.row(align=True)
                col.operator("presets_angle.clear_list", icon="TRASH", text = "")
                # row.operator("presets_angle.remove_duplicates", icon="GHOST_ENABLED")




class PRESETS_presets_length_Collection(PropertyGroup):

    unit: FloatProperty(
        name="Length",
        description="Length of the edge",
        step = 100.0,
        unit='LENGTH',
        precision = 6,)
    name: StringProperty()
class PRESETS_presets_angle_Collection(PropertyGroup):

    unit: FloatProperty(
        name="Angle",
        description="Angle",
        min=-360.0, max=360.0,
        default=0.0,
        step = 100.0,
        unit="ROTATION",
        precision = 6,)
    name: StringProperty()


    # remember_index = IntProperty()
    # obj_type: StringProperty()
    # obj_id: IntProperty()
class PRESETS_presets_area_Collection(PropertyGroup):

    unit: FloatProperty(
        name="area",
        description="area of the edge",
        step = 100.0,
        unit='LENGTH',
        precision = 6,)
    name: StringProperty()



PRESET_SUBDIR = "Length"
class PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets(Menu):
    bl_label = "Preset"
    preset_subdir = PRESET_SUBDIR
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset
class PRESETS_FOR_PRESETS_LENGTH_OT_AddPreset(AddPresetBase, Operator):
    bl_idname = "scene.presets_for_presets_length_add"
    bl_label = ""
    preset_menu = "PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets"
    bl_description = "Add or remove preset"

    @classmethod
    def description(cls, context, properties):
        if properties.remove_active == False:
            return "Add Preset"
        elif properties.remove_active == True:
            return "Delete Preset"
        else:
            pass

    preset_defines = ["scene = bpy.context.scene"]

    preset_values = [
        "scene.presets_length",
        "scene.presets_length_index",
    ]

    preset_subdir = PRESET_SUBDIR
class PRESETS_FOR_PRESETS_LENGTH_OT_Rename(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_for_presets_length.rename"
    bl_label = "Rename"
    bl_description = "Rename item"
    # bl_options = {'UNDO'}

    name_input: StringProperty()

    # def draw(self, context):
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):

        self.name_input = bpy.types.PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets.bl_label

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)


    def execute(self, context):

        # bpy.ops.scene.presets_for_presets_add(name=self.name_input, remove_name=1, remove_active=0)
        bpy.types.PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets.bl_label = self.name_input
        # bpy.ops.eeveepresets.preset_add(name=self.name_input, remove_name=0, remove_active=False)

        return {"FINISHED"}
class PRESETS_FOR_PRESETS_LENGTH_OT_Refresh(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_for_presets_length.refresh"
    bl_label = "Save"
    bl_description = "Overwrite item"
    # bl_options = {'UNDO'}

    name_input: StringProperty()

    # def draw(self, context):
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):
        self.name_input =  bpy.types.PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets.bl_label

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        bpy.ops.scene.presets_for_presets_length_add(name=self.name_input, remove_name=0, remove_active=1)
        bpy.ops.scene.presets_for_presets_length_add(name=self.name_input, remove_name=0, remove_active=False)

        # bpy.context.scene.presets_length_save = 0

        return {"FINISHED"}



PRESET_SUBDIR = "Angle"
class PRESETS_FOR_PRESETS_ANGLE_MT_DisplayPresets(Menu):
    bl_label = "Preset"
    preset_subdir = PRESET_SUBDIR
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset
class PRESETS_FOR_PRESETS_ANGLE_OT_AddPreset(AddPresetBase, Operator):
    bl_idname = "scene.presets_for_presets_add"
    bl_label = ""
    preset_menu = "PRESETS_FOR_PRESETS_ANGLE_MT_DisplayPresets"
    bl_description = "Add or remove preset"

    @classmethod
    def description(cls, context, properties):
        if properties.remove_active == False:
            return "Add Preset"
        elif properties.remove_active == True:
            return "Delete Preset"
        else:
            pass


    preset_defines = ["scene = bpy.context.scene"]

    preset_values = [
        "scene.presets_angle",
        "scene.presets_angle_index",
    ]

    preset_subdir = PRESET_SUBDIR
class PRESETS_FOR_PRESETS_ANGLE_OT_Rename(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_for_presets.rename"
    bl_label = "Rename"
    bl_description = "Rename item"
    # bl_options = {'UNDO'}

    name_input: StringProperty()

    # def draw(self, context):
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):

        self.name_input = bpy.types.PRESETS_FOR_PRESETS_ANGLE_MT_DisplayPresets.bl_label

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)


    def execute(self, context):

        # bpy.ops.scene.presets_for_presets_add(name=self.name_input, remove_name=1, remove_active=0)
        bpy.types.PRESETS_FOR_PRESETS_ANGLE_MT_DisplayPresets.bl_label = self.name_input
        # bpy.ops.eeveepresets.preset_add(name=self.name_input, remove_name=0, remove_active=False)

        return {"FINISHED"}
class PRESETS_FOR_PRESETS_ANGLE_OT_Refresh(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_for_presets.refresh"
    bl_label = "Save"
    bl_description = "Overwrite item"
    # bl_options = {'UNDO'}

    name_input: StringProperty()

    # def draw(self, context):
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):
        self.name_input =  bpy.types.PRESETS_FOR_PRESETS_ANGLE_MT_DisplayPresets.bl_label

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        bpy.ops.scene.presets_for_presets_add(name=self.name_input, remove_name=0, remove_active=1)
        bpy.ops.scene.presets_for_presets_add(name=self.name_input, remove_name=0, remove_active=False)

        return {"FINISHED"}


PRESET_SUBDIR = "Area"
class PRESETS_FOR_PRESETS_AREA_MT_DisplayPresets(Menu):
    bl_label = "Preset"
    preset_subdir = PRESET_SUBDIR
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset
class PRESETS_FOR_PRESETS_AREA_OT_AddPreset(AddPresetBase, Operator):
    bl_idname = "scene.presets_for_presets_area_add"
    bl_label = ""
    preset_menu = "PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets"
    bl_description = "Add or remove preset"

    @classmethod
    def description(cls, context, properties):
        if properties.remove_active == False:
            return "Add Preset"
        elif properties.remove_active == True:
            return "Delete Preset"
        else:
            pass

    preset_defines = ["scene = bpy.context.scene"]

    preset_values = [
        "scene.presets_length",
        "scene.presets_length_index",
    ]

    preset_subdir = PRESET_SUBDIR
class PRESETS_FOR_PRESETS_AREA_OT_Rename(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_for_presets_area.rename"
    bl_label = "Rename"
    bl_description = "Rename item"
    # bl_options = {'UNDO'}

    name_input: StringProperty()

    # def draw(self, context):
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):

        self.name_input = bpy.types.PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets.bl_label

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)


    def execute(self, context):

        # bpy.ops.scene.presets_for_presets_add(name=self.name_input, remove_name=1, remove_active=0)
        bpy.types.PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets.bl_label = self.name_input
        # bpy.ops.eeveepresets.preset_add(name=self.name_input, remove_name=0, remove_active=False)

        return {"FINISHED"}
class PRESETS_FOR_PRESETS_AREA_OT_Refresh(Operator):
    """Clear all items of the list"""
    bl_idname = "presets_for_presets_area.refresh"
    bl_label = "Save"
    bl_description = "Overwrite item"
    # bl_options = {'UNDO'}

    name_input: StringProperty()

    # def draw(self, context):
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name_input", text = "Name")

    def invoke(self, context, event):
        self.name_input =  bpy.types.PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets.bl_label

        return context.window_manager.invoke_props_dialog(self)
        # return context.window_manager.invoke_popup(self)
        # return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):

        bpy.ops.scene.presets_for_presets_length_add(name=self.name_input, remove_name=0, remove_active=1)
        bpy.ops.scene.presets_for_presets_length_add(name=self.name_input, remove_name=0, remove_active=False)

        # bpy.context.scene.presets_length_save = 0

        return {"FINISHED"}



class PRESETS_FOR_PRESETS_PT_panel(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_label = "Library Presets (Angle / Length)"
    bl_options = {'DEFAULT_CLOSED'}


    @classmethod
    def poll(cls, context):
        return bpy.context.active_object != None\
            and bpy.context.active_object.mode in {'EDIT'}

    def draw_header(self, context):
        layout = self.layout
        # layout.label(icon = "OUTLINER_OB_GROUP_INSTANCE")
        layout.label(icon = "ASSET_MANAGER")

    def draw(self, context):
        layout = self.layout

        col = layout.column()

        row = col.row(align=True)
        row.scale_y = 1.1
        row.scale_x = 1.35

        sub_row = row.row(align = 1)
        sub_row.alignment = "LEFT"
        sub_row.ui_units_x = 2.4
        sub_row.label(icon = "DRIVER_ROTATIONAL_DIFFERENCE", text = "Angle")


        row.menu(PRESETS_FOR_PRESETS_ANGLE_MT_DisplayPresets.__name__,
                 text=PRESETS_FOR_PRESETS_ANGLE_MT_DisplayPresets.bl_label)

        row.operator(PRESETS_FOR_PRESETS_ANGLE_OT_AddPreset.bl_idname,
                     text="", icon='ADD')

        row.operator(PRESETS_FOR_PRESETS_ANGLE_OT_AddPreset.bl_idname,
                     text="", icon='REMOVE').remove_active = True

        row.operator("presets_for_presets.refresh", icon = "FOLDER_REDIRECT", text = "")

        # row.operator("presets_for_presets.rename", icon = "SORTALPHA")


        col.separator(factor = 0.35)


        row = col.row(align=True)
        row.scale_y = 1.1
        row.scale_x = 1.35

        sub_row = row.row(align = 1)
        sub_row.alignment = "LEFT"
        sub_row.ui_units_x = 2.4
        sub_row.label(icon = "DRIVER_DISTANCE", text = "Length")

        row.menu(PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets.__name__,
                 text=PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets.bl_label)

        row.operator(PRESETS_FOR_PRESETS_LENGTH_OT_AddPreset.bl_idname,
                     text="", icon='ADD')

        row.operator(PRESETS_FOR_PRESETS_LENGTH_OT_AddPreset.bl_idname,
                     text="", icon='REMOVE').remove_active = True

        row.operator("presets_for_presets_length.refresh", icon = "FOLDER_REDIRECT", text = "")

        # if bpy.context.scene.presets_length_save != 0:
        #     row = row.row(align = 1)
        #     row.alignment = "RIGHT"
        #     row.label(icon = "ERROR")

        # row.operator("presets_for_presets_length.rename", icon = "SORTALPHA")

        col.separator(factor = 0.35)


        row = col.row(align=True)
        row.scale_y = 1.1
        row.scale_x = 1.35

        sub_row = row.row(align = 1)
        sub_row.alignment = "LEFT"
        sub_row.ui_units_x = 2.4
        sub_row.label(icon = "FULLSCREEN_ENTER", text = "Area")

        row.menu(PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets.__name__,
                 text=PRESETS_FOR_PRESETS_LENGTH_MT_DisplayPresets.bl_label)

        row.operator(PRESETS_FOR_PRESETS_LENGTH_OT_AddPreset.bl_idname,
                     text="", icon='ADD')

        row.operator(PRESETS_FOR_PRESETS_LENGTH_OT_AddPreset.bl_idname,
                     text="", icon='REMOVE').remove_active = True

        row.operator("presets_for_presets_length.refresh", icon = "FOLDER_REDIRECT", text = "")







# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

# @call_once(bpy.app.handlers.depsgraph_update_pre)
# def my_handler(scene):
#     # print("Frame Change", scene.frame_current)
#     # print("\n")
#     print("Index", bpy.context.scene.presets_length_index)
#     # print(presets_length_index)
#     # print(scene)

#     # print( k + 1)
#     # bpy.ops.presets_length.list_action_refresh()
#     if bpy.context.scene.presets_length_index:
#         scn = bpy.context.scene
#         idx = scn.presets_length_index

#         try:
#             item = scn.presets_length[idx]
#             if bpy.context.active_object:
#                 bpy.context.window_manager.setprecisemesh.length = item.unit
#                 # pass
#         except IndexError:
#             pass
#         except UnboundLocalError:
#             pass

#     # bpy.app.handlers.depsgraph_update_pre.remove(my_handler)


if __name__ == "__main__":
    register()
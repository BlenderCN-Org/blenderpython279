# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# bl_info = {
#    "name": "Rotate Constrained",
#    "author": "Ryan Southall",
#    "version": (0, 0, 1),
#    "blender": (2, 6, 6),
#    "category": "User Changed"}


import bpy
import math
import mathutils


class RotateConstrained(bpy.types.Operator):
    """constraine rotation to keep the face ko-planar"""
    bl_idname = "mesh.rot_con"
    bl_label = "Rotate Constrained"
    bl_options = {'REGISTER', 'UNDO'}

    axis = bpy.props.EnumProperty(
        items=[("0", "X", "Rotate around X-axis"),
               ("1", "Y", "Rotate around Y-axis"),
               ("2", "Z", "Rotate around Z-axis"),
               ],
        name="Rotation Axis",
        description="Specify the axis of rotation",
        default="1")

    caxis = bpy.props.EnumProperty(
        items=[("0", "X", "Constrain to X-axis"),
               ("1", "Y", "Constrain to Y-axis"),
               ("2", "Z", "Constrain to Z-axis"),
               ],
        name="Constraint Normal Axis",
        description="Specify the vertex constraint axis",
        default="2")

    rpoint = bpy.props.EnumProperty(
        items=[("0", "Mid", "Rotate the end face around its midpoint"),
               ("1", "Max", "Rotate the end face around its highpoint"),
               ("2", "Min", "Rotate the end face around its lowpoint"),
               ],
        name="Rotation point",
        description="Specify the point on the end face to rotate around",
        default="0")

    rdeg = bpy.props.FloatProperty(name="Degrees", default=0, min=-120, max=120)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)
        bpy.ops.object.mode_set(mode="OBJECT")
        self.fnorm = [face.normal for face in context.active_object.data.polygons if face.select == True][0]
        (self.fnormx, self.fnormy, self.fnormz) = self.fnorm
        bpy.ops.object.mode_set(mode="EDIT")
        return {'FINISHED'}

    def execute(self, context):
        if self.rdeg != 0 and self.caxis != self.axis:
            bpy.ops.object.mode_set(mode="OBJECT")
            mesh = context.active_object.data
            posaxis = [int(paxis) for paxis in ("0", "1", "2") if paxis not in (self.axis, self.caxis)][0]
            verts = [vert.index for vert in mesh.vertices if vert.select == True]
            vmax = max([v.co[posaxis] for v in bpy.context.active_object.data.vertices if v.index in verts])
            vmin = min([v.co[posaxis] for v in bpy.context.active_object.data.vertices if v.index in verts])
            refpos = ((vmin + vmax) / 2, vmax, vmin)[int(self.rpoint)]
            if context.space_data.transform_orientation == 'NORMAL':
                for v in bpy.context.active_object.data.vertices:
                    if v.index in verts:
                        v.co += (v.co[posaxis] - refpos) * mathutils.Vector((self.fnormx, self.fnormy, self.fnormz)) * math.tan(float(self.rdeg) * 0.0174533)
            else:
                for v in bpy.context.active_object.data.vertices:
                    if v.index in verts:
                        v.co[int(self.caxis)] += (v.co[posaxis] - refpos) * math.tan(float(self.rdeg) * 0.0174533)
            bpy.ops.object.mode_set(mode="EDIT")
        return {'FINISHED'}

# def menu_func(self, context):
#    self.layout.operator("mesh.rot_con")

#addon_keymaps = []


def register():
    bpy.utils.register_class(RotateConstrained)
#    bpy.types.VIEW3D_PT_tools_meshedit.append(menu_func)

    #wm = bpy.context.window_manager
    #km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    #kmi = km.keymap_items.new("mesh.rot_con", 'R', 'PRESS', ctrl=True, shift=True)
    #kmi.properties.rdeg = 0
    # addon_keymaps.append(km)


def unregister():
    bpy.utils.unregister_class(RotateConstrained)
#    bpy.types.VIEW3D_PT_tools_meshedit.remove(menu_func)
    #wm = bpy.context.window_manager
    # for km in addon_keymaps:
    # wm.keyconfigs.addon.keymaps.remove(km)
    #del addon_keymaps[:]


#####  Rotate  Plus  #############

#----X Axis----

class rotateXz(bpy.types.Operator):
    """rotate selected face > Xz 45° """
    bl_label = "Xz 45°"
    bl_idname = "mesh.face_rotate_xz45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='0', caxis='2', rpoint='1', rdeg=45)

        return {"FINISHED"}


class rotateXy(bpy.types.Operator):
    """rotate selected face > Xy 45° """
    bl_label = "Xy 45°"
    bl_idname = "mesh.face_rotate_xy45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='0', caxis='1', rpoint='1', rdeg=45)

        return {"FINISHED"}


#----Y Axis----

class rotateYz(bpy.types.Operator):
    """rotate selected face > Yz 45° """
    bl_label = "Yz 45°"
    bl_idname = "mesh.face_rotate_yz45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='1', caxis='2', rpoint='1', rdeg=45)

        return {"FINISHED"}


class rotateYx(bpy.types.Operator):
    """rotate selected face > Yx 45° """
    bl_label = "Yx 45°"
    bl_idname = "mesh.face_rotate_yx45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='1', caxis='0', rpoint='1', rdeg=45)

        return {"FINISHED"}


#----Z Axis----

class rotateZy(bpy.types.Operator):
    """rotate selected face > Zy 45° """
    bl_label = "Zy 45°"
    bl_idname = "mesh.face_rotate_zy45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='2', caxis='1', rpoint='1', rdeg=45)

        return {"FINISHED"}


class rotateZx(bpy.types.Operator):
    """rotate selected face > Zx 45° """
    bl_label = "Zx 45°"
    bl_idname = "mesh.face_rotate_zx45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='2', caxis='0', rpoint='1', rdeg=45)

        return {"FINISHED"}


#####  Rotate  Minus  #############

#----X Axis----

class rotatemXz(bpy.types.Operator):
    """rotate selected face > Xz -45° """
    bl_label = "Xz 45°"
    bl_idname = "mesh.face_rotate_mxz45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='0', caxis='2', rpoint='1', rdeg=-45)

        return {"FINISHED"}


class rotatemXy(bpy.types.Operator):
    """rotate selected face > Xy -45° """
    bl_label = "Xy 45°"
    bl_idname = "mesh.face_rotate_mxy45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='0', caxis='1', rpoint='1', rdeg=-45)

        return {"FINISHED"}


#----Y Axis----

class rotatemYz(bpy.types.Operator):
    """rotate selected face > Yz -45° """
    bl_label = "Yz 45°"
    bl_idname = "mesh.face_rotate_myz45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='1', caxis='2', rpoint='1', rdeg=-45)

        return {"FINISHED"}


class rotatemYx(bpy.types.Operator):
    """rotate selected face > Yx -45° """
    bl_label = "Yx 45°"
    bl_idname = "mesh.face_rotate_myx45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='1', caxis='0', rpoint='1', rdeg=-45)

        return {"FINISHED"}


#----Z Axis----

class rotatemZy(bpy.types.Operator):
    """rotate selected face > Zy 45° """
    bl_label = "Zy 45°"
    bl_idname = "mesh.face_rotate_mzy45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='2', caxis='1', rpoint='1', rdeg=-45)

        return {"FINISHED"}


class rotatemZx(bpy.types.Operator):
    """rotate selected face > Zx 45° """
    bl_label = "Zx 45°"
    bl_idname = "mesh.face_rotate_mzx45"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.mesh.rot_con(axis='2', caxis='0', rpoint='1', rdeg=-45)

        return {"FINISHED"}


############  REGISTER  ############

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

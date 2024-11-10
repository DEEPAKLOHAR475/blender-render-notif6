bl_info = {
    "name": "Render Complete Sound",
    "author": "Custom Plugin",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Preferences > Add-ons",
    "description": "Plays a sound when render completes",
    "category": "Render",
}

import bpy
import os
import aud
from bpy.types import (AddonPreferences, Operator)
from bpy.props import StringProperty
from bpy.app.handlers import persistent  # Added this import

class RenderSoundPreferences(AddonPreferences):
    bl_idname = __name__

    sound_file: StringProperty(
        name="Sound File",
        subtype='FILE_PATH',
        default="",
        description="Choose a sound file to play when render completes"
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "sound_file")

def play_sound():
    prefs = bpy.context.preferences.addons[__name__].preferences
    sound_file = prefs.sound_file
    
    if sound_file and os.path.exists(sound_file):
        device = aud.Device()
        sound = aud.Sound(sound_file)
        device.play(sound)

@persistent
def render_complete_handler(scene):
    play_sound()

def register():
    bpy.utils.register_class(RenderSoundPreferences)
    bpy.app.handlers.render_complete.append(render_complete_handler)

def unregister():
    bpy.utils.unregister_class(RenderSoundPreferences)
    bpy.app.handlers.render_complete.remove(render_complete_handler)

if __name__ == "__main__":
    register()
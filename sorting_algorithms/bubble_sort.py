import bpy
import random

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def change_object_color(obj, color=(1, 1, 1, 1)):
    """
    Changes the color of the given object by applying a material with the specified color.

    Parameters:
    obj (bpy.types.Object): The Blender object to change color for.
    color (tuple): RGBA values for the color (Red, Green, Blue, Alpha).
    """
    # Ensure the object has a material; create one if it doesn't
    if not obj.data.materials:
        mat = bpy.data.materials.new(name="Material")
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]

    # Enable nodes for the material and access the Principled BSDF shader
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")

    if bsdf is None:
        bsdf = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")

    # Set the base color of the material
    bsdf.inputs["Base Color"].default_value = color

    # Also set the viewport display color
    mat.diffuse_color = color
    obj.active_material = mat

def get_object_color(obj):
    """
    Retrieves the base color of the given object's material.

    Parameters:
    obj (bpy.types.Object): The Blender object to get the color from.

    Returns:
    tuple: A tuple representing the RGBA color (Red, Green, Blue, Alpha), with each component ranging from 0 to 1.
           Returns None if the object has no material or the material does not use nodes.
    """
    if obj.active_material and obj.active_material.use_nodes:
        bsdf = obj.active_material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Convert the default_value to a tuple to store the color
            color = tuple(bsdf.inputs["Base Color"].default_value)
            return color
    return None

def create_bars(num_elements=20, bar_width=0.5, max_height=5):
    data = [random.randint(1, max_height) for _ in range(num_elements)]
    bars = []
    for i, value in enumerate(data):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i * bar_width * 2, 0, value / 2))
        bar = bpy.context.object
        bar.scale.x = bar_width
        bar.scale.z = value
        color = (random.random(), random.random(), random.random(), 1)
        change_object_color(bar, color)
        bars.append(bar)
    return bars

def bubble_sort_animation(bars, sort_speed):
    global frame_num
    swap_duration = sort_speed
    n = len(bars)
    for i in range(n):
        for j in range(n - i - 1):
            bar1 = bars[j]
            bar2 = bars[j + 1]

            # Check if swap is needed
            if bar1.scale.z > bar2.scale.z:
                bar1.keyframe_insert(data_path="location", frame=frame_num)
                bar2.keyframe_insert(data_path="location", frame=frame_num)

            # Store original colors using get_object_color function
                original_color1 = get_object_color(bar1)
                original_color2 = get_object_color(bar2)

            # Insert keyframes for colors at the current frame
                change_object_color(bar1, original_color1)
                change_object_color(bar2, original_color2)
                bar1.active_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].keyframe_insert(data_path='default_value', frame=frame_num)
                bar2.active_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].keyframe_insert(data_path='default_value', frame=frame_num)

                frame_num+=1
                # Change colors to red for swapping using change_object_color function
                change_object_color(bar1, color=(1, 0, 0, 1))  # Red
                change_object_color(bar2, color=(1, 0, 0, 1))  # Red

                # Insert keyframes for color change at the start of the swap
                bar1.active_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].keyframe_insert(data_path='default_value', frame=frame_num)
                bar2.active_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].keyframe_insert(data_path='default_value', frame=frame_num)
                frame_num+=swap_duration/2
                # Record initial positions
                x1 = bar1.location.x
                x2 = bar2.location.x

                # Swap positions
                bar1.location.x = x2
                bar2.location.x = x1

                # Insert keyframes at the end of the swap
                bar1.keyframe_insert(data_path="location", frame=frame_num)
                bar2.keyframe_insert(data_path="location", frame=frame_num )

                # Revert colors back to original using change_object_color function
                change_object_color(bar1, color=original_color1)
                change_object_color(bar2, color=original_color2)

                # Insert keyframes for color change at the end of the swap
                bar1.active_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].keyframe_insert(data_path='default_value', frame=frame_num )
                bar2.active_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].keyframe_insert(data_path='default_value', frame=frame_num )

                # Swap the bars in the list
                bars[j], bars[j + 1] = bars[j + 1], bars[j]

            # Increment frame_num after each comparison
            frame_num += swap_duration/2

# Main code
num_elements = 20          # Number of elements to sort
bar_width = 0.5            # Width of each bar
max_height = 5             # Max height for bars
sort_speed = 10            # Frames per swap (speed of sorting)
frame_num = 1              # Start frame for the animation

bars = create_bars(num_elements, bar_width, max_height)

# Set initial keyframes for positions and colors
for bar in bars:
    bar.keyframe_insert(data_path="location", frame=frame_num)
    # Insert initial keyframe for color
    bar.active_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].keyframe_insert(data_path='default_value', frame=frame_num)

bubble_sort_animation(bars, sort_speed)

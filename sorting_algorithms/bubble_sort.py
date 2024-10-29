import bpy
import random


def change_object_color(obj, color=(1, 1, 1, 1)):
    if len(obj.data.materials) == 0:
        mat = bpy.data.materials.new(name="ColorMaterial")
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]

    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")

    if bsdf is None:
        bsdf = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")

    bsdf.inputs["Base Color"].default_value = color

def get_object_color(obj):
    if obj.data.materials:
        mat = obj.data.materials[0]
        if mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                color = bsdf.inputs["Base Color"].default_value
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
        change_object_color(bar, (random.random(), random.random(), random.random(), 1))
        bars.append(bar)
    return bars

def bubble_sort_animation(data, sort_speed):
    global frame_num
    swap_duration = sort_speed  # Duration of each swap animation
    for i in range(len(data)):
        for j in range(len(data) - i - 1):
            # Set keyframes to show comparison (optional)

            # Check if swap is needed
            if data[j].scale.z > data[j + 1].scale.z:
                # Record the current positions
                bar1 = data[j]
                bar2 = data[j + 1]
                x1_initial = bar1.location.x
                x2_initial = bar2.location.x

                # Set keyframes at the start of the swap
                bar1.keyframe_insert(data_path="location", frame=frame_num )
                bar2.keyframe_insert(data_path="location", frame=frame_num )

                # Swap the bars in the list
                data[j], data[j + 1] = data[j + 1], data[j]

                # Set the new positions
                bar1.location.x = x2_initial
                bar2.location.x = x1_initial

                # Insert keyframes at the end of the swap
                frame_num += swap_duration
                bar1.keyframe_insert(data_path="location", frame=frame_num+swap_duration)
                bar2.keyframe_insert(data_path="location", frame=frame_num+swap_duration)
            frame_num += swap_duration/2

# Main code
# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
num_elements = 20          # Number of elements to sort
bar_width = 0.5            # Width of each bar
max_height = 5             # Max height for bars
sort_speed = 10            # Frames per swap (speed of sorting)
frame_num = 1              # Start frame for the animation

bars = create_bars(num_elements, bar_width, max_height)

# Set initial keyframes
for bar in bars:
    bar.keyframe_insert(data_path="location", frame=frame_num)
frame_num += sort_speed
bubble_sort_animation(bars, sort_speed)

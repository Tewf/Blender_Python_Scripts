import bpy
import random

'''import bpy
import random

def change_object_color(obj, color):
    if not obj.data.materials:
        mat = bpy.data.materials.new(name="Material")
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    principled_bsdf = nodes.get("Principled BSDF")
    if principled_bsdf:
        principled_bsdf.inputs["Base Color"].default_value = color

def get_height(obj):
    original_height = 1
    return obj.scale.z * original_height

def create_bars(num_elements=20, bar_width=0.5, max_height=5, data=None):
    if data is None:
        data = [random.randint(1, max_height) for _ in range(num_elements)]
    else:
        num_elements = len(data)

    bars = []
    for i, value in enumerate(data):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i * bar_width * 2, 0, 0))
        bar = bpy.context.object
        bar.scale.x = bar_width
        bar.scale.z = value
        bar.location.z = value / 2  # Position bars on the ground
        change_object_color(bar, (random.random(), random.random(), random.random(), 1))
        bars.append(bar)

    return bars

def move_bars(bars, delta_y):
    for bar in bars:
        bar.location.y += delta_y

def update_location(bar, frame_num):
    bar.keyframe_insert(data_path="location", frame=frame_num)

def update_location_all(bars, frame_num):
    for bar in bars:
        update_location(bar, frame_num)

def get_coordinates(objects):
    return [(obj.location.x, obj.location.y, obj.location.z) for obj in objects]

def merge_sort_animation(arr, start, end, sort_speed):
    global frame_num
    if end - start > 1:
        mid = (start + end) // 2
        # Move only the current sublist bars up
        bars = arr[start:end]
        move_bars(bars, 5)
        update_location_all(bars, frame_num)
        frame_num += sort_speed

        # Recursively sort left and right halves
        merge_sort_animation(arr, start, mid, sort_speed)
        merge_sort_animation(arr, mid, end, sort_speed)

        # Merge the sorted halves
        merge_animation(arr, start, mid, end)

        # Move the merged bars back down
        move_bars(arr[start:end], -5)
        update_location_all(arr[start:end], frame_num)
        frame_num += sort_speed

def merge_animation(arr, start, mid, end):
    global sort_speed
    global frame_num
    left = arr[start:mid]
    right = arr[mid:end]
    i = j = 0
    sorted_bars = []
    # Get x-coordinates for the bars in this range
    coordinates = [bar.location.x for bar in arr[start:end]]

    while i < len(left) and j < len(right):
        if left[i].scale.z <= right[j].scale.z:
            sorted_bars.append(left[i])
            i += 1
        else:
            sorted_bars.append(right[j])
            j += 1

    # Add any remaining bars
    sorted_bars.extend(left[i:])
    sorted_bars.extend(right[j:])

    # Update positions and keyframes
    for idx, bar in enumerate(sorted_bars):
        bar.location.x = coordinates[idx]
        update_location(bar, frame_num)

    # Update the original array with sorted bars
    arr[start:end] = sorted_bars
    frame_num += sort_speed

# Example usage
num_elements = 16           # Number of elements to sort
bar_width = 0.5             # Width of each bar
max_height = 20             # Max height for bars
sort_speed = 10             # Frames per action
frame_num = 1               # Start frame for the animation

# Clear existing objects in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bars = create_bars(num_elements, bar_width, max_height)
update_location_all(bars, frame_num)
frame_num += sort_speed

merge_sort_animation(bars, 0, len(bars), sort_speed)

'''
def change_object_color(obj, color):
    if not obj.data.materials:
        mat = bpy.data.materials.new(name="Material")
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    principled_bsdf = nodes.get("Principled BSDF")
    if principled_bsdf:
        principled_bsdf.inputs["Base Color"].default_value = color

def get_height(obj):
    original_height = 1
    return obj.scale.z * original_height

def create_bars(num_elements=20, bar_width=0.5, max_height=5, sort_speed=10, data=None):
    if data is None:
        data = [random.randint(1, max_height) for _ in range(num_elements)]
    else:
        num_elements = len(data)

    bars = []
    for i, value in enumerate(data):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i * bar_width * 2, 0, 0))
        bar = bpy.context.object
        bar.scale.x = bar_width
        bar.scale.z = value
        change_object_color(bar, (random.random(), random.random(), random.random(), 1))
        bars.append(bar)
    
    return bars

def move_bars(bars, vector):
    for bar in bars:
        bar.location.x += vector[0]
        bar.location.y += vector[1]
        bar.location.z += vector[2]

def update_location(bar, frame_num):
    bar.keyframe_insert(data_path="location", frame=frame_num)

def update_location_all(x, frame_num):
    for i in x:
        update_location(i, frame_num)

def get_coordinates(objects):
    coordinates = []
    for obj in objects:
        coordinates.append((obj.location.x, obj.location.y, obj.location.z))
    return coordinates

def set_mesh_coordinates(mesh, coordinates):
    mesh.location.x, mesh.location.y, mesh.location.z = coordinates

def merge_sort_animation(arr, sort_speed):
    global frame_num
    if len(arr) > 1:
        mid = len(arr) // 2
        coordinates = get_coordinates(arr)
        left_half = arr[:mid]
        right_half = arr[mid:]
        #start
        update_location_all(arr, frame_num)
        move_bars(left_half, (-5, 5, 0))
        move_bars(right_half, (5, 5, 0))
        update_location_all(left_half, frame_num+sort_speed)
        update_location_all(right_half, frame_num+sort_speed)
        frame_num += sort_speed
        #end
        merge_sort_animation(left_half, sort_speed)
        merge_sort_animation(right_half, sort_speed)
        merge_animation(arr, coordinates, left_half, right_half)
        

def merge_animation(arr, coordinates, left_half, right_half):
    global sort_speed
    global frame_num
    i = j = k = 0
    merged = []
    while i < len(left_half) and j < len(right_half):
        if left_half[i].scale.z < right_half[j].scale.z:
            #start
            update_location(left_half[i], frame_num)
            left_half[i].location = coordinates[k]
            update_location(left_half[i], frame_num+sort_speed)
            #end
            merged.append(left_half[i])
            i += 1
        else:
            #start
            update_location(right_half[j], frame_num)
            right_half[j].location = coordinates[k]
            update_location(right_half[j], frame_num+sort_speed)
            #end
            merged.append(right_half[j])
            j += 1
        frame_num += sort_speed
        k += 1

    while i < len(left_half):
        #start
        update_location(left_half[i], frame_num)
        left_half[i].location = coordinates[k]
        merged.append(left_half[i])
        frame_num += sort_speed
        update_location(left_half[i], frame_num)
        #end
        i += 1
        k += 1

    while j < len(right_half):
        #start
        update_location(right_half[j], frame_num)
        right_half[j].location = coordinates[k]
        merged.append(right_half[j])
        frame_num += sort_speed
        update_location(right_half[j], frame_num)
        #end
        j += 1
        k += 1

    arr[:] = merged[:]

# Example usage
# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

num_elements = 16           # Number of elements to sort
bar_width = 0.5             # Width of each bar
max_height = 20             # Max height for bars
sort_speed = 10             # Frames per swap (speed of sorting)
frame_num = 1               # Start frame for the animation

bars = create_bars(num_elements, bar_width, max_height, sort_speed)
update_location_all(bars, frame_num)
frame_num += sort_speed
merge_sort_animation(bars, sort_speed)

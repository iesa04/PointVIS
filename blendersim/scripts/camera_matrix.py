import bpy
import numpy as np
import json
import os

# Replace 'Camera' with the actual name of your camera
camera_name = 'Camera'

# Get the camera object
camera_obj = bpy.data.objects.get(camera_name)
if camera_obj is None or camera_obj.type != 'CAMERA':
    print(f"Error: Camera '{camera_name}' not found or is not a valid camera object.")
else:
    # Get the camera data
    camera_data = camera_obj.data

    # Get the camera properties
    scene = bpy.context.scene
    render = scene.render
    f = camera_data.lens
    sensor_width = camera_data.sensor_width
    sensor_height = camera_data.sensor_height if camera_data.sensor_fit == 'VERTICAL' else sensor_width / render.resolution_x * render.resolution_y
    resolution_x_in_px = render.resolution_x
    resolution_y_in_px = render.resolution_y
    scale = render.resolution_percentage / 100
    resolution_x_in_px = int(scale * resolution_x_in_px)
    resolution_y_in_px = int(scale * resolution_y_in_px)
    
    # Intrinsic matrix
    pixel_aspect_ratio = render.pixel_aspect_x / render.pixel_aspect_y
    s_u = resolution_x_in_px / sensor_width
    s_v = resolution_y_in_px / sensor_height * pixel_aspect_ratio
    alpha_u = f * s_u
    alpha_v = f * s_v
    u_0 = resolution_x_in_px / 2
    v_0 = resolution_y_in_px / 2

    K = np.array([[alpha_u, 0, u_0],
                  [0, alpha_v, v_0],
                  [0, 0, 1]])
    print("Intrinsic Matrix (K):")
    print(K)

    # Extrinsic matrix (world to camera)
    RT = np.linalg.inv(np.array(camera_obj.matrix_world))
    print("Extrinsic Matrix (RT):")
    print(RT)

    # Saving matrices to JSON
    matrix_data = {
        'K': K.tolist(),
        'RT': RT.tolist()
    }
    
    file_path = "C:/Programming/Fourth Semester/PointVIS/PointVIS/assets/output/camera4.csv"
    with open(file_path, 'w') as f:
        json.dump(matrix_data, f)
    print(f"Matrix data saved to {file_path}")

    # To load the matrices back
    with open(file_path, 'r') as f:
        loaded_data = json.load(f)
        K_loaded = np.array(loaded_data['K'])
        RT_loaded = np.array(loaded_data['RT'])

    print("Loaded Intrinsic Matrix (K):")
    print(K_loaded)
    print("Loaded Extrinsic Matrix (RT):")
    print(RT_loaded)

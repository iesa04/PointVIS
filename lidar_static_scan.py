import bpy
import range_scanner
import json
import csv
import datetime
import numpy as np
import math

def get_specific_camera_properties(camera_name):
    
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

        RT = np.array(camera_obj.matrix_world.inverted())
    
        T_blender_to_cv = np.array([[1, 0, 0, 0],
                                    [0, -1, 0, 0],
                                    [0, 0, -1, 0],
                                    [0, 0, 0, 1]])
        RT_cv = T_blender_to_cv @ RT
        print("Extrinsic Matrix (RT):")
        print(RT_cv)

    matrix_data = {
        'K': K.tolist(),
        'RT': RT_cv.tolist()
    }

    render = bpy.context.scene.render
    matrix_data['resolution_x'] = render.resolution_x  
    matrix_data['resolution_y'] = render.resolution_y  

    return matrix_data

def save_camera_properties_to_csv(camera_name, file_path):
    
    matrix_data = get_specific_camera_properties(camera_name)
    
    with open(file_path, 'w') as f:
        json.dump(matrix_data, f)

def my_save_handler(dummy):

    filename = 'assets/room1/1registry'

    def count_lines_csv(filename):
        count = 0
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                count += 1
        return count

    myid = count_lines_csv(filename)

    camera_name = "Camera"
    file_name = f"view{myid}"
    file_path = "C:/Programming/Fourth Semester/PointVIS/PointVIS/assets/room1"

    save_camera_properties_to_csv(camera_name, file_path + f"/camera{myid}.csv")

    range_scanner.ui.user_interface.scan_static(
        bpy.context, 

        scannerObject=bpy.context.scene.objects[camera_name],

        resolutionX=640, fovX=90, resolutionY=480, fovY=60, resolutionPercentage=100,

        reflectivityLower=0.0, distanceLower=0.0, reflectivityUpper=0.0, distanceUpper=99999.9, maxReflectionDepth=10,
        
        enableAnimation=False, frameStart=1, frameEnd=1, frameStep=1, frameRate=1,

        addNoise=True, noiseType='gaussian', mu=0.0, sigma=0.01, noiseAbsoluteOffset=0.02, noiseRelativeOffset=0.02,

        simulateRain=False, rainfallRate=0.0, 

        addMesh=True,

        exportLAS=False, exportHDF=False, exportCSV=True, exportPLY=False, exportSingleFrames=False,
        exportRenderedImage=True, exportSegmentedImage=True, exportPascalVoc=False, exportDepthmap=False, depthMinDistance=0.0, depthMaxDistance=100.0, 
        dataFilePath=file_path, dataFileName=file_name,
        
        debugLines=False, debugOutput=False, outputProgress=True, measureTime=False, singleRay=False, destinationObject=None, targetObject=None
    )

    with open(filename, mode='a', newline='\n') as file:

        data = [[myid, datetime.datetime.now().strftime("%H:%M:%S"), f"view{myid}_frame_1_image_rendered", f"view{myid}_frames_1_to_1.csv", f"view{myid}_frame_1_image_segmented.png", f"camera{myid}.csv"]]

        writer = csv.writer(file)
        writer.writerows(data)


bpy.app.handlers.save_post.clear()

bpy.app.handlers.save_post.append(my_save_handler)

print("Save handler has been registered.")

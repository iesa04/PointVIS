import bpy
import range_scanner
import csv

import csv
import math

def get_specific_camera_properties(camera_name):
    
    camera = bpy.data.objects.get(camera_name)
    
    if camera is None or camera.type != 'CAMERA':
        raise ValueError("No camera found with the name '{}'".format(camera_name))

    cam_data = camera.data
    
    camera_properties = {}
    
    camera_properties['fov'] = math.degrees(cam_data.angle)  
    camera_properties['sensor_width'] = cam_data.sensor_width  
    camera_properties['sensor_height'] = cam_data.sensor_height  
    camera_properties['clip_start'] = cam_data.clip_start  
    camera_properties['clip_end'] = cam_data.clip_end  
    camera_properties['type'] = cam_data.type  
    camera_properties['shift_x'] = cam_data.shift_x  
    camera_properties['shift_y'] = cam_data.shift_y  
    camera_properties['dof_distance'] = cam_data.dof.focus_distance  
    
    camera_properties['location_x'] = camera.location.x  
    camera_properties['location_y'] = camera.location.y  
    camera_properties['location_z'] = camera.location.z  
    camera_properties['rotation_euler_x'] = math.degrees(camera.rotation_euler.x)  
    camera_properties['rotation_euler_y'] = math.degrees(camera.rotation_euler.y)  
    camera_properties['rotation_euler_z'] = math.degrees(camera.rotation_euler.z)  

    render = bpy.context.scene.render
    camera_properties['resolution_x'] = render.resolution_x  
    camera_properties['resolution_y'] = render.resolution_y  

    return camera_properties

def save_camera_properties_to_csv(camera_name, file_path):
    
    camera_properties = get_specific_camera_properties(camera_name)
    
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Property', 'Value'])
        for prop, value in camera_properties.items():
            writer.writerow([prop, value])

camera_name = "Camera"
file_name = "toilet4"
file_path = "C:/Programming/Fourth Semester/PointVIS/PointVIS/assets/output"

save_camera_properties_to_csv(camera_name, file_path + "/camera4.csv")

range_scanner.ui.user_interface.scan_static(
    bpy.context, 

    scannerObject=bpy.context.scene.objects[camera_name],

    resolutionX=640, fovX=90, resolutionY=480, fovY=60, resolutionPercentage=100,

    reflectivityLower=0.0, distanceLower=0.0, reflectivityUpper=0.0, distanceUpper=99999.9, maxReflectionDepth=10,
    
    enableAnimation=False, frameStart=1, frameEnd=1, frameStep=1, frameRate=1,

    addNoise=True, noiseType='gaussian', mu=0.0, sigma=0.01, noiseAbsoluteOffset=0.02, noiseRelativeOffset=0.02,

    simulateRain=False, rainfallRate=0.0, 

    addMesh=False,

    exportLAS=False, exportHDF=False, exportCSV=True, exportPLY=False, exportSingleFrames=False,
    exportRenderedImage=True, exportSegmentedImage=True, exportPascalVoc=False, exportDepthmap=False, depthMinDistance=0.0, depthMaxDistance=100.0, 
    dataFilePath=file_path, dataFileName=file_name,
    
    debugLines=False, debugOutput=False, outputProgress=True, measureTime=False, singleRay=False, destinationObject=None, targetObject=None
)
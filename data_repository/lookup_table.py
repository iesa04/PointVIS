import pandas as pd

csv_file = 'data_repository/lookup_table.csv'

def initialise_lookup_table():
    df = pd.DataFrame(columns=['objectID', 'instanceID', 'class_name', 'x_centroid', 'y_centroid', 'z_centroid', 'AABB', 'OBB' , 'eigenvalues' , 'eigenvectors' , 'volume', 'surface_area' ,'convex_hull_volume', 'convex_hull_surface_area', 'diameter', 'file_path'])
    df.to_csv(csv_file, index=False)
    print("Lookup table initialized.")

def add_row(objectID, instanceID, class_name, x_centroid, y_centroid, z_centroid, file_path, AABB = -1, OBB = -1 , eigenvalues = -1 , eigenvectors = -1 , convex_hull_volume = -1, convex_hull_surface_area = -1, diameter = -1, volume = -1, surface_area=-1):
    df = pd.read_csv(csv_file)
    if df[(df['objectID'] == objectID) & (df['instanceID'] == instanceID)].empty:
        new_row = pd.DataFrame([{
            'objectID': objectID,
            'instanceID': instanceID,
            'class_name': class_name,
            'x_centroid': x_centroid,
            'y_centroid': y_centroid,
            'z_centroid': z_centroid,
            'AABB' : AABB,
            'OBB' : OBB,
            'eigenvalues' : eigenvalues,
            'eigenvectors' : eigenvectors,
            'volume': volume,
            'surface_area': surface_area,
            'convex_hull_volume' : convex_hull_volume,
            'convex_hull_surface_area' : convex_hull_surface_area,
            'diameter' : diameter,
            'file_path': file_path
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(csv_file, index=False)
        print("Row added successfully.")
    else:
        print("Row with given objectID and instanceID already exists.")

def edit_row(objectID, instanceID, class_name, x_centroid, y_centroid, z_centroid, file_path, AABB=-1, OBB=-1, eigenvalues=-1, eigenvectors=-1, convex_hull_volume=-1, convex_hull_surface_area=-1, diameter=-1, volume=-1, surface_area=-1):
    df = pd.read_csv(csv_file)
    index = df[(df['objectID'] == objectID) & (df['instanceID'] == instanceID)].index
    if not index.empty:
        df.loc[index, 'class_name'] = class_name
        df.loc[index, 'x_centroid'] = x_centroid
        df.loc[index, 'y_centroid'] = y_centroid
        df.loc[index, 'z_centroid'] = z_centroid
        df.loc[index, 'AABB'] = AABB
        df.loc[index, 'OBB'] = OBB
        df.loc[index, 'eigenvalues'] = str(eigenvalues)
        df.loc[index, 'eigenvectors'] = str(eigenvectors)
        df.loc[index, 'convex_hull_volume'] = convex_hull_volume
        df.loc[index, 'convex_hull_surface_area'] = convex_hull_surface_area
        df.loc[index, 'diameter'] = str(diameter)
        df.loc[index, 'volume'] = volume
        df.loc[index, 'surface_area'] = surface_area
        df.loc[index, 'file_path'] = file_path

        df.to_csv(csv_file, index=False)
        print("Row updated successfully.")
    else:
        print("Row with given objectID and instanceID not found.")
        
def delete_row(objectID, instanceID):
    df = pd.read_csv(csv_file)
    index = df[(df['objectID'] == objectID) & (df['instanceID'] == instanceID)].index
    if not index.empty:
        df = df.drop(index)
        df.to_csv(csv_file, index=False)
        print("Row deleted successfully.")
    else:
        print("Row with given objectID and instanceID not found.")

import os
import time

def read_table():
    # Check if the file exists and has content
    while not (os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0):
        print("Waiting for the file to be available and have content...")
        time.sleep(1)  # Wait for 1 second before checking again
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    return df

initialise_lookup_table()
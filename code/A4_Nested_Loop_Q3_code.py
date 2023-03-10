# -*- coding: utf-8 -*-
"""
Created On : Sat Nov 20 22:10:42 2021
Last Modified : Thur Nov 25 2021
Course : MSBD5002 
Assignment : Assignment 04 


"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import random


def distance_euclidean(center, point_obj):
    """ Calculate the Euclidean Distance between 2 pair of points"""
    y_dist = math.pow(point_obj[1] - center[1], 2)
    x_dist = math.pow(point_obj[0] - center[0], 2)
    distance = math.sqrt(y_dist + x_dist)
    return distance
    

def sort(input_list):
    """Function to Remove Duplicate Elements in list"""
    sorted_list = []
    for i in input_list:
        if i not in sorted_list:
            sorted_list.append(i)
    return sorted_list
    

def nested_loop(first_array_block, list_of_other_blocks, count_threshold, radius_input):
    """Function to carry out the nested loop algorithm for every Block"""
    list_possible_outliers = [] # Store possible Outliers
    ### This section is to determine the possible Outliers from the First Array Block
    # - Checking each points in the First Array against every other point in the First Array
    for coor1 in first_array_block:
        count_coor1 = 0 # this is to count the number of neighbouring points for the current Center Point (coor1)
        count_iteration = 0 # to track the number of points that were checked
        for coor2 in first_array_block:
            count_iteration += 1
            ### Determine the distance between 2 points (coor1, coor2) 
            distance_coor1_coor2 = distance_euclidean(coor1, coor2) 
            ### If the distance between 2 points is within the Distance Threshold
            # - consider this point to be a neighbouring point
            if distance_coor1_coor2 <= radius_input:
                count_coor1 += 1 # Increment 1 to number of neighbouring points variable
            ### When the number of neighbouring points exceed the threshold (for minimum number of nearby points)
            # - the Point (coor1) is considered not an Outlier and the for loop is ended
            # - Proceed to the next Point (coor1)
            if count_coor1 > count_threshold:
                break
            ### If every point (coor2) has been checked against the current point (coor1)
            # - if the number of neighbouring points is less than the threshold
            # - consider this point (coor1) a possible outlier 
            if count_coor1 <= count_threshold and count_iteration == len(first_array_block):
                list_possible_outliers.append(coor1) # store (coor1) Point into the possible outlier list
                
    ### This section is to determine the possible Outliers (found from previous section) against the other Blocks 
    # - if a point is still considered to be an Outlier 
    # - the coordinates of the Outlier Points are Returned by the Function
    # Variable to output the final list of Points of Outliers Found
    list_possible_final_outliers = []
    for coor1_next in list_possible_outliers:
        ### This section is to check, for every possible Outlier Points from the Previous Section
        # - Compare the distance of the Outlier Points to the other Points in the Other Blocks (Blocks besides the First Array Block)
        # - Determine if the Outlier Point is still an Outlier
        for block in list_of_other_blocks:
            count_coor1_next = 0  # this is to count the number of neighbouring points for the current Center Point (coor1_next)
            count_iteration = 0  # to track the number of points that were checked
            for coor2_next in block:
                count_iteration += 1
                ### Determine the distance between 2 points (coor1_next, coor2_next)
                distance_coor1_coor2_next = distance_euclidean(coor1_next, coor2_next)
                ### If the distance between 2 points is within the Distance Threshold
                # - consider this point to be a neighbouring point
                if distance_coor1_coor2_next <= radius_input:
                    count_coor1_next += 1 # Increment 1 to number of neighbouring points variable
                ### When the number of neighbouring points exceed the threshold (for minimum number of nearby points)
                # - The current point is not an outlier (coor1_next) 
                # - Proceed to the next Point (coor1_next)
                if count_coor1_next > count_threshold:
                    break
                ### If every point (coor2_next) has been checked against the current point (coor1_next)
                # - if the number of neighbouring points is less than the threshold
                # - consider this point (coor1_next) an Outlier
                if count_coor1_next <= count_threshold and count_iteration == len(block):
                    list_possible_final_outliers.append(coor1_next)
        list_possible_final_outliers = sort(list_possible_final_outliers) # Remove any duplicate elements

    return list_possible_final_outliers



### Data Processing
# Extract the dataset from txt file
dataset_df = pd.read_csv("Nested_Points.txt" , sep="\n", header=None)
dataset_list = dataset_df[0].tolist()
dataset_str_list = [ x.split(" ") for x in dataset_list]
dataset_float_list = []
# Convert the string data into float data
for coordinate in dataset_str_list:
    dataset_float_list.append([float(coordinate[0]), float(coordinate[1])])

# Remove duplicate points
dataset_list = []
for coordinate in dataset_float_list:
    if coordinate not in dataset_list:
        dataset_list.append(coordinate)






### Partition the Dataset into Blocks
split_blocks = np.array_split(dataset_list,4)
coordinate_A = [ list(x) for x in split_blocks[0]]
coordinate_B = [ list(x) for x in split_blocks[1]]
coordinate_C = [ list(x) for x in split_blocks[2]]
coordinate_D = [ list(x) for x in split_blocks[3]]
starting_block_list = [coordinate_A, coordinate_B, coordinate_C, coordinate_D]

### For tracking the Block's 
block_label_tracker_first_array = [] 
block_label_tracker_second_array = []

### Set the Parameters and Threshold
stages = 4 # Fixed
num_points_threshold = 3 # <==
distance_threshold = 20 # <==
all_outlier_list = [] # Records all the Outlier Points determined from each Stage

### Start the Nested Loop Algorithm Outlier Detection
for stage in range(1,stages+1):
    if stage == 1:
        ### Block A
        all_outlier_list += nested_loop(coordinate_A, [coordinate_B, coordinate_C, coordinate_D], num_points_threshold, distance_threshold)

    if stage == 2:
        ### Block D
        all_outlier_list += nested_loop(coordinate_D, [coordinate_B, coordinate_C], num_points_threshold, distance_threshold)
        
    if stage == 3:
        ### Block C
        all_outlier_list += nested_loop(coordinate_C, [coordinate_A, coordinate_B], num_points_threshold, distance_threshold)

    if stage == 4: 
        ### Block B
        all_outlier_list += nested_loop(coordinate_B, [coordinate_D, coordinate_A], num_points_threshold, distance_threshold)



### Plot the Cluster (Set of Non Outliers) in blue and the Outliers in red
dataset_y = [ x[1] for x in dataset_list]
dataset_x = [ x[0] for x in dataset_list]
plt.plot(dataset_x, dataset_y, '.')
dataset_y = [ x[1] for x in all_outlier_list]
dataset_x = [ x[0] for x in all_outlier_list]
plt.plot(dataset_x, dataset_y,  'x', color='r', markersize=15)
plt.xticks(list(range(0,110,10)))
plt.yticks(list(range(0,110,10)))
plt.show()

### Print the Coordinates of the Outliers that were found 
print("""
      Parameter Settings:
          Minimum Number of Points Threshold : {}
          Distance Threshold : {}
          Number of Outliers Found : {}
          
      The Coordinates of the Outliers are:
      """.format(num_points_threshold, distance_threshold, len(all_outlier_list)))
for points in all_outlier_list:
    print("\t\t {}".format(points))



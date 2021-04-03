#!/usr/bin/env python3
import numpy as np
import math
import csv
from Vicon.Mocap import Vicon
from GaitCore.Core import Point
from GaitCore.Core.PointArray import PointArray
from Vicon.Tools.AnimateModel import AnimateModel

import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = Vicon.Vicon("TestData/mechanical_knee_trial01.csv", interpolate=False)

    marker_poses = data.data_dict.get('Trajectories')

    main_markers = {}

    main_markers['thigh'] = data.data_dict.get('Trajectories').get('thigh1')
    main_markers['shank'] = data.data_dict.get('Trajectories').get('shank3')
    main_markers['center'] = data.data_dict.get('Trajectories').get('thigh5')

    points_list = []

    points_list.append(PointArray(main_markers.get('thigh').get('X').get('data'),
                                  main_markers.get('thigh').get('Y').get('data'),
                                  main_markers.get('thigh').get('Z').get('data')).toPointList())
    
    points_list.append(PointArray(main_markers.get('center').get('X').get('data'),
                                  main_markers.get('center').get('Y').get('data'),
                                  main_markers.get('center').get('Z').get('data')).toPointList())

    points_list.append(PointArray(main_markers.get('shank').get('X').get('data'),
                                  main_markers.get('shank').get('Y').get('data'),
                                  main_markers.get('shank').get('Z').get('data')).toPointList())

    points_list = np.transpose(points_list).tolist()

    # ----- Determine flexion/extension ----- #
    flexion = []
    extension = []

    # thigh1 -> thigh5 = a
    # thigh5 -> shank4 = b
    # shank4 -> thigh1 = c

    for points in points_list:
        a = math.sqrt((points[0].x - points[1].x)**2 + (points[0].y - points[1].y)**2)
        b = math.sqrt((points[1].x - points[2].x)**2 + (points[1].y - points[2].y)**2)
        c = math.sqrt((points[2].x - points[0].x)**2 + (points[2].y - points[0].y)**2)

        flexion.append(math.degrees(math.acos((c**2 - b**2 - a**2)/(-2.0 * a * b))))

        extension.append(a + b)
    
    # ----- Normalize Data and remove outliers ----- #
    flexion[:] = [max(flexion) - p for p in flexion]
    extension[:] = [e - min(extension) for e in extension]
    
    list_final = []
    for i in range(len(extension)):
        if extension[i] < 50:
            list_final.append([extension[i], flexion[i]])

    # ----- Plot flexion/extension ----- #
    fig, ax = plt.subplots()

    ax.set(title = "Knee Joint Flexion vs Extension")
    ax.set_xlabel("Flexion $\\theta$ [deg]")
    ax.set_ylabel("Extension r [mm]")

    theta = np.array(range(100))
    r = 1.0003 * pow(10, -7) * pow(theta, 4) - 5.9461 * pow(10, -5) * pow(theta, 3) + 0.0081 * pow(theta, 2) - 0.0144 * theta

    ax.plot(theta, r, color = "red", label="Goal Trajectory")

    plot = ax.scatter(x = [l[1] for l in list_final], y = [l[0] for l in list_final],
                     marker='o', color="black", s=0.2, zorder=1, label="Actual Joint Trajectory")

    plt.legend()
    
    plt.show()
    # ----- 3D Animation of points ----- #
    if False:
        animation = AnimateModel(x_limit=(-200, 200), y_limit=(-50, 350), z_limit=(100, 200))
        animation.import_markers(marker_poses)
        animation.draw()

    # ----- Save Data as CSV ----- #
    with open('test_data.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(list_final)

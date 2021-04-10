#!/usr/bin/env python3
from Vicon.Mocap import Vicon

from GaitCore.Core.PointArray import PointArray
from GaitCore.Core import Point

from Vicon.Tools.AnimateModel import AnimateModel

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D as plot3d
import matplotlib.animation as animation


if __name__ == '__main__':
    data = Vicon.Vicon("TestData/KneePreTrial_Nathaniel1.csv", interpolate=False)

    # data = Vicon.Vicon("TestData/testdata.csv")

    # thigh_data = data.data_dict.get('Segments').get('thigh')
    # shank_data = data.data_dict.get('Segments').get('shank')

    flexion = data._joint_objs.get('Thigh_Shank').angle.rz 
    flexion[:] = [(angle - 48)*-1 for angle in flexion] # Normalize angles

    score_obj = data._joint_objs.get('Thigh_Shank').score
    sara_obj = data._joint_objs.get('Thigh_Shank').sara

    # Calculate distance
    extension_list = []
    extension_list_score = []

    test_thigh     = PointArray(data.data_dict.get('Trajectories').get('Thigh4').get('X').get('data'),
                                data.data_dict.get('Trajectories').get('Thigh4').get('Y').get('data'),
                                data.data_dict.get('Trajectories').get('Thigh4').get('Z').get('data'))
    
    test_shank     = PointArray(data.data_dict.get('Trajectories').get('Shank2').get('X').get('data'),
                                data.data_dict.get('Trajectories').get('Shank2').get('Y').get('data'),
                                data.data_dict.get('Trajectories').get('Shank2').get('Z').get('data'))

    # thigh_pt_array = PointArray(thigh_data.get('TX').get('data'),
    #                             thigh_data.get('TY').get('data'),
    #                             thigh_data.get('TZ').get('data'))

    # shank_pt_array = PointArray(shank_data.get('TX').get('data'),
    #                             shank_data.get('TY').get('data'),
    #                             shank_data.get('TZ').get('data'))
    
    sara_pt_array  = PointArray(sara_obj.x_array,
                                sara_obj.y_array,
                                sara_obj.z_array)
    
    score_pt_array = PointArray(score_obj.x_array,
                                score_obj.y_array,
                                score_obj.z_array)


    # find length from thigh to joint center, joint center to shank
    for (thigh, shank, sara, score) in zip(test_thigh, test_shank, sara_pt_array, score_pt_array):
        extension_list.append(Point.distance(thigh, sara) + Point.distance(sara, shank))
        extension_list_score.append(Point.distance(thigh, score) + Point.distance(score, shank))

    # ----- 3D Animation of points ---- #
    # animation = AnimateModel(x_limit=(-500, 500), y_limit=(-500, 500), z_limit=(0, 500))
    # animation.import_markers(data.data_dict.get('Trajectories'))
    # animation.import_joint( joint_name = "knee",
    #                         parent_joint_segment = test_thigh,
    #                         child_joint_segment = test_shank,
    #                         joint_center = score_pt_array)
    # animation.import_sara({'SARA': sara_obj})
    # animation.import_score({'SCoRE': score_obj})
    # animation.draw()

    # ----- Plot of Joint Centers + 
    # side_plot = z_fig.add_subplot(121)
    # side_plot2 = z_fig.add_subplot(122)
    # side_plot.scatter(thigh_pt_array.x, flexion)
    # side_plot2.scatter(shank_pt_array.x, flexion)

    main_fig = plot.figure()

    # ----- Plot Extension vs Flexion ----- #
    plot1 = main_fig.add_subplot(111) # 1 Row 1 column 1st position
    plot1.plot(flexion, extension_list_score)
    plot1.set_xlabel("Flexion (deg)")
    plot1.set_ylabel("Extension (mm)")
    plot1.set_title("Knee Flexion vs Extension Patterns")
    plot.show()

  
    print("Done!")

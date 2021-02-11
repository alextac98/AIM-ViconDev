from Vicon.Mocap import Vicon

from GaitCore.Core.PointArray import PointArray
from GaitCore.Core import Point

from Vicon.Tools.AnimateModel import AnimateModel

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D as plot3d
import matplotlib.animation as animation


if __name__ == '__main__':
    data = Vicon.Vicon("TestData/ExoKneeRange_Test1.csv", interpolate=False)

    # data = Vicon.Vicon("TestData/testdata.csv")

    thigh_data = data.data_dict.get('Segments').get('thigh')
    shank_data = data.data_dict.get('Segments').get('shank')

    flexion = data._joint_objs.get('thigh_shank').angle.rz 
    flexion[:] = [(angle - 48)*-1 for angle in flexion] # Normalize angles

    score_obj = data._joint_objs.get('thigh_shank').score
    sara_obj = data._joint_objs.get('thigh_shank').sara

    # Calculate distance
    extension_list = []
    extension_list_score = []

    thigh_pt_array = PointArray(thigh_data.get('TX').get('data'),
                                thigh_data.get('TY').get('data'),
                                thigh_data.get('TZ').get('data'))

    shank_pt_array = PointArray(shank_data.get('TX').get('data'),
                                shank_data.get('TY').get('data'),
                                shank_data.get('TZ').get('data'))
    
    sara_pt_array  = PointArray(sara_obj.x_array,
                                sara_obj.y_array,
                                sara_obj.z_array)
    
    score_pt_array = PointArray(score_obj.x_array,
                                score_obj.y_array,
                                score_obj.z_array)


    # find length from thigh to joint center, joint center to shank
    for (thigh, shank, sara, score) in zip(thigh_pt_array, shank_pt_array, sara_pt_array, score_pt_array):
        extension_list.append(Point.distance(thigh, sara) + Point.distance(sara, shank))
        extension_list_score.append(Point.distance(thigh, score) + Point.distance(score, shank))

    # ----- Plot of Joint Centers + 
    # side_plot = z_fig.add_subplot(121)
    # side_plot2 = z_fig.add_subplot(122)
    # side_plot.scatter(thigh_pt_array.x, flexion)
    # side_plot2.scatter(shank_pt_array.x, flexion)

    # main_fig = plot.figure()

    # plot1 = main_fig.add_subplot(111) # 1 Row 1 column 1st position
    # plot1.plot(flexion, extension_list_score)
    # plot1.set_xlabel("Flexion")
    # plot1.set_ylabel("Extension")
    # plot.show()

    # ----- 3D Animation of points ---- #
    animation = AnimateModel(x_limit=(-500, 500), y_limit=(-500, 500), z_limit=(0, 500))
    animation.import_markers(data.data_dict.get('Trajectories'))
    animation.import_sara({'SARA': sara_obj})
    animation.import_score({'SCoRE': score_obj})
    animation.draw()

  
    print("Done!")

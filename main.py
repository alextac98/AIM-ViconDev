from Vicon.Mocap import Vicon

from GaitCore.Core.PointArray import PointArray
from GaitCore.Core import Point

# from Vicon.Tools.AnimateModel import AnimateModel

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D as plot3d
import matplotlib.animation as animation

def make_model_animation(   thigh_list: list, 
                            joint_cntr_list: list, 
                            shank_list: list):
    # Set up figure
    fig = plot.figure()
    fig.canvas.set_window_title('Leg Model Animation')
    ax = fig.add_subplot(111, aspect='equal', projection='3d')
    ax.grid()

    ax.set_title('Leg Animation')
    line, = ax.plot([], [], 'o-', lw=5, color='#de2d26')

    # def init():
    #     line.set_data([], [])
    #     return line,
    
    # def animate(i):
    #     shank_point = 


if __name__ == '__main__':
    data = Vicon.Vicon("TestData/ExoKneeRange_Test1.csv", interpolate=False)

    # data = Vicon.Vicon("TestData/testdata.csv")

    thigh_data = data.data_dict.get('Segments').get('thigh')
    shank_data = data.data_dict.get('Segments').get('shank')

    flexion = data._joint_objs.get('thigh_shank').angle.rz 
    flexion[:] = [(angle - 48)*-1 for angle in flexion] # Normalize angles

    score = data._joint_objs.get('thigh_shank').score
    sara = data._joint_objs.get('thigh_shank').sara

    # Calculate distance
    extension_list = []
    extension_list_score = []

    thigh_pt_array = PointArray(thigh_data.get('TX').get('data'),
                                thigh_data.get('TY').get('data'),
                                thigh_data.get('TZ').get('data'))

    shank_pt_array = PointArray(shank_data.get('TX').get('data'),
                                shank_data.get('TY').get('data'),
                                shank_data.get('TZ').get('data'))
    
    sara_pt_array  = PointArray(sara.x_array,
                                sara.y_array,
                                sara.z_array)
    
    score_pt_array = PointArray(score.x_array,
                                score.y_array,
                                score.z_array)


    # find length from thigh to joint center, joint center to shank
    for (thigh, shank, sara, score) in zip(thigh_pt_array, shank_pt_array, sara_pt_array, score_pt_array):
        extension_list.append(Point.distance(thigh, sara) + Point.distance(sara, shank))
        extension_list_score.append(Point.distance(thigh, score) + Point.distance(score, shank))
    
    # animation = AnimateModel()
    # animation.import_markers(data.data_dict.get('Trajectories'))

    data.markers.play()

    # z_fig = plot.figure()

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


  
    print("Done!")

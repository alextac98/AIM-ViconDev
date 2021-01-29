from Vicon.Mocap import Vicon

if __name__ == '__main__':
    data = Vicon.Vicon("TestData/ExoKneeRange_Test1.csv", interpolate=False)

    # data = Vicon.Vicon("TestData/testdata.csv")

    data.markers.rigid_body

    print("Done!")

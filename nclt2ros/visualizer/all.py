import matplotlib.pyplot as plt
from nclt2ros.visualizer.plotter import Plotter
from nclt2ros.visualizer.gt import GroundTruth
from nclt2ros.visualizer.gps_rtk import GPS_RTK
from nclt2ros.visualizer.gps import GPS
from nclt2ros.visualizer.wheel_odom import WheelOdom


class AllSensors(Plotter, GroundTruth, GPS_RTK, GPS, WheelOdom):
    """Class to visualize all sensor data in one plot

    USAGE:
            AllSensors('2013-01-10', plt_show=True)

    """
    def __init__(self, date, plt_show=True):

        self.date = date

        # init base classes
        Plotter.__init__(self, date=self.date)
        GroundTruth.__init__(self, date=self.date)
        GPS_RTK.__init__(self, date=self.date)
        GPS.__init__(self, date=self.date)
        WheelOdom.__init__(self, date=self.date)

        self.plt_show = plt_show

    def plot(self):
        """visualize all data in one plot
        """

        gt_x, gt_y = self.get_gt_data()
        gps_rtk_x, gps_rtk_y = self.get_gps_rtk_data()
        gps_x, gps_y = self.get_gps_data()
        wheel_odom_x, wheel_odom_y = self.get_wheel_odom_data()
        print(self.plt_show)
        gt = plt.plot(gt_y, gt_x, color="lime", label='ground truth')                # swap x,y coordinate axes!
        gps_rtk = plt.plot(gps_rtk_y, gps_rtk_x, 'r-', label='gps rtk')              # swap x,y coordinate axes!
        gps = plt.plot(gps_y, gps_x, 'y-', label='gps')                              # swap x,y coordinate axes!
        wheel_odom = plt.plot(wheel_odom_y, wheel_odom_x, 'm-', label='wheel odom')  # swap x,y coordinate axes!

        plt.title('All Sensors')
        plt.xlabel('x in meter')
        plt.ylabel('y in meter')
        plt.legend(loc='upper left')

        plt.grid()
        plt.savefig(self.visualization_png_all_dir + 'raw_data_all.png')

        if self.plt_show:
            plt.show()

    def get_png_all_dir(self):
        """get the png all sensors directory

        :return: path to png all sensors directory
        """
        return self.visualization_png_all_dir


if __name__ == '__main__':
    all =AllSensors('2012-01-15', plt_show=False)
    all.plot()

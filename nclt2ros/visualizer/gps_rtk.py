import math
import numpy as np
import matplotlib.pyplot as plt

from nclt2ros.visualizer.plotter import Plotter
from nclt2ros.transformer.coordinate_frame import CoordinateFrame


class GPS_RTK(Plotter):
    """Class to visualize the GPS RTK data as a kml and png file

    USAGE:
            GPS_RTK(date='2013-01-10', output_file='gps_rtk', plt_show=True)

    """
    def __init__(self, date, output_file='gps_rtk', plt_show=True):

        if isinstance(output_file, str):
            self.output_file = output_file
        else:
            raise TypeError("'output_file' must be type of string")

        self.date = date
        self.plt_show = plt_show

        # init base class
        Plotter.__init__(self, date=self.date)

        # transform coordinate frame into 'odom' or 'gt'
        if self.date == '2013-01-10':
            self.gps_rtk_converter = CoordinateFrame(origin='odom')
        else:
            self.gps_rtk_converter = CoordinateFrame(origin='gt')

        # load data
        self.gps_rtk = self.reader.read_gps_rtk_csv(all_in_one=True)

    def save_kml_line(self):
        """visualize the gps rtk data as a kml file
        """

        lat = self.gps_rtk[:, 3]
        lng = self.gps_rtk[:, 4]
        gps_rtk_list = list()

        for (i_lat, j_lng) in zip(lat, lng):

            if not math.isnan(i_lat) and not math.isnan(j_lng):
                tup = (np.rad2deg(j_lng), np.rad2deg(i_lat))  # swap and convert lat long to deg
                gps_rtk_list.append(tup)

        ls = self.kml.newlinestring(name="gps rtk", coords=gps_rtk_list, description="latitude and longitude from gps rtk")
        ls.style.linestyle.width = 1
        ls.style.linestyle.color = self.red

        self.kml.save(self.visualization_kml_dir + self.output_file + '.kml')

    def get_gps_rtk_data(self):
        """get gps rtk data for visualization

        :return: list for x coordinates, list for y coordinates
        """
        lat = self.gps_rtk[:, 3]
        lng = self.gps_rtk[:, 4]
        x_list = list()
        y_list = list()

        for (i_lat, j_lng) in zip(lat, lng):

            if not math.isnan(i_lat) and not math.isnan(j_lng):
                x = self.gps_rtk_converter.get_x(lat=np.rad2deg(i_lat))
                y = self.gps_rtk_converter.get_y(lon=np.rad2deg(j_lng))
                x_list.append(x)
                y_list.append(y)

        return x_list, y_list

    def save_gps_rtk_png(self):
        """visualize the gps rtk data as a png file

        """

        x_list, y_list = self.get_gps_rtk_data()

        plt.plot(y_list, x_list, 'r-', label='gps rtk')
        plt.title('GPS RTK')
        plt.xlabel('x in meter')
        plt.ylabel('y in meter')
        plt.legend(loc='upper left')

        plt.grid()
        plt.savefig(self.visualization_png_gps_rtk_dir + 'gps_rtk.png')

        if self.plt_show:
            plt.show()

    def get_png_gps_rtk_dir(self):
        """get the png gps rtk directory

        :return: path to png gps rtk directory
        """
        return self.visualization_png_gps_rtk_dir


if __name__ == '__main__':
    gps = GPS_RTK(date='2012-01-08')
    gps.save_gps_rtk_png()
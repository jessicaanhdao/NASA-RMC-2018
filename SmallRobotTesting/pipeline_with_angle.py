import cv2
import numpy
import math
from enum import Enum

class Pipeline:
    """This is a generated class from GRIP.
    To use the pipeline first create a Pipeline instance and set the sources,
    next call the process method,
    finally get and use the outputs.
    """

    def __init__(self):
        """initializes all values to presets or None if need to be set
        """
        self.__source0 = None
        self.__blur_input = self.__source0
        self.__blur_type = BlurType.Gaussian_Blur
        self.__blur_radius = 0
        self.blur_output = None

        self.__hsv_threshold_input = self.blur_output
        self.__hsv_threshold_hue = [0.0, 180.0]
        self.__hsv_threshold_saturation = [0.0, 255.0]        
        self.__hsv_threshold_value = [225.0, 255.0]
        self.hsv_threshold_output = None

        self.__find_contours_input = self.hsv_threshold_output
        self.__find_contours_external_only = False
        self.find_contours_output = None

        self.__filter_contours_contours = self.find_contours_output
        self.__filter_contours_min_area = 400.0
        self.__filter_contours_min_perimeter = 4.0
        self.__filter_contours_min_width = 0
        self.__filter_contours_max_width = 2000
        self.__filter_contours_min_height = 0
        self.__filter_contours_max_height = 2000
        self.__filter_contours_solidity = [93.33453237410072, 100.0]
        self.__filter_contours_max_vertices = 1000000
        self.__filter_contours_min_vertices = 0
        self.__filter_contours_min_ratio = 0
        self.__filter_contours_max_ratio = 1000
        self.filter_contours_output = None


    def process(self, source0):
        """Runs the pipeline.
        Sets outputs to new values.
        Requires all sources to be set.
        """
        #Step Blur0:
        self.__blur_input = source0
        (self.blur_output ) = self.__blur(self.__blur_input, self.__blur_type, self.__blur_radius)

        #Step HSV_Threshold0:
        self.__hsv_threshold_input = self.blur_output
        (self.hsv_threshold_output ) = self.__hsv_threshold(self.__hsv_threshold_input, self.__hsv_threshold_hue, self.__hsv_threshold_saturation, self.__hsv_threshold_value)

        #Step Find_Contours0:
        self.__find_contours_input = self.hsv_threshold_output
        (self.find_contours_output ) = self.__find_contours(self.__find_contours_input, self.__find_contours_external_only)

        #Step Filter_Contours0:
        self.__filter_contours_contours = self.find_contours_output
        (self.filter_contours_output ) = self.__filter_contours(self.__filter_contours_contours, self.__filter_contours_min_area, self.__filter_contours_min_perimeter, self.__filter_contours_min_width, self.__filter_contours_max_width, self.__filter_contours_min_height, self.__filter_contours_max_height, self.__filter_contours_solidity, self.__filter_contours_max_vertices, self.__filter_contours_min_vertices, self.__filter_contours_min_ratio, self.__filter_contours_max_ratio)

    def set_source0(self, value):
        """Sets source0 to given value checking for correct type.
        """
        assert isinstance(value, numpy.ndarray) , "Source must be of type numpy.ndarray"
        self.__source0 = value



    @staticmethod
    def __blur(src, type, radius):
        """Softens an image using one of several filters.
        Args:
            src: The source mat (numpy.ndarray).
            type: The blurType to perform represented as an int.
            radius: The radius for the blur as a float.
        Returns:
            A numpy.ndarray that has been blurred.
        """
        if(type is BlurType.Box_Blur):
            ksize = int(2 * round(radius) + 1)
            return cv2.blur(src, (ksize, ksize))
        elif(type is BlurType.Gaussian_Blur):
            ksize = int(6 * round(radius) + 1)
            return cv2.GaussianBlur(src, (ksize, ksize), round(radius))
        elif(type is BlurType.Median_Filter):
            ksize = int(2 * round(radius) + 1)
            return cv2.medianBlur(src, ksize)
        else:
            return cv2.bilateralFilter(src, -1, round(radius), round(radius))

    @staticmethod
    def __hsv_threshold(input, hue, sat, val):
        """Segment an image based on hue, saturation, and value ranges.
        Args:
            input: A BGR numpy.ndarray.
            hue: A list of two numbers the are the min and max hue.
            sat: A list of two numbers the are the min and max saturation.
            lum: A list of two numbers the are the min and max value.
        Returns:
            A black and white numpy.ndarray.
        """
        out = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
        return cv2.inRange(out, (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))

    @staticmethod
    def __find_contours(input, external_only):
        """Sets the values of pixels in a binary image to their distance to the nearest black pixel.
        Args:
            input: A numpy.ndarray.
            external_only: A boolean. If true only external contours are found.
        Return:
            A list of numpy.ndarray where each one represents a contour.
        """
        if(external_only):
            mode = cv2.RETR_EXTERNAL
        else:
            mode = cv2.RETR_LIST
        method = cv2.CHAIN_APPROX_SIMPLE
        contours, hierarchy =cv2.findContours(input, mode=mode, method=method)
        return contours

    @staticmethod
    def __filter_contours(input_contours, min_area, min_perimeter, min_width, max_width,
                        min_height, max_height, solidity, max_vertex_count, min_vertex_count,
                        min_ratio, max_ratio):
        """Filters out contours that do not meet certain criteria.
        Args:
            input_contours: Contours as a list of numpy.ndarray.
            min_area: The minimum area of a contour that will be kept.
            min_perimeter: The minimum perimeter of a contour that will be kept.
            min_width: Minimum width of a contour.
            max_width: MaxWidth maximum width.
            min_height: Minimum height.
            max_height: Maximimum height.
            solidity: The minimum and maximum solidity of a contour.
            min_vertex_count: Minimum vertex Count of the contours.
            max_vertex_count: Maximum vertex Count.
            min_ratio: Minimum ratio of width to height.
            max_ratio: Maximum ratio of width to height.
        Returns:
            Contours as a list of numpy.ndarray.
        """
        output = []
        for contour in input_contours:
            x,y,w,h = cv2.boundingRect(contour)
            if (w < min_width or w > max_width):
                continue
            if (h < min_height or h > max_height):
                continue
            area = cv2.contourArea(contour)
            if (area < min_area):
                continue
            if (cv2.arcLength(contour, True) < min_perimeter):
                continue
            hull = cv2.convexHull(contour)
            solid = 100 * area / cv2.contourArea(hull)
            if (solid < solidity[0] or solid > solidity[1]):
                continue
            if (len(contour) < min_vertex_count or len(contour) > max_vertex_count):
                continue
            ratio = (float)(w) / h
            if (ratio < min_ratio or ratio > max_ratio):
                continue
            output.append(contour)
        return output


BlurType = Enum('BlurType', 'Box_Blur Gaussian_Blur Median_Filter Bilateral_Filter')

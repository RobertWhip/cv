from typing import List
import math
import util


class Pixel:
    def __init__(self, pixel) -> None:
        pass

    # Overloading "less than" ("<") operator 
    def __lt__(self, other):
        pass

    def __str__(self):
        pass

    def __add__(self, other):
        pass

    def mean(self, n) -> float:
        pass

    def get_value(self) -> float:
        pass

    @staticmethod
    def get_depth() -> int:
        pass

class GrayscalePixel:
    def __init__(self, pixel=0) -> None:
        self.value = pixel # 0 ... 255
        self.depth = self.get_depth()

    def __lt__(self, other):
        return (self.value < other.value)

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        return GrayscalePixel(self.value + other.value)

    def mean(self, n) -> float:
        return self.value / n
    
    def get_value(self) -> float:
        return self.value

    @staticmethod
    def get_depth() -> int:
        return 256

"""
    ImageProcessor - abstract class for image processors.

    Image processor is a class which consist of a set of functions for 
    image processing (analytics, equalization).
"""
class ImageProcessor:
    @staticmethod
    def raw_to_pixel(raw_pixel=None):
        pass
    
    def format_statistics(self, stats):
        min = str(stats['min'])
        max = str(stats['max'])
        mean = str(stats['mean'])
        ds = str(stats['ds'])
        var = str(stats['variance'])
        snr = str(stats['snr'])

        return f'Statistics:\n\
            Min: {min}\n\
            Max: {max}\n\
            Mean: {mean}\n\
            Standard deviation: {ds}\n\
            Variance: {var}\n\
            Signal-to-noise ratio: {snr}'

    def get_pixel_depth(self):
        pass

    # TODO: optimize
    def get_standard_deviation(self, image, stats) -> float:
        sum = 0

        for row in image:
            for raw_pixel in row:
                distance = (self.raw_to_pixel(raw_pixel).get_value() - stats['mean'])**2
                sum = sum + distance
        
        return math.sqrt(sum / stats['size'])

    """ 
        (1.a) Stasistics of image

        A function for statistical analysis of an image, which calculates 
        and returns min, max, mean, standard deviation, variance, and SNR 
        (signal-to-noise ratio) of an image.

        returns a dict of statistical values
    """
    def get_statistics(self, image) -> dict:
        stats = dict()

        stats['size'] = len(image) * len(image[0])
        stats['min'] = self.raw_to_pixel(image[0][0])
        stats['max'] = self.raw_to_pixel(image[0][0])
        stats['mean'] = self.raw_to_pixel()
        
        for row in image:
            for raw_pixel in row:
                pixel = self.raw_to_pixel(raw_pixel)

                if pixel < stats['min']:
                    stats['min'] = pixel

                if stats['max'] < pixel:
                    stats['max'] = pixel

                stats['mean'] = stats['mean'] + pixel

        # Calculating mean
        stats['mean'] = stats['mean'].get_value() / stats['size']

        # Calculating standard deviation
        stats['ds'] = self.get_standard_deviation(image, stats)

        # Calculating variance
        stats['variance'] = stats['ds']**2

        # Calculating signal-to-noise ratio
        stats['snr'] = 10 * math.log10(stats['mean'] / stats['ds'])

        return stats

    """ 
        (1.b) Histogram data

        A function, which calculates, returns the data for the histogram
        plot of an image.
    """
    def histogram(self, image) -> List[int]:
        h = [0] * self.get_pixel_depth()

        for row in image:
            for raw_pixel in row:
                i = self.raw_to_pixel(raw_pixel).get_value()
                h[i] = h[i]+1
        
        return h


    # probability mass function - https://www.tutorialspoint.com/dip/introduction_to_probability.htm
    def pmf(self, hist, stats):
        return list(map(lambda px: px / stats['size'], hist))

    # cumulative distributive function - https://www.tutorialspoint.com/dip/introduction_to_probability.htm
    def cdf(self, list):
        sum = 0

        for i in range(len(list)):
            sum = sum + list[i]
            list[i] = sum

        return list

    """ 
        (1.c) Histogram equalization

        A function, which accepts an image, performs its histogram equalization 
        and returns an image with an equalized histogram.

        https://www.tutorialspoint.com/dip/histogram_equalization.htm
    """
    def hist_equalize(self, image):
        histogram = self.histogram(image)
        stats = self.get_statistics(image)
        pmf = self.pmf(histogram, stats) # probability mass function
        cdf = self.cdf(pmf) # cumulative distributive function
        
        contrast_map = dict()
        for i in range(len(cdf)): # px - brightness
            px = cdf[i]
            contrast_map[i] = math.floor(px * (self.get_pixel_depth() - 1))

        equalized_img = util.copy_img(image)
        for y in range(len(image)):
            for x in range(len(image[y])):
                equalized_img[y][x] = contrast_map[image[y][x]]

        # TODO: optimize
        equalized_hist = self.histogram(equalized_img)

        return (equalized_img, equalized_hist)

    """ 
        (1.d) Linear contrast correction

        A function, which accepts an image and performs its linear contrast
        correction and returns an image with corrected contrast.
    """
    def lin_contrast_correct(self, image):
        stats = self.get_statistics(image)
        min = stats['min'].get_value()
        max = stats['max'].get_value()

        enhanced = util.copy_img(image)
        for y in range(len(image)):
            for x in range(len(image[y])):
                enhanced[y][x] = (image[y][x] - min) / (max - min) * self.get_pixel_depth()

        return enhanced

class GrayscaleImageProcessor(ImageProcessor):
    @staticmethod
    def raw_to_pixel(raw_pixel=0):
        return GrayscalePixel(raw_pixel)

    def get_pixel_depth(self):
        return GrayscalePixel.get_depth()
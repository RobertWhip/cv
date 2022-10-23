from image import GrayscaleImageProcessor
import util
import sys

STATISTICS = 'stats'
HISTOGRAM = 'hist'
HIST_EQUALIZATION = 'hist-eq'
LINEAR_CONTRAST_CORRECTION = 'lin-enhance'
commands = [
    STATISTICS,
    HISTOGRAM,
    HIST_EQUALIZATION,
    LINEAR_CONTRAST_CORRECTION,
]

if len(sys.argv) > 1:
    imp = GrayscaleImageProcessor()
    command = sys.argv[1]
    filename = sys.argv[2]

    if command == STATISTICS:
        img = util.read_grayscale(filename)

        print(img)
        print(
            imp.format_statistics(
                imp.get_statistics(img)
            )
        )
        sys.exit(0)
    elif command == HISTOGRAM:
        img = util.read_grayscale(filename)
        util.plot_histogram(imp.histogram(img))

        sys.exit(0)
    elif command == HIST_EQUALIZATION:
        img = util.read_grayscale(filename)
        hist = imp.histogram(img)
        eq_img, eq_hist = imp.hist_equalize(img)

        util.show_two('Original', img, 'Histogram equalized', eq_img)
        util.plot_histogram(hist)
        util.plot_histogram(eq_hist)

        sys.exit(0)
    elif command == LINEAR_CONTRAST_CORRECTION:
        img = util.read_grayscale(filename)
        enhanced_img = imp.lin_contrast_correct(img)
        util.show_two('Original', img, 'Enhanced image', enhanced_img)

        util.plot_histogram(imp.histogram(img))
        util.plot_histogram(imp.histogram(enhanced_img))
        sys.exit(0)
    else:
        print('Invalid command: ' + command)

print('Please choose from the following commands: ' + str(commands))
sys.exit(1)
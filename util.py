import matplotlib.pyplot as plt
import cv2


def copy_img(img):
    return img.copy()

def show(label, img):
    cv2.imshow(label, img)

def show_two(label0, img0, label1, img1):
    show(label0, img0)
    show(label1, img1)

    # Maintain output window util user presses a key
    cv2.waitKey(0)       
    
    # Destroying present windows on screen
    cv2.destroyAllWindows()

def read(filepath):
    return cv2.imread(filepath)

def read_grayscale(filepath):
    return cv2.cvtColor(read(filepath), cv2.COLOR_BGR2GRAY)

def save(filepath, img):
    cv2.imwrite(filepath, img)

def plot_histogram(x):
    plt.bar(range(len(x)), x)
    plt.show()
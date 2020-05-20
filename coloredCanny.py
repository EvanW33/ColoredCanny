import cv2
import numpy as np


class Color():
    """
    Class used to hold color values to be used to give each pixel in the edged
    detection color.
    """

    def __init__(self, update_parameter):
        """
        Variables:
        update_parameter: used to determine how much to change each pixel on every
            pixel next in the numpy array of pixels in the image. Increases until the color
            reaches 255.0 and then resets it to randNum
        """
        self.randNum = np.random.randint(0., 255.0)
        self.counter = 0
        self.update_parameter = update_parameter
        self.rand1 = np.random.randint(0., 255.0)
        self.rand2 = np.random.randint(0., 255.0)
        self.rand3 = np.random.randint(0., 255.0)
        self.color = np.array([self.rand1, self.rand2, self.rand3])
        self.colorCopy = self.color
        self.index = 0
        self.update_addition = np.zeros(3)
        self.update_addition[self.index] = self.update_parameter

    def __repr__(self):
        return self.color

    def getColor(self):
        """
        Returns the color
        """
        return self.color

    def getColorCopy(self):
        """
        Returns the variable colorCopy
        """
        return self.colorCopy

    def getIndex(self):
        """
        Returns the index of the colors in the numpy array being changed
        """
        return self.index

    def getNextRandNum(self):
        """
        Gets a new random number once old one's exhausted
        """
        self.randNum = np.random.randint(0., 255.0)
        self.counter = 0

    def next_color(self, color_selected):
        """
        Picks the next color in the form of a numpy array.
        Adds a small value so that the color changes very
        slightly between pixels
        """
        if color_selected.all() == self.colorCopy.all():
            self.colorCopy = np.add(self.colorCopy, self.update_addition)
            self.above_max()
        elif color_selected.all() == self.color.all():
            self.color = np.add(self.color, self.update_addition)
            self.above_max()

    def above_max(self):
        """
        Checks if a color needs to be changed due to reaching
        the maximum value of RGB (255.0). Then applies the change
        by setting the value to value over 255.0 to 0 and changes the
        incrementation index
        """
        if self.color[self.index] >= 255.0:
            self.color[self.index] = self.randNum
            self.counter += 1
            self.update_index()
        for i in range(3):
            if self.colorCopy[i] >= 255.0:
                self.colorCopy[i] = self.randNum
                self.counter += 1
                self.update_index()
        if self.counter >= 2:
            self.getNextRandNum()

    def update_index(self):
        """
        Updates the index that is currently being changed
        """
        self.update_addition[self.index] = 0.0
        if self.index == 2:
            self.index = 0
        else:
            self.index += 1
        self.update_addition[self.index] = self.update_parameter

    def revert_to_copy(self):
        """
        Changes the color back to the copy and increments it by 1.
        This keeps the columns and rows around a specific area in a
        similar color spectrum
        """
        self.next_color(self.colorCopy)
        self.color = self.colorCopy


def convert_pixels(image, color):
    """
    Converts each pixel to have 3 challenges (color). This uses the
    color class object to convert those 3 channels to be the correct
    color and to not be extremely random.
    """
    rows, cols = image.shape
    color_image = np.zeros((rows,cols,3),dtype=np.uint8)

    # Gets all the edges
    clrs = image.nonzero()

    # counts to reset the color starting on the next row
    counter = 0
    for i in zip(*clrs):
        color_image[i] = color.color
        color.next_color(color.getColor())
        counter += 1
        if counter % cols == 0:
            color.revert_to_copy()

    return color_image


def main():
    """
    Function that creates a video from the user's webcam, then applies the
    Canny image filter to show edges, then uses convert_pixels to change the
    pixels from grayscale to RGB, this gives the pixels color and then prints
    the pixels to the screen.
    """
    # Gets video from the webcam
    cap = cv2.VideoCapture(0)

    # Sets dimensions of the image
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Creates a color class to hold all color values
    color = Color(0.01)

    while True:
        # reads in the image and gets where or not it was read as a bool
        success, image = cap.read()

        # Makes sure the image is being read in correctly
        if success == False:
            break

        # Turns the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        lower = 40
        higher = 100

        # Converts the image to edges
        edged = cv2.Canny(gray, lower, higher)
        # Changes the pixels from grayscale to be colorful
        edged = convert_pixels(edged, color)

        # Shows the image
        cv2.imshow("Colored Canny Video", edged)

        # Wait for Esc key to stop
        esc = cv2.waitKey(30) & 0xff
        if esc == 27: # breaks if escape is pressed
            break

    # Exits out of the opencv window
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

import cv2
import numpy as np
from picamera import PiCamera
import picamera.array
from fastiecm import fastiecm


# Load a specific image (for testing purposes)
# original = cv2.imread('/home/pi/project/park.png')
# original = cv2.imread('test.png')


'''
Take an image with the camera
'''
def take_picture():
    # Instantiate a camera object
    cam = PiCamera()
    # Rotate image if needed
    cam.rotation = 180
    # Set resolution of image
    # cam.resolution = (1920, 1080)
    cam.resolution = (800, 600)
    # Save image as file (for testing purposes)
    # cam.capture('test.png')
    stream = picamera.array.PiRGBArray(cam)
    cam.capture(stream, format='bgr', use_video_port=True)
    original = stream.array
    cam.close()
    # return cv2.imread('test.png')
    return original.astype(np.uint8)


''' 
Displays the image.
Type any key to close the window.
'''
def display(image, image_name):
    # convert image into an array of dtype
    image = np.array(image, dtype=float)/float(255)
    # Get original image size dimensions
    shape = image.shape
    # Modify image height 
    height = int(shape[0]/3)
    # Modify image width
    width = int(shape[1]/2)
    # Resize the image using width and height
    image = cv2.resize(image, (width, height))
    # Create display window
    cv2.namedWindow(image_name)
    # Show (open) the window
    cv2.imshow(image_name, image)
    # Wait for key interrupt
    cv2.waitKey(0)
    # Close the window after interrupt
    cv2.destroyAllWindows()


'''
Modify the image to increase contrast.
'''
def contrast_stretch(im):
    # Find the top brightness of pixels
    # in the top 5% and bottom 5% of image
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    # Define maximum and minimum brightness
    out_min = 0.0
    out_max = 255.0

    # Calculations to increase image contrasts
    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    # Return new contrasted image
    return out


'''
Calculate NDVI (Normalised Difference Vegetation Index)
'''
def calc_ndvi(image):
    # Get blue, green, red values
    b, g, r = cv2.split(image)
    # Add red and blue
    bottom = (r.astype(float) + b.astype(float))
    # If bottom = 0, set it to 0.01 (avoid divide by 0)
    bottom[bottom==0] = 0.01
    # Calculate NDVI value
    # by subtracting blue by red
    # then divided by the sum
    ndvi = (r.astype(float) - b) / bottom
    # Save NDVI array as .csv file
    # (warning - file size is about 32 MB)
    # Return NDVI value
    print(f'Mean: {np.mean(ndvi)}')
    print(f'Median: {np.median(ndvi)}')
    print(f'Max: {ndvi.max()}')
    return ndvi, np.percentile(ndvi, 70), np.percentile(ndvi, 95)


if __name__ == '__main__':
    original = take_picture()
    # original = cv2.imread('test.png').astype(float)
    print("Picture taken!")
    # display(original, 'Original')
    contrasted = contrast_stretch(original)
    # display(contrasted, 'Contrasted original')
    # Create/Update contrasted image file
    # cv2.imwrite('contrasted.png', contrasted)
    # Calculate NDVI value
    ndvi, p1, p2 = calc_ndvi(contrasted) 
    print("P1: ", p1, "\nP2: ", p2)
    # np.savetxt("output.csv", ndvi, fmt="%.3f", delimiter=",")
    # display(ndvi, 'NDVI')
    # cv2.imwrite('ndvi.png', ndvi)
    # If image is too dark, increase contrast
    ndvi_contrasted = contrast_stretch(ndvi)
    # display(ndvi_contrasted, 'NDVI Contrasted')
    # Save NDVI array as .csv file
    # (warning - file size is about 32 MB)
    np.savetxt("output.csv", ndvi, fmt="%.3f", delimiter=",")
    color_mapped_prep = ndvi_contrasted.astype(np.uint8)
    color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
    cv2.imwrite('color_mapped_image.png', color_mapped_image)
    np.savetxt("color_mapped.csv", color_mapped_prep, fmt="%.3f", delimiter=",")
    cv2.imwrite('test.png', original)
    # for i in range(1,10):
    #     print(original[0][i], sep=" ")
    # print()
    b,g,r = cv2.split(original)
    np.savetxt('test.csv', g, fmt='%.3f', delimiter=',')
    cv2.imwrite('test_contrasted.png', contrasted)
    cv2.imwrite('ndvi_contrasted.png', ndvi_contrasted)

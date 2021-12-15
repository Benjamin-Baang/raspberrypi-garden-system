import cv2
import numpy as np

# Load a specific image
original = cv2.imread('/home/pi/project/park.png')


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
    ndvi = (b.astype(float) - r) / bottom
    # Save NDVI array as .csv file
    # (warning - file size is about 32 MB)
    # np.savetxt("output.csv", ndvi, fmt="%.3f", delimiter=",")
    # Return NDVI value
    return ndvi


display(original, 'Original')
contrasted = contrast_stretch(original)
display(contrasted, 'Contrasted original')
# Create/Update contrasted image file
cv2.imwrite('contrasted.png', contrasted)
# Calculate NDVI value
ndvi = calc_ndvi(contrasted)
display(ndvi, 'NDVI')
cv2.imwrite('ndvi.png', ndvi)
# If image is too dark, increase contrast
ndvi_contrasted = contrast_stretch(ndvi)
display(ndvi_contrasted, 'NDVI Contrasted')
cv2.imwrite('ndvi_contrasted.png', ndvi_contrasted)

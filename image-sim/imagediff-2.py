from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

def mse(imageA, imageB):
  # the 'Mean Squared Error' between the two images is the
  # sum of the squared difference between the two images;
  # NOTE: the two images must have the same dimension
  err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
  err /= float(imageA.shape[0] * imageA.shape[1])
  
  # return the MSE, the lower the error, the more "similar"
  # the two images are
  return err
 
def compare_images(imageA, imageB, title):
  # compute the mean squared error and structural similarity
  # index for the images
  m = mse(imageA, imageB)
  s = ssim(imageA, imageB)
  print "MSE: %.2f, SSIM: %.2f" % (m, s)
 

a = cv2.imread("~/Desktop/image similarity test/a.jpg")
b = cv2.imread("~/Desktop/image similarity test/b.jpg")
 
# convert the images to grayscale
a_ = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
b_ = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)

 
# compare the images
compare_images(a, b, "a -> b")
compare_images(a_, b_, "a_ -> b_")

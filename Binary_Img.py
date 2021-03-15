import numpy as np
import matplotlib.pyplot as plt
import cv2

     ### Function of creating thresholded binary image
def threshold_binary(img, sobelx_thresh=(0, 255), channel_thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    l_channel = hls[:, :, 1]
    s_channel = hls[:, :, 2]
    # Sobel Operator in x direction
    sobel_x = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0)
    abs_sobelx = np.absolute(sobel_x)
    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))

    # Apply threshold for sobel in x direction
    sobelx_binary = np.zeros_like(scaled_sobel)
    sobelx_binary[(scaled_sobel > sobelx_thresh[0]) & (scaled_sobel < sobelx_thresh[1])] = 1
    
    # Apply threshold for color channel (in s channel)
    channel_binary = np.zeros_like(s_channel)
    channel_binary[(s_channel > channel_thresh[0])&(s_channel < channel_thresh[1])] = 1

    # get new binary image by combining two binary image
    combined_binary = np.zeros_like(sobelx_binary)
    combined_binary[(sobelx_binary == 1) | (channel_binary == 1)] = 1

    return combined_binary

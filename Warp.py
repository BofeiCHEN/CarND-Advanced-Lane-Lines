import numpy as np
import cv2
from Finding_Lane import fit_polynomial
from Binary_Img import threshold_binary

def show_warp_lane(img, warp_lane):
    ### img => undistort image
    
    # Combine the result with the original image and return
    return cv2.addWeighted(img, 1, warp_lane, 0.3, 0)

def warp_lane(img, matrix): 
    ### img => birds eye image

    # get left_fitx, right_fitx, ploty
    binary_birds_eye = threshold_binary(img, sobelx_thresh=(70, 170), channel_thresh=(170, 255))
    
    left_fitx, right_fitx, ploty, out_img = fit_polynomial(binary_birds_eye)
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(img, np.int_([pts]), (0,255, 0))

    # Warp the lane back to original image space using inverse perspective matrix (Minv)
    return cv2.warpPerspective(img, matrix, (binary_birds_eye.shape[1], binary_birds_eye.shape[0])) 
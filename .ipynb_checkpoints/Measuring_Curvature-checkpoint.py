import numpy as np
import matplotlib.pyplot as plt
import cv2
from Finding_Lane import find_lane_pixels


def generate_polynomials(binary_warped, ym_per_pix, xm_per_pix):
    '''
    Generates the second order polynomial
    '''

    # Find our lane pixels 
    leftx, lefty, rightx, righty, out_img = find_lane_pixels(binary_warped)
    # Fit a second order polynomial
    left_fit_cr = np.polyfit(lefty*ym_per_pix, leftx*xm_per_pix, 2)
    right_fit_cr = np.polyfit(righty*ym_per_pix, rightx*xm_per_pix, 2)
    
    return left_fit_cr, right_fit_cr

    
def measure_curvature_real(binary_warped_img, ym_per_pix, xm_per_pix):
    '''
    Calculates the curvature of polynomial functions in meters.
    '''
    
    # get the second order polynomia 
    left_fit_cr, right_fit_cr = generate_polynomials(binary_warped_img, ym_per_pix, xm_per_pix)
    
    # The maximum y-value => the bottom of image
    y_eval = np.max(binary_warped_img.shape[0])*ym_per_pix
    
    x_left_cr = left_fit_cr[0]*y_eval**2 + left_fit_cr[1]*y_eval + left_fit_cr[2]
    x_right_cr = right_fit_cr[0]*y_eval**2 + right_fit_cr[1]*y_eval + right_fit_cr[2]
    x_max = binary_warped_img.shape[1]*xm_per_pix
    veh_position = x_max/2 - (x_left_cr + x_right_cr)/2 # if in left pos < 0, if in right pos > 0
    
    # Radius of curvature
    if (0 != left_fit_cr[0]):
        left_curverad = pow(1 + (2*y_eval*left_fit_cr[0] + left_fit_cr[1])**2, 3/2)/abs(2*left_fit_cr[0])  
    else:
        left_curverad = 0
        
    if (0 != right_fit_cr[0]):
        right_curverad = pow(1 + (2*y_eval*right_fit_cr[0] + right_fit_cr[1])**2, 3/2)/abs(2*right_fit_cr[0])  
    else:
        right_curverad = 0  
    
    return left_curverad, right_curverad, veh_position

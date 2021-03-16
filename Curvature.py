import numpy as np
import matplotlib.pyplot as plt
import cv2
from Finding_Lane import find_lane_pixels
from Binary_Img import threshold_binary

def generate_polynomials(binary_warped, ym_per_pix, xm_per_pix):
    '''
    Generates the second order polynomial
    '''

    # Find our lane pixels 
    leftx, lefty, rightx, righty, out_img, success = find_lane_pixels(binary_warped)
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
    
    # Check if the lane is successfully found, lane weight = 3.7 meters
    sucess = True
    line_dis = abs(x_right_cr - x_left_cr)
    lane_weight = 3.7
    if(abs(line_dis - lane_weight) > 0.3):
        #sucess = False
        veh_position = "error"

    # Curvature
    if (0 != left_fit_cr[0]):
        left_curverad = pow(1 + (2*y_eval*left_fit_cr[0] + left_fit_cr[1])**2, 3/2)/abs(2*left_fit_cr[0])  
    else:
        left_curverad = 0
        
    if (0 != right_fit_cr[0]):
        right_curverad = pow(1 + (2*y_eval*right_fit_cr[0] + right_fit_cr[1])**2, 3/2)/abs(2*right_fit_cr[0])  
    else:
        right_curverad = 0

    # Two curvature should be same
    if (left_curverad > 200) & (right_curverad > 200):
        left_curverad = "straight"
        right_curverad = "straight"
    elif(2*abs((left_curverad - right_curverad)/(left_curverad + right_curverad)) > 0.2):
        #sucess = False
        left_curverad = "error"
        right_curverad = "error"
    
    return left_curverad, right_curverad, veh_position, sucess

    
def display_curvature(img, ym_pix, xm_pix): # Write and display the curvature to image
    ### img => birds eye image
    ### ym_pix => y distance in meter per pix
    ### xm_pix => x distance in meter per pix
    
    # get the curvature and position
    measure_binary = threshold_binary(img, sobelx_thresh=(70, 170), channel_thresh=(170, 255))
    left, right, veh_pos, success = measure_curvature_real(measure_binary, ym_pix, xm_pix)
    
    return write_curvature(img, left, right, veh_pos)
    

def write_curvature(img, left, right, pos):
    ### left => left point curvature value
    ### right => right point curvature value
    ### position => vehicle position in the lane, if in left pos < 0, if in right pos > 0
    
    # write the curvature to image
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    LeftText = (100,100)
    RightText = (100,200)
    PosText = (100,300)
    if (pos == "error"):
        veh_pos_text  = "Vehicle position error. " 
    elif pos < 0:
        l_r_sign = "left"
        veh_pos_text  = "Vehicle is " + str(abs(round(pos, 2))) +"m " + l_r_sign + " of the center"
    elif pos > 0:
        l_r_sign = "right"
        veh_pos_text  = "Vehicle is " + str(abs(round(pos, 2))) +"m " + l_r_sign + " of the center"
    
    
    if ((left == "straight") or (left == "error")):
        left_curvature_text         = "Left curvature: " + left
        right_curvature_text         = "Right curvature: " + right
    else:
        left_curvature_text         = "Left curvature: " + str(round(left, 2)) +"m"
        right_curvature_text         = "Right curvature: " + str(round(right, 2)) +"m"

    cv2.putText(img,left_curvature_text, 
        LeftText, 
        font, 
        fontScale,
        fontColor,
        lineType)

    cv2.putText(img,right_curvature_text, 
        RightText, 
        font, 
        fontScale,
        fontColor,
        lineType)
    
    cv2.putText(img,veh_pos_text, 
        PosText, 
        font, 
        fontScale,
        fontColor,
        lineType)
    
    return img
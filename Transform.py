import numpy as np
import cv2

def transform_matrix():
    # Define 4 source points 
    #test1_src = np.float32([[499, 530], [844, 530], [1008, 630], [362, 630]])
    straight2_src = np.float32([[557, 475], [729, 475], [961, 630], [345, 630]]) 
    src = straight2_src

    # Define 4 destination points 
    #test1_dst = np.float32([[500, 550], [800, 550], [800, 630], [500, 630]])
    straight2_dst = np.float32([[500, 300], [800, 300], [800, 680], [500, 680]])

    dst = straight2_dst
    # Get the transform matrix
    M = cv2.getPerspectiveTransform(src, dst)
    Min = cv2.getPerspectiveTransform(dst, src)
    return M, Min
    
def transform(tran_matrix, img):
    ### Get the warped image,
    ### if tran_matrix = M, img = undist image => return birds_eye image
    ### if tran_matrix = Min, img = birds_eye image => return undist image
    
    return cv2.warpPerspective(img, tran_matrix, img.shape[1::-1], flags=cv2.INTER_LINEAR)
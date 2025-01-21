#Copyright (c) 2022-2024, INRAE - MIAT
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#
#Author : Christophe Klopp
#https://github.com/chklopp/extract_chromosomes_images_juicebox/
#

import cv2
import numpy as np
import sys
import os

# read image
img = cv2.imread(sys.argv[1])
filename = sys.argv[1]
#cv2.imshow("img", img)

# do simple color reduction
imgcopy = img.copy()
#div = 128
#imgcopy = div * ( imgcopy // div ) + div // 2
#list_bgr_colors = np.unique(imgcopy.reshape(-1, imgcopy.shape[2]), axis=0)
#print(list_bgr_colors)
list_bgr_colors, count_bgr_colors = np.unique(img.reshape(-1, img.shape[2]), axis=0, return_counts=1)
#count_bgr_colors = np.count(img.reshape(-1, img.shape[2]), axis=0)
print(list_bgr_colors)
print(count_bgr_colors)

# threshold on yellow color
lower=(255,0,0)
upper=(255,0,0)
mask = cv2.inRange(img, lower, upper)

# change all non-yellow to white
result = img.copy()
result[mask!=255] = (255, 255, 255)

# save results
# cv2.imwrite('corn_yellow.jpg',result)

# display result
#cv2.imshow("mask", mask)
#cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply Canny Edge Detection
edges = cv2.Canny(result, 300, 300)
#cv2.imshow("edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Find contours from the edges
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

l = 0 

for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    if w > 100 and h > 100 and w / (w+h) > 0.48 and  w / (w+h) < 0.52 :
        l += 1
j = 1

for i, contour in enumerate(contours):
    # Get bounding box of the contour
    x, y, w, h = cv2.boundingRect(contour)
    print(x, y, w, h)
    
    # Apply a size filter to ignore small artifacts (optional)
    if w > 100 and h > 100 and w / (w+h) > 0.48 and  w / (w+h) < 0.52 :  # Adjust this threshold as needed
    #if w > 100 and h > 100 :  # Adjust this threshold as needed
        
        chr = l - j + 1
        # Extract the region of interest (ROI)
        roi = imgcopy[y:y+h, x:x+w]
        roi_flip = cv2.flip(roi, 0)
        
        # Save the ROI
        output_path = os.path.join(f"{filename}_chr_{chr}.png")
        cv2.imwrite(output_path, roi_flip)
        j += 1

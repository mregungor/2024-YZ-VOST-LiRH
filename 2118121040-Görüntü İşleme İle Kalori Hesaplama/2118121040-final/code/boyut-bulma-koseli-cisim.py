# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:34:50 2024

@author: Melisa
"""
import cv2
import numpy as np

SCALE = 3
PAPER_W = 210 * SCALE
PAPER_H = 297 * SCALE

def load_image(path, scale=0.35):#Resim yükleyen bir fonksiyondur. 
    img = cv2.imread(path)
    img_resized = cv2.resize(img, (0, 0), None, scale, scale)
    return img_resized

def show_image(img, window_name="Image"):#Bir görüntüyü gösteren bir fonksiyondur. 
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def preprocess_image(img, thresh_1=57, thresh_2=232):#Görüntüyü önişleyen bir fonksiyondur.
    img_gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)      
    img_blur  = cv2.GaussianBlur(img_gray, (5,5), 1)       
    img_canny = cv2.Canny(img_blur, thresh_1, thresh_2)    
    
    kernel = np.ones((3,3))    
    img_dilated = cv2.dilate(img_canny, kernel, iterations=1)    
    img_closed = cv2.morphologyEx(img_dilated, cv2.MORPH_CLOSE, 
                                  kernel, iterations=4)          
    
    img_preprocessed = img_closed.copy()
    
    img_each_step = {'img_dilated': img_dilated, 
                     'img_canny'  : img_canny, 
                     'img_blur'   : img_blur, 
                     'img_gray'   : img_gray,
                     'img_preprocessed': img_preprocessed}
    
    return img_preprocessed, img_each_step

def find_contours(img_preprocessed, img_original, epsilon_param=0.04):
    contours, _ = cv2.findContours(image=img_preprocessed, 
                                   mode=cv2.RETR_EXTERNAL, 
                                   method=cv2.CHAIN_APPROX_NONE)  
    
    img_contour = img_original.copy()
    cv2.drawContours(img_contour, contours, -1, (203,192,255), 6)  
    
    polygons = []
    for contour in contours:
        epsilon = epsilon_param * cv2.arcLength(curve=contour, 
                                                closed=True)  
        polygon = cv2.approxPolyDP(curve=contour, 
                                   epsilon=epsilon, closed=True)  

        # Polygon 4 köşe noktası içermiyorsa convexHull ile dörtgeni al
        if len(polygon) != 4:
            hull = cv2.convexHull(contour)
            polygon = cv2.approxPolyDP(hull, epsilon=0.02*cv2.arcLength(hull, True), closed=True)
        
        polygon = polygon.reshape(-1, 2)  
        rect_coords = np.float32(reorder_coords(polygon))  
        polygons.append(rect_coords)
        
        for point in rect_coords:    
            img_contour = cv2.circle(img=img_contour, center=tuple(point.astype(int)), 
                                     radius=8, color=(0,240,0), 
                                     thickness=-1)  
    
    return polygons, img_contour

def reorder_coords(polygon):#Dörtgenin köşe noktalarını yeniden sıralayan bir fonksiyondur
    rect_coords = np.zeros((4, 2))

    add = polygon.sum(axis=1)
    rect_coords[0] = polygon[np.argmin(add)]    # Top left
    rect_coords[3] = polygon[np.argmax(add)]    # Bottom right

    subtract = np.diff(polygon, axis=1)
    rect_coords[1] = polygon[np.argmin(subtract)]    # Top right
    rect_coords[2] = polygon[np.argmax(subtract)]    # Bottom left
    
    return rect_coords

def warp_image(rect_coords, paper_coords, img_original, pad=5):#Görüntüyü dörtgenin içine yerleştiren bir perspektif dönüşümü uygular.
    matrix = cv2.getPerspectiveTransform(src=rect_coords, 
                                         dst=paper_coords)   
    img_warped = cv2.warpPerspective(img_original, matrix,
                                      (PAPER_W, PAPER_H))    

    warped_h = img_warped.shape[0]
    warped_w = img_warped.shape[1]
    img_warped = img_warped[pad:warped_h-pad, pad:warped_w-pad]  

    return img_warped

def calculate_sizes(polygons_warped):#Dörtgenlerin boyutlarını hesaplayan bir fonksiyondur
    
    rect_coords_list = []
    for polygon in polygons_warped:
        rect_coords = np.float32(reorder_coords(polygon))  
        rect_coords_list.append(rect_coords)
    
    heights = []
    widths  = []
    for rect_coords in rect_coords_list:
        height = cv2.norm(rect_coords[0], rect_coords[2], cv2.NORM_L2)  
        width  = cv2.norm(rect_coords[0], rect_coords[1], cv2.NORM_L2)  
        
        heights.append(height)
        widths.append(width)
    
    heights = np.array(heights).reshape(-1,1)
    widths  = np.array(widths).reshape(-1,1)
    
    sizes = np.hstack((heights, widths))  
        
    return sizes, rect_coords_list

def convert_to_mm(sizes_pixel, img_warped):#Piksel cinsinden ölçülen boyutları milimetre cinsine dönüştüren bir fonksiyondur.
    warped_h = img_warped.shape[0]
    warped_w = img_warped.shape[1]
    
    scale_h = PAPER_H / warped_h    
    scale_w = PAPER_W / warped_w    
    
    sizes_mm = []
    
    for size_pixel_h, size_pixel_w in sizes_pixel:
        size_mm_h = size_pixel_h * scale_h / SCALE    
        size_mm_w = size_pixel_w * scale_w / SCALE    
        
        sizes_mm.append([size_mm_h, size_mm_w])
    
    return np.array(sizes_mm)

def write_size(rect_coords_list, sizes, img_warped):#Dörtgenlerin etrafına boyutları yazan bir fonksiyondur.
    
    img_result = img_warped.copy()
    
    for rect_coord, size in zip(rect_coords_list, sizes):
        
        top_left = rect_coord[0].astype(int)
        top_right = rect_coord[1].astype(int)
        bottom_left = rect_coord[2].astype(int)
        
        cv2.line(img_result, tuple(top_left), tuple(top_right), (255,100,50), 4)
        cv2.line(img_result, tuple(top_left), tuple(bottom_left), (100,50,255), 4)
        
        cv2.putText(img_result, f'{np.int32(size[0])} mm', 
                    (bottom_left[0]-20, bottom_left[1]+50), 
                    cv2.FONT_HERSHEY_DUPLEX, 1, (100,50,255), 1)

        cv2.putText(img_result, f'{np.int32(size[1])} mm', 
                    (top_right[0]+20, top_right[1]+20), 
                    cv2.FONT_HERSHEY_DUPLEX, 1, (255,100,50), 1)
    
    return img_result

if __name__ == '__main__':
    img_original = load_image(path=r'C:\Users\Melisa\Desktop\Tez calismasi\koseli-cisimlerin-boyutunu-bulma\kutu.jpg')

    cv2.imshow("Image", img_original)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    img_preprocessed, img_each_step = preprocess_image(img_original)

    show_image(img_each_step['img_gray'], "Grayscale")
    show_image(img_each_step['img_blur'], "Blurred")
    show_image(img_each_step['img_canny'], "Canny")
    show_image(img_each_step['img_dilated'], "Dilated")

    polygons, img_contours = find_contours(img_preprocessed, img_original, epsilon_param=0.04)
    show_image(img_contours)
    print("Polygon Points:", polygons[0])

    if len(polygons) > 0:
        # Dörtgenin köşe noktalarını ve kağıdın köşe noktalarını oluştur
        rect_coords = np.float32(reorder_coords(polygons[0]))
        paper_coords = np.float32([[0,0],                # Top left
                                   [PAPER_W,10],          # Top right
                                   [0,PAPER_H],          # Bottom left
                                   [PAPER_W,PAPER_H]])   # Bottom right

        # Görüntüyü kağıdın boyutlarına dönüştür
        img_warped = warp_image(rect_coords, paper_coords, img_original)

        cv2.imshow("Warped Image", img_warped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Dönüştürülen görüntüyü yeniden işle ve dörtgenleri bul
        img_warped_preprocessed, _ = preprocess_image(img_warped)
        polygons_warped, img_contours_warped = find_contours(img_warped_preprocessed, img_warped,
                                                             epsilon_param=0.04)
        show_image(img_contours_warped)
        print("Warped Polygon Points:", polygons_warped[0])

        sizes, rect_coords_list = calculate_sizes(polygons_warped)
        sizes_mm = convert_to_mm(sizes, img_warped)
        img_result = write_size(rect_coords_list, sizes_mm, img_warped)  

        cv2.imshow("Measured Image", img_result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()




   



    


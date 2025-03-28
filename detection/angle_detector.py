import cv2
import numpy as np

from sklearn.cluster import KMeans
from utils.log_config import get_logger
from camera.pi_camera import PiCamera

logger = get_logger(__name__)

class AngleDetector():

    def __init__(self, test_mode: False):
        self.camera = PiCamera()
        self.test_mode = test_mode

    def get_angles(self):
        angles = []
        
        #img = self.camera.take_picture()
        img = cv2.imread("C:/Users/minfang/HSLU/PREN/images/point.jpg")

        transformed_img = self.transform_img(img)

        circle_center = self.get_circle_center(transformed_img)

        edge_points = self.get_edge_points(transformed_img)
        
        for edge_point in edge_points:
            angles.append(self.calculate_angle(circle_center, edge_point))

            if self.test_mode:
                cv2.circle(transformed_img, (edge_point[0], edge_point[1]), 5, (0, 0, 255), -1)  # draw edge point on image
                cv2.line(transformed_img, circle_center, (edge_point[0], edge_point[1]), (255, 0, 0), 2)  # draw blue line

        if self.test_mode:
            cv2.imwrite()

        return angles  

    def get_circle_center(self, img):
        # convert image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

        gray_blurred = cv2.blur(gray, (3, 3))

        kernel = np.ones((5,5),np.uint8)
        eroded_img = cv2.morphologyEx(gray_blurred, cv2.MORPH_OPEN, kernel)

        detected_circles = cv2.HoughCircles(image = eroded_img,  
                                            method = cv2.HOUGH_GRADIENT, 
                                            dp = 1.2, 
                                            minDist = 200, 
                                            param1 = 50, 
                                            param2 = 30, 
                                            minRadius = 180, 
                                            maxRadius = 220)
        
        if detected_circles is not None:
            if len(detected_circles) > 1:
                logger.warning("More than one waypoint was detected on the image!", detected_circles)

            detected_circles = np.uint16(np.around(detected_circles))

            for x, y, r in detected_circles[0, :]:
                logger.info(f"Circle detected on image with center point ({x}, {y})")
                return (x, y)
        else:
            raise Exception("No circle found")

    def get_edge_points(self, img):
        white_edge_pixles = [] # all white edge pixles
        height, width, _ = img.shape # image size

        # convert image to gray scale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # turns ever pixel black except defined range
        _, binary = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY)

        # search for white pixels on top and bottom image line
        for x in range(width):
            if binary[0, x] == 255:  # top
                white_edge_pixles.append((x, 0))
            if binary[height - 1, x] == 255:  # bottom
                white_edge_pixles.append((x, height - 1))

        # search for white pixels on left and right image line
        for y in range(height):
            if binary[y, 0] == 255:  # left
                white_edge_pixles.append((0, y))
            if binary[y, width - 1] == 255:  # right
                white_edge_pixles.append((width - 1, y))

        
        if len(white_edge_pixles) > 1:
            kmeans = KMeans(n_clusters=min(5, len(white_edge_pixles)), n_init=10).fit(white_edge_pixles)
            edge_points = kmeans.cluster_centers_.astype(int)
        else:
            edge_points = white_edge_pixles

        return edge_points

    def transform_img(self, img):
        # coordinates to transform
        tl = (900,1400)
        bl = (400, 1900)
        tr = (1700,1400)
        br = (2200,1900)

        if self.test_mode:
            cv2.circle(img, tl, 5, (0,0,255), -1)
            cv2.circle(img, bl, 5, (0,0,255), -1)
            cv2.circle(img, tr, 5, (0,0,255), -1)
            cv2.circle(img, br, 5, (0,0,255), -1)
        
        # transform image
        pts1 = np.float32([tl, bl, tr, br])
        pts2 = np.float32([(0,0), (0,600), (600,0), (600,600)])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        transformed_img = cv2.warpPerspective(img, matrix, (600,600))

        return transformed_img
    
    def calculate_angle(self, circle_center, edge_point):
        delta_y = edge_point[1] - circle_center[1]
        delta_x = edge_point[0] - circle_center[0]
        angle_rad = np.arctan2(delta_x, delta_y)
        angle_deg = np.degrees(angle_rad)

        # ensure that the angle is between 0 and 360
        angle_deg = (angle_deg + 360) % 360
        logger.info(f"Found line on waypoint with angle: {angle_deg}")

        return angle_deg
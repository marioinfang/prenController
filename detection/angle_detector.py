import cv2
import numpy as np
from collections import defaultdict

from sklearn.cluster import KMeans
from utils.log_config import get_logger

logger = get_logger(__name__)
SHOW_IMAGES = False

class AngleDetector():

    def __init__(self, test_mode: False):
        self.test_mode = test_mode

    def get_angles(self, img):
        angles = []

        transformed_img = self.transform_img(img)

        circle_center = self.get_circle_center(transformed_img)

        edge_points = self.get_edge_points(transformed_img, circle_center)

        for edge_point in edge_points:
            angles.append(self.calculate_angle(circle_center, edge_point))

            if self.test_mode:
                cv2.circle(transformed_img, (edge_point[0], edge_point[1]), 5, (0, 0, 255), -1)  # draw edge point on image
                cv2.line(transformed_img, circle_center, (edge_point[0], edge_point[1]), (255, 0, 0), 2)  # draw blue line
                cv2.putText(transformed_img, str(round(self.calculate_angle(circle_center, edge_point))),(edge_point[0], edge_point[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        
        # map smalest angle to 0
        distance_to_0 = np.abs(np.array(angles) - 0)
        distance_to_360 = np.abs(np.array(angles) - 360)
        angles[np.argmin(np.minimum(distance_to_0, distance_to_360))] = 0

        cv2.imshow("Gefundene Randpunkte & Winkel", transformed_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return angles
    
    def transform_img(self, img):
        """
        Transforms an image so that the waypoint is visible from above.
        """

        # coordinates to transform
        tl = (600,1050)
        bl = (0, 1944)
        tr = (2050,1050)
        br = (2592,1944)

        if SHOW_IMAGES:
            tem_img = img
            cv2.circle(tem_img, tl, 5, (0,0,255), -1)
            cv2.circle(tem_img, bl, 5, (0,0,255), -1)
            cv2.circle(tem_img, tr, 5, (0,0,255), -1)
            cv2.circle(tem_img, br, 5, (0,0,255), -1)

            scale_percent = 15
            width = int(tem_img.shape[1] * scale_percent / 100)
            height = int(tem_img.shape[0] * scale_percent / 100)
            resized_img = cv2.resize(tem_img, (width, height), interpolation=cv2.INTER_AREA)

            cv2.imshow("Befor transformation", resized_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        # transform image
        pts1 = np.float32([tl, bl, tr, br])
        pts2 = np.float32([(0,0), (0,600), (600,0), (600,600)])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        transformed_img = cv2.warpPerspective(img, matrix, (600,600))

        if SHOW_IMAGES:
            cv2.imshow("After transformation", transformed_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return transformed_img

    def get_circle_center(self, img):
        # convert image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        gray_blurred = cv2.blur(gray, (3, 3))

        kernel = np.ones((5,5),np.uint8)
        eroded_img = cv2.morphologyEx(gray_blurred, cv2.MORPH_OPEN, kernel)

        detected_circles = cv2.HoughCircles(image = gray_blurred,  
                                            method = cv2.HOUGH_GRADIENT, 
                                            dp = 1, 
                                            minDist = 50, 
                                            param1 = 100, 
                                            param2 = 10, 
                                            minRadius = 10, 
                                            maxRadius = 500)
        
        if detected_circles is not None:
            if len(detected_circles) > 1:
                logger.warning("More than one waypoint was detected on the image!", detected_circles)

            detected_circles = np.uint16(np.around(detected_circles))

            for x, y, r in detected_circles[0, :]:
                logger.info(f"Circle detected on image with center point ({x}, {y})")

                if SHOW_IMAGES:
                    temp_img = img
                    cv2.circle(temp_img, (x, y), r, 70, thickness=5)

                    cv2.imshow("Detected Circle", temp_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                return (x, y)
        else:
            raise Exception("No circle found")

    def get_edge_points(self, img, circle_center):
        white_edge_pixles = [] # all white edge pixles
        height, width, _ = img.shape # image size

        # convert image to gray scale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # turns ever pixel black except defined range
        _, binary = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY)

        cv2.imshow("Gefundene Randpunkte & Winkel", binary)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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

        print(white_edge_pixles)

        if len(white_edge_pixles) > 1:
            #cluster_centers = self.testi(white_edge_pixles, circle_center)
            sse = []
            for k in range(1, min(5, len(white_edge_pixles))):
                kmeans = KMeans(n_clusters=k, n_init=10).fit(white_edge_pixles)
                sse.append(kmeans.inertia_)

            deltas = np.diff(sse)
            k_optimal = np.argmax(deltas) + 1

            kmeans = KMeans(n_clusters=k_optimal, n_init=20, max_iter=300, tol=1e-6, init='k-means++',).fit(white_edge_pixles)
            cluster_centers = kmeans.cluster_centers_.astype(int)
        else:
            cluster_centers = white_edge_pixles

        return cluster_centers

        if len(white_edge_pixles) > 1:
            kmeans = KMeans(n_clusters=min(5, len(white_edge_pixles)), n_init=10).fit(white_edge_pixles)
            edge_points = kmeans.cluster_centers_.astype(int)
        else:
            edge_points = white_edge_pixles

        return edge_points
    
    def calculate_angle(self, circle_center, edge_point):
        delta_y = edge_point[1] - circle_center[1]
        delta_x = edge_point[0] - circle_center[0]
        angle_rad = np.arctan2(-delta_x, delta_y)
        angle_deg = np.degrees(angle_rad)

        # ensure that the angle is between 0 and 360
        angle_deg = (angle_deg + 360) % 360
        logger.info(f"Found line on waypoint with angle: {angle_deg}")

        return angle_deg
    
    def testi(self, white_edge_points, circle_center):
        linien_toleranz_winkel = 5  # Toleranz für den Winkel zwischen Linien (in Grad)
        linien_toleranz_abstand = 10

        gruppen = defaultdict(list)
        zugeordnete = set()

        for i, punkt1 in enumerate(white_edge_points):
            if i in zugeordnete:
                continue
            
            winkel1 = self.calculate_angle(circle_center, punkt1)
            neue_gruppe = [punkt1]
            zugeordnete.add(i)
            gruppen[winkel1].append(punkt1)

            for j in range(i + 1, len(white_edge_points)):
                if j not in zugeordnete:
                    punkt2 = white_edge_points[j]
                    winkel2 = self.calculate_angle(circle_center, punkt2)

                    winkel_differenz = min(abs(winkel1 - winkel2), 360 - abs(winkel1 - winkel2))

                    if winkel_differenz < linien_toleranz_winkel:
                        # Prüfe zusätzlich auf räumliche Nähe, um sicherzustellen, dass es sich um die gleiche Linie handelt
                        distanz = np.sqrt((punkt1[0] - punkt2[0])**2 + (punkt1[1] - punkt2[1])**2)
                        if distanz < 20: # Passe diesen Wert nach Bedarf an
                            gruppen[winkel1].append(punkt2)
                            zugeordnete.add(j)

        # Zusammenführen von Gruppen mit sehr ähnlichen Winkeln
        final_gruppen = defaultdict(list)
        zugeordnete_winkel = set()
        for winkel1, gruppe1 in gruppen.items():
            if winkel1 in zugeordnete_winkel:
                continue
            final_gruppen[winkel1].extend(gruppe1)
            zugeordnete_winkel.add(winkel1)
            for winkel2, gruppe2 in gruppen.items():
                if winkel2 != winkel1 and winkel2 not in zugeordnete_winkel:
                    winkel_differenz = min(abs(winkel1 - winkel2), 360 - abs(winkel1 - winkel2))
                    if winkel_differenz < linien_toleranz_winkel * 1.5: # Etwas größere Toleranz beim Mergen
                        final_gruppen[winkel1].extend(gruppe2)
                        zugeordnete_winkel.add(winkel2)

        mittlere_punkte = []
        for gruppe in final_gruppen.values():
            if gruppe:
                koordinaten = np.array(gruppe)
                mittel_x = int(np.mean(koordinaten[:, 0]))
                mittel_y = int(np.mean(koordinaten[:, 1]))
                mittlere_punkte.append((mittel_x, mittel_y))

        return mittlere_punkte
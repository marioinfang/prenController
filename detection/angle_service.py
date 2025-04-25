import cv2
import numpy as np

from sklearn.cluster import DBSCAN
from utils.log_config import get_logger

logger = get_logger(__name__)

class AngleService():

    def __init__(self, show_images=False):
        logger.debug("Angle service inizialised")
        self.show_images = show_images

    def get_angles_of_waypoint(self, img):
        """
        Detects the angles of lines connected to the waypoint in the input image.

        Args:
            img (numpy.ndarray): The input image (NumPy array).

        Returns:
            list: A list of angles (in degrees) of the detected lines relative to the center of the waypoint.
                  The smallest angle is mapped to 0. Returns an empty list if no edge points are found.
        """
        angles = []

        transformed_img = self._transform_img(img)

        circle = self._get_circle(transformed_img)
        edge_points = self._get_edge_points(transformed_img, circle)

        temp_img = transformed_img
        for edge_point in edge_points:
            # Calculate the angle between the center of the circle and the edge point
            angles.append(self._calculate_angle((circle[0], circle[1]), edge_point))

            if self.show_images:
                cv2.circle(temp_img, (edge_point[0], edge_point[1]), 5, (0, 0, 255), -1)  # draw edge point on image
                cv2.line(temp_img, (circle[0], circle[1]), (edge_point[0], edge_point[1]), (255, 0, 0), 2)  # draw blue line
                cv2.putText(temp_img, str(round(self._calculate_angle((circle[0], circle[1]), edge_point))),(edge_point[0], edge_point[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        
        if self.show_images:
            cv2.imshow("Found angles", temp_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # Map the smallest angle to 0 for consistent orientation
        distance_to_0 = np.abs(np.array(angles) - 0)
        distance_to_360 = np.abs(np.array(angles) - 360)
        angles[np.argmin(np.minimum(distance_to_0, distance_to_360))] = 0

        # Claclulate the relative angles
        sorted_angles = angles.sort()

        differences = []
        for i in range(1, len(angles)):
            difference = (sorted_angles[i] - sorted_angles[i - 1]) % 360
            differences.append(difference)
             
        logger.info(f"Translated angles into differences {differences}")

        return angles
    
    def _transform_img(self, img):
        """
        Transforms an image to provide a top-down view of the waypoint area.

        This transformation uses perspective transformation based on predefined
        corner coordinates.

        Args:
            img (numpy.ndarray): The input image to be transformed.

        Returns:
            numpy.ndarray: The perspective-transformed image.
        """
        # Coordinates of the four corners in the original image
        tl = (494,1150)
        bl = (0, 2592)
        tr = (1450,1150)
        br = (1944,2592)

        if self.show_images:
            tem_img = img.copy()
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
        
        # Define the corresponding points in the transformed image
        pts1 = np.float32([tl, bl, tr, br])
        pts2 = np.float32([(0,0), (0,600), (300,0), (300,600)])

        # Get the perspective transform matrix
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        # Apply the perspective transformation to the image
        transformed_img = cv2.warpPerspective(img, matrix, (300,600))

        if self.show_images:
            cv2.imshow("After transformation", transformed_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return transformed_img

    def _get_circle(self, img):
        """
        Detects a circular waypoint in the image using the Hough Circle Transform.

        Args:
            img (numpy.ndarray): The input image to search for a circle.

        Returns:
            tuple: A tuple containing the (x, y) coordinates of the circle's center and its radius (r).
                   Returns None if no circle is found.

        Raises:
            Exception: If no circle is detected in the image.
        """
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur to reduce noise
        gray_blurred = cv2.blur(gray, (3, 3))

        # Apply Hough Circle Transform to detect circles
        detected_circles = cv2.HoughCircles(image = gray_blurred,  
                                            method = cv2.HOUGH_GRADIENT, 
                                            dp = 1, 
                                            minDist = 50, 
                                            param1 = 100, 
                                            param2 = 10, 
                                            minRadius = 10, 
                                            maxRadius = 500)
        
        if detected_circles is not None:
            # Convert the circle parameters to integers
            detected_circles = np.uint16(np.around(detected_circles))

            if len(detected_circles) > 1:
                logger.warning("More than one waypoint was detected on the image!", detected_circles)

            for x, y, r in detected_circles[0, :]:
                logger.info(f"Circle detected on image with center point ({x}, {y})")

                if self.show_images:
                    temp_img = img
                    cv2.circle(temp_img, (x, y), r, 70, thickness=5)

                    cv2.imshow("Detected Circle", temp_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                return (x, y, r)
        else:
            raise Exception("No circle found")

    def _get_edge_points(self, img, circle):
        """
        Finds white points (potential edge points) around the detected circle
        in a thresholded binary image. Then, it clusters these points using DBSCAN
        to find the centers of the edge lines connected to the waypoint.

        Args:
            img (numpy.ndarray): The input image.
            circle (tuple): A tuple containing the (x, y) center and radius (r) of the detected circle.

        Returns:
            list: A list of (x, y) coordinates representing the center points of the detected edge lines.
                  Returns a list of all white points if clustering does not find significant clusters.
        """
        height, width, _ = img.shape # Get image dimensions

        # Convert the image to grayscale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Turns ever pixel black except defined range
        _, binary = cv2.threshold(gray_img, 180, 255, cv2.THRESH_BINARY)

        if self.show_images:
            cv2.imshow("Blacked picure", binary)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        white_points = []
        # Sample points around the circle's circumference
        for angle in range(360):
            theta = np.radians(angle)
            # Calculate the x and y coordinates of a point slightly outside the circle
            x = int(circle[0] + (circle[2] + 10) * np.cos(theta))
            y = int(circle[1] + (circle[2] + 10) * np.sin(theta))

            # Check if the point is within the image boundaries
            if 0 <= x < width and 0 <= y < height:
                # If the pixel at the sampled point is white (255), add it to the list
                if binary[y, x] == 255:
                    white_points.append((x, y))

        if self.show_images:
            temp_img = img.copy()
            for x, y in white_points:
                cv2.circle(temp_img, (x, y), 3, (0, 255, 0), -1)
            cv2.imshow("White Points on Circle", temp_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # Cluster the white points using DBSCAN to find the centers of potential lines
        if len(white_points) > 1:
            clustering = DBSCAN(eps=10, min_samples=3).fit(white_points)
            labels = clustering.labels_

            clusters = []
            # Calculate the center of each cluster (excluding noise points labeled -1).
            for label in set(labels):
                if label == -1:
                    continue
                cluster_points = [white_points[i] for i in range(len(labels)) if labels[i] == label]
                cluster_center = np.mean(cluster_points, axis=0)
                print(cluster_center.astype(int))
                clusters.append(cluster_center.astype(int))

            return clusters
        else:
            return white_points
    
    def _calculate_angle(self, circle_center, edge_point):
        """
        Calculates the angle (in degrees) of a line formed by the center of the
        circle and an edge point relative to the positive y-axis (upwards).

        Args:
            circle_center (tuple): The (x, y) coordinates of the circle's center.
            edge_point (tuple): The (x, y) coordinates of the edge point.

        Returns:
            float: The angle in degrees, ranging from 0 to 360.
        """
        delta_y = edge_point[1] - circle_center[1]
        delta_x = edge_point[0] - circle_center[0]
        # Calculate the angle in radians using arctan2
        angle_rad = np.arctan2(-delta_x, delta_y)
        # Convert the angle from radians to degrees
        angle_deg = np.degrees(angle_rad)

        # Ensure the angle is within the range [0, 360]
        angle_deg = (angle_deg + 360) % 360
        logger.info(f"Found line on waypoint with angle: {angle_deg}")

        return angle_deg
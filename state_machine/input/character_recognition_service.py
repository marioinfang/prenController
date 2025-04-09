#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract
import sys
import os

from utils.log_config import get_logger

logger = get_logger(__name__)

def _whiten_background_around_circle(image, radius_scale=0.9, debug=False):
    """
    Detect a circle using HoughCircles, then shrink the detected radius by radius_scale.
    Set every pixel outside the adjusted circle to white.

    This isolates the letter within the circle even if extraneous white bars are attached.
    """
    # Convert to grayscale and apply a median blur for better circle detection.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)

    # Detect circles using Hough Circle Transform.
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2,
                               minDist=50, param1=50, param2=30,
                               minRadius=0, maxRadius=0)

    if circles is not None:
        # Use the first detected circle.
        circles = np.round(circles[0, :]).astype("int")
        x, y, r = circles[0]
        # Adjust the radius according to the scale factor.
        r = int(r * radius_scale)
        if debug:
            logger.info(f"Detected circle: center=({x}, {y}), original radius={circles[0][2]}, adjusted radius={r}")

        # Create a mask with a white circle (value 255) of the adjusted radius.
        mask = np.zeros(gray.shape, dtype="uint8")
        cv2.circle(mask, (x, y), r, 255, -1)

        # Set pixels outside the circle to white.
        output = image.copy()
        output[mask == 0] = [255, 255, 255]

        if debug:
            cv2.imwrite("debug_whitened.png", output)
            logger.info("Whitened image saved as debug_whitened.png")
        return output
    else:
        if debug:
            logger.info("No circle detected; using the original image.")
        return image

def _preprocess_image(image, debug=False):
    """
    Convert the image to grayscale, blur it, apply Otsu thresholding,
    apply morphological closing to strengthen letter features,
    and invert the result so that the text appears as black on a white background.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blurred, 0, 255,
                              cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Apply morphological closing to join any broken parts of the letter B
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    processed = cv2.bitwise_not(closed)

    if debug:
        cv2.imwrite("debug_preprocessed.png", processed)
        print("Preprocessed image saved as debug_preprocessed.png")
    return processed

def _rotate_image(image, angle):
    """
    Rotate the image by a specified angle.
    """
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             flags=cv2.INTER_CUBIC,
                             borderMode=cv2.BORDER_REPLICATE)
    return rotated

def _ocr_on_image(image, config):
    """
    Run Tesseract OCR on the image with the given configuration.
    """
    result = pytesseract.image_to_string(image, config=config)
    return result.strip()

def _brute_force_rotate(image, debug=False):
    """
    Resize the image for better OCR accuracy, rotate it in 30° increments,
    run OCR on each rotated version, and collect the results.
    """
    # Resize image (scale up) to improve OCR.
    scale_factor = 4
    h, w = image.shape[:2]
    resized = cv2.resize(image, (w * scale_factor, h * scale_factor),
                         interpolation=cv2.INTER_CUBIC)

    # Configure Tesseract to only consider the characters A, B, and C.
    config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=ABC'
    results = {}

    for angle in range(0, 360, 15):
        rotated = _rotate_image(resized, angle)
        result = _ocr_on_image(rotated, config)
        results[angle] = result
        if debug:
            logger.info(f"Angle {angle}° -> OCR result: '{result}'")
            cv2.imwrite(f"debug_rotated_{angle}.png", rotated)
    return results

def process_image(image_path, debug=False):
    """
    Read the image, whiten the background outside the detected circle using an adjusted radius,
    preprocess the image for OCR, perform brute-force rotation OCR,
    and return the recognized character if it is A, B, or C.
    """
    if not os.path.exists(image_path):
        logger.info("Error: Image file not found.")
        sys.exit(1)

    image = cv2.imread(image_path)
    if image is None:
        logger.info("Error: Failed to load image.")
        sys.exit(1)

    # Whiten everything outside the detected circle using the adjusted radius.
    whitened = _whiten_background_around_circle(image, radius_scale=0.8, debug=debug)

    # Preprocess the image for OCR.
    processed = _preprocess_image(whitened, debug=debug)

    # Rotate the image in fixed increments and get OCR results.
    results = _brute_force_rotate(processed, debug=debug)

    # Return the first valid OCR result that is 'A', 'B', or 'C'.
    for angle, res in results.items():
        if res in ['A', 'B', 'C']:
            logger.info(f"Valid OCR detected at angle {angle}°: {res}")
            return res

    logger.info("No valid character detected; returning empty.")
    return ""
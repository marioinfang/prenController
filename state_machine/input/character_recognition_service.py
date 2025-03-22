import cv2
import easyocr

def process_image(image_path):
    reader = easyocr.Reader(['en'])

    valid_letters = {"A", "B", "C"}

    image = cv2.imread(image_path)

    # OCR on original image
    result_original = reader.readtext(image, detail=0)
    detected_original = [text.strip().upper() for text in result_original if text.strip().upper() in valid_letters]

    # OCR on flipped image
    flipped = cv2.rotate(image, cv2.ROTATE_180)
    result_flipped = reader.readtext(flipped, detail=0)
    detected_flipped = [text.strip().upper() for text in result_flipped if text.strip().upper() in valid_letters]

    # Decide which result to use
    if detected_original:
        print("Detected from original orientation:", detected_original)
        return detected_original[0]  # Return first valid letter
    elif detected_flipped:
        print("Detected from flipped orientation:", detected_flipped)
        return detected_flipped[0]
    else:
        print("No valid letter (A, B, or C) detected.")
        return None

if __name__ == "__main__":
    extracted_text = process_image("images/test_image_a_flipped.jpeg")
    print("Extracted Text:", extracted_text)
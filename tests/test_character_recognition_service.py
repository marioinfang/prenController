from unittest import TestCase
from state_machine.input.character_recognition_service import process_image

class TestCharacterRecognition(TestCase):
    base_image_path = "images"

    def test_letter_A(self):
        for i in range(1, 9):  # A_1.jpeg to A_8.jpeg
            image_path = f"{self.base_image_path}/letter_A/A_{i}.jpeg"
            with self.subTest(image=image_path):
                result = process_image(image_path)
                self.assertEqual(result, "A", f"Expected 'A' but got '{result}' for {image_path}")

    def test_letter_BB(self):
            image_path = f"{self.base_image_path}/letter_B/B_{2}.jpeg"
            result = process_image(image_path)
            self.assertEqual(result, "B", f"Expected 'B' but got '{result}' for {image_path}")

    def test_letter_AA(self):
        image_path = f"{self.base_image_path}/letter_A/A_{6}.jpeg"
        result = process_image(image_path)
        self.assertEqual(result, "A", f"Expected 'A' but got '{result}' for {image_path}")


    def test_letter_B(self):
        for i in range(1, 9):  # Assuming B images: B_1.jpeg to B_8.jpeg
            image_path = f"{self.base_image_path}/letter_B/B_{i}.jpeg"
            with self.subTest(image=image_path):
                result = process_image(image_path)
                self.assertEqual(result, "B", f"Expected 'B' but got '{result}' for {image_path}")

    def test_letter_C(self):
        for i in range(1, 9):  # Assuming C images: C_1.jpeg to C_8.jpeg
            image_path = f"{self.base_image_path}/letter_C/C_{i}.jpeg"
            with self.subTest(image=image_path):
                result = process_image(image_path)
                self.assertEqual(result, "C", f"Expected 'C' but got '{result}' for {image_path}")

    def test_base_node(self):
        image_path = f"{self.base_image_path}/letter_template/base.jpeg"
        result = process_image(image_path)
        self.assertEqual(result, "", f"Expected '' but got '{result}' for {image_path}")


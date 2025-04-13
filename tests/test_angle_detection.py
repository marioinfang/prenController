from unittest import TestCase
from detection.angle_service import AngleService

class TestAngleDetection(TestCase):
    base_image_path = "images"

    def test_angles_0_90_180_270(self):
        image_path = f"{self.base_image_path}/waypoint/angle_0_90_180_270.png"
        with self.subTest(image=image_path):
            result = AngleService.get_angles_of_waypoint(image_path)
            self.assertEqual(len(result), 4, msg=f"Expected 4 angles but got {len(result)}")
            self.assertAlmostEqual(result[0], 0, delta=0, msg=f"Expected angle of 0 but got {result[0]}")
            self.assertAlmostEqual(result[1], 90, delta=5, msg=f"Expected angle of 90 but got {result[1]}")
            self.assertAlmostEqual(result[2], 180, delta=5, msg=f"Expected angle of 180 but got {result[2]}")
            self.assertAlmostEqual(result[3], 270, delta=5, msg=f"Expected angle of 270 but got {result[3]}")

    def test_angles_0(self):
        image_path = f"{self.base_image_path}/waypoint/angle_0.png"
        with self.subTest(image=image_path):
            result = AngleService.get_angles_of_waypoint(image_path)
            self.assertEqual(len(result), 1, msg=f"Expected 1 angles but got {len(result)}")
            self.assertAlmostEqual(result[0], 0, delta=0, msg=f"Expected angle of 0 but got {result[0]}")
                
    def test_angles_0_135_225(self):
        image_path = f"{self.base_image_path}/waypoint/angle_0_135_225.png"
        with self.subTest(image=image_path):
            result = AngleService.get_angles_of_waypoint(image_path)
            self.assertEqual(len(result), 3, msg=f"Expected 3 angles but got {len(result)}")
            self.assertAlmostEqual(result[0], 0, delta=0, msg=f"Expected angle of 0 but got {result[0]}")
            self.assertAlmostEqual(result[1], 135, delta=5, msg=f"Expected angle of 135 but got {result[1]}")
            self.assertAlmostEqual(result[2], 225, delta=5, msg=f"Expected angle of 225 but got {result[2]}")

    def test_angles_0_30(self):
        image_path = f"{self.base_image_path}/waypoint/angle_0_30.png"
        with self.subTest(image=image_path):
            result = AngleService.get_angles_of_waypoint(image_path)
            self.assertEqual(len(result), 2, msg=f"Expected 2 angles but got {len(result)}")
            self.assertAlmostEqual(result[0], 0, delta=0, msg=f"Expected angle of 0 but got {result[0]}")
            self.assertAlmostEqual(result[1], 30, delta=5, msg=f"Expected angle of 30 but got {result[1]}")

    def test_angles_0_30_180_250_320(self):
        image_path = f"{self.base_image_path}/waypoint/angle_0_30_180_250_320.png"
        with self.subTest(image=image_path):
            result = AngleService.get_angles_of_waypoint(image_path)
            self.assertEqual(len(result), 5, msg=f"Expected 5 angles but got {len(result)}")
            self.assertAlmostEqual(result[0], 0, delta=0, msg=f"Expected angle of 0 but got {result[0]}")
            self.assertAlmostEqual(result[1], 30, delta=5, msg=f"Expected angle of 30 but got {result[1]}")
            self.assertAlmostEqual(result[2], 180, delta=5, msg=f"Expected angle of 180 but got {result[2]}")
            self.assertAlmostEqual(result[3], 250, delta=5, msg=f"Expected angle of 250 but got {result[3]}")
            self.assertAlmostEqual(result[4], 320, delta=5, msg=f"Expected angle of 320 but got {result[4]}")

    def test_angles_no_waypoint(self):
        image_path = f"{self.base_image_path}/waypoint/angle_no_circle.png"
        with self.subTest(image=image_path):
            with self.assertRaises(Exception):
                AngleService.get_angles_of_waypoint(image_path)
            


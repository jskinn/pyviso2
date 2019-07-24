import unittest
import os
import numpy as np
from viso2 import VisualOdometryStereo, Stereo_parameters


class TestLibVisOStereoExecution(unittest.TestCase):

    def test_simple_trial_run(self):
        params = Stereo_parameters()

        # Camera calibration
        params.calib.f = 120
        params.calib.cu = 160
        params.calib.cv = 120
        params.base = 25

        # Actually run the system using mocked images
        subject = VisualOdometryStereo(params)
        
        num_frames = 50
        got_motion = False
        got_matches = False
        got_inliers = False
        for time in range(num_frames):
            left_frame, right_frame = create_frame(time / num_frames)
            subject.process_frame(left_frame, right_frame)
            motion = subject.getMotion()
            inliers = subject.getNumberOfInliers()
            matches = subject.getNumberOfMatches()

            # Prints, for visualization. Uncomment to see what it actually estimates.
            # print("Time {0}: {1} inliers, {2} matches".format(time, inliers, matches))
            # print(motion)

            # Convert the motion to a numpy array
            np_motion = np.zeros((4, 4))
            motion.toNumpy(np_motion)

            if time <= 0:
                # Should be no features and no motion after the first frame
                self.assertEqual(0, inliers)
                self.assertEqual(0, matches)
                self.assertTrue(np.array_equal(np.identity(4), np_motion))
            else:
                # Otherwise, there should be _some_ motion registered, sometime
                if inliers > 0:
                    got_inliers = True
                if matches > 0:
                    got_matches = True
                if not np.array_equal(np.identity(4), np_motion):
                    got_motion = True
        self.assertTrue(got_motion, msg="libviso did not estimate nonzero motion for any frame")
        self.assertTrue(got_inliers, msg="libviso did not have any inliers for any frame")
        self.assertTrue(got_matches, msg="libviso did not have any feature matches for any frame")


def create_frame(time):
    """
    Make a sequence of simple greyscale images with a number of various intensity grey rectangles.
    Does simple 3D projection to render the rectangles to the screen, giving us a test image sequence,
    from which libviso should be able to estimate motion (although not necessarily very well).
    """
    left_frame = np.zeros((240, 320), dtype=np.uint8)
    right_frame = np.zeros((240, 320), dtype=np.uint8)
    speed = 200
    baseline = 25
    f = left_frame.shape[1] / 2
    cx = left_frame.shape[1] / 2
    cy = left_frame.shape[0] / 2
    num_stars = 300
    z_values = [600 - idx * 2 - speed * time for idx in range(num_stars)]
    stars = [{
        'pos': (
            (127 * idx + 34 * idx * idx) % 400 - 200,
            (320 - 17 * idx + 7 * idx * idx) % 400 - 200,
            z_value
        ),
        'width': idx % 31 + 1,
        'height': idx % 27 + 1,
        'colour': 50 + (idx * 7 % 206)
    } for idx, z_value in enumerate(z_values) if z_value > 0]

    for star in stars:
        x, y, z = star['pos']

        left = int(np.round(f * ((x - star['width'] / 2) / z) + cx))
        right = int(np.round(f * ((x + star['width'] / 2) / z) + cx))

        top = int(np.round(f * ((y - star['height'] / 2) / z) + cy))
        bottom = int(np.round(f * ((y + star['height'] / 2) / z) + cy))

        left = max(0, min(left_frame.shape[1], left))
        right = max(0, min(left_frame.shape[1], right))
        top = max(0, min(left_frame.shape[0], top))
        bottom = max(0, min(left_frame.shape[0], bottom))

        left_frame[top:bottom, left:right] = star['colour']

        left = int(np.round(f * ((x + baseline - star['width'] / 2) / z) + cx))
        right = int(np.round(f * ((x + baseline + star['width'] / 2) / z) + cx))

        left = max(0, min(left_frame.shape[1], left))
        right = max(0, min(left_frame.shape[1], right))

        right_frame[top:bottom, left:right] = star['colour']
    return left_frame, right_frame
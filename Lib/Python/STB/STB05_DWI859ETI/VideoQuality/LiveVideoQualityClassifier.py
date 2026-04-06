# import cv2
# import numpy as np
# from skimage.metrics import structural_similarity as ssim
# from robot.api.deco import keyword

# class LiveVideoQualityClassifier:

#     @keyword("Classify Live Video Quality")
#     def classify_live_video_quality(self, port="/dev/video0", duration=20, iterations=5):
#         results = []

#         for i in range(iterations):
#             cap = cv2.VideoCapture(port)
#             if not cap.isOpened():
#                 raise Exception(f"Cannot open video source: {port}")

#             fps = cap.get(cv2.CAP_PROP_FPS)
#             if fps == 0:
#                 fps = 25
#             frame_limit = int(fps * duration)

#             blurry = 0
#             stddev_glitch = 0
#             brightness_issue = 0
#             prev_img = None
#             prev_blur = None
#             prev_brightness = None
#             prev_stddev = None
#             blur_streak = 0
#             bright_streak = 0
#             stddev_streak = 0

#             for _ in range(frame_limit):
#                 ret, frame = cap.read()
#                 if not ret or frame is None:
#                     continue

#                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                 blur = cv2.Laplacian(gray, cv2.CV_64F).var()
#                 brightness = np.mean(gray)
#                 stddev = np.std(gray)

#                 if prev_blur is not None and abs(blur - prev_blur) < 10:
#                     blur_streak += 1
#                 else:
#                     blur_streak = 0

#                 if prev_brightness is not None and abs(brightness - prev_brightness) < 5:
#                     bright_streak += 1
#                 else:
#                     bright_streak = 0

#                 if prev_stddev is not None and abs(stddev - prev_stddev) < 5:
#                     stddev_streak += 1
#                 else:
#                     stddev_streak = 0

#                 if blur_streak >= 2:
#                     blurry += 1
#                 if stddev_streak >= 2:
#                     stddev_glitch += 1
#                 if bright_streak >= 2:
#                     brightness_issue += 1

#                 prev_img = gray
#                 prev_blur = blur
#                 prev_brightness = brightness
#                 prev_stddev = stddev

#             cap.release()

#             if blurry <= 20 and stddev_glitch >= 300 and brightness_issue >= 300:
#                 label = "Bad"
#             elif blurry >= 80 and stddev_glitch >= 500 and brightness_issue >= 500:
#                 label = "Clear"
#             else:
#                 label = "Middle"
#             results.append({
#                 "iteration": i + 1,
#                 "blurry": blurry,
#                 "stddev_glitch": stddev_glitch,
#                 "brightness_issue": brightness_issue,
#                 "label": label
#             })

#         # Print summary
#         for r in results:
#             print(f"\n🎬 Iteration {r['iteration']}:")
#             print(f"   Blurry frames: {r['blurry']}")
#             print(f"   Stddev glitches: {r['stddev_glitch']}")
#             print(f"   Brightness issues: {r['brightness_issue']}")
#             print(f"   ➤ Classified as: {r['label']}")

#         return results

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import time
from robot.api.deco import keyword

# === CONFIG ===
VIDEO_SOURCE = "/dev/video0"
DURATION_SECONDS = 20
SSIM_THRESHOLD = 0.90
BLUR_TOLERANCE = 10.0
STDDEV_TOLERANCE = 5.0
BRIGHTNESS_TOLERANCE = 5.0
BLACK_WHITE_RATIO = 0.80
CONSECUTIVE_STREAK_THRESHOLD = 2

class LiveVideoQualityClassifier:

    def is_black_or_white(self, img, threshold_ratio=BLACK_WHITE_RATIO):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        total_pixels = gray.size
        black_pixels = np.sum(gray <= 10)
        white_pixels = np.sum(gray >= 245)
        if black_pixels / total_pixels >= threshold_ratio:
            return True, "mostly black"
        elif white_pixels / total_pixels >= threshold_ratio:
            return True, "mostly white"
        return False, None

    def is_consistent(self, val1, val2, tolerance):
        return abs(val1 - val2) < tolerance

    def analyze_live_video(self, source, duration):
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print(f"❌ Unable to open video source: {source}")
            return None

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 25
        frame_limit = int(fps * duration)

        total_frames = 0
        black_white_count = 0
        blur_count = 0
        stddev_count = 0
        brightness_count = 0
        ssim_freeze_count = 0

        prev_img = None
        prev_blur = None
        prev_brightness = None
        prev_stddev = None
        blur_streak = 0
        bright_streak = 0
        stddev_streak = 0
        ssim_streak = 0
        bw_streak = 0

        print(f"\n🎥 Capturing live video from {source} for {duration} seconds...\n")
        start_time = time.time()

        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            total_frames += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.Laplacian(gray, cv2.CV_64F).var()
            brightness = np.mean(gray)
            stddev = np.std(gray)
            bw_match, _ = self.is_black_or_white(frame)

            if bw_match:
                bw_streak += 1
            else:
                bw_streak = 0

            if prev_blur is not None and self.is_consistent(blur, prev_blur, BLUR_TOLERANCE):
                blur_streak += 1
            else:
                blur_streak = 0

            if prev_brightness is not None and self.is_consistent(brightness, prev_brightness, BRIGHTNESS_TOLERANCE):
                bright_streak += 1
            else:
                bright_streak = 0

            if prev_stddev is not None and self.is_consistent(stddev, prev_stddev, STDDEV_TOLERANCE):
                stddev_streak += 1
            else:
                stddev_streak = 0

            if prev_img is not None:
                try:
                    curr = cv2.resize(gray, (256, 256))
                    prev = cv2.resize(prev_img, (256, 256))
                    score, _ = ssim(curr, prev, full=True)
                    if score > SSIM_THRESHOLD:
                        ssim_streak += 1
                    else:
                        ssim_streak = 0
                except:
                    ssim_streak = 0

            if bw_streak >= CONSECUTIVE_STREAK_THRESHOLD:
                black_white_count += 1
            elif blur_streak >= CONSECUTIVE_STREAK_THRESHOLD:
                blur_count += 1
            elif stddev_streak >= CONSECUTIVE_STREAK_THRESHOLD:
                stddev_count += 1
            elif bright_streak >= CONSECUTIVE_STREAK_THRESHOLD:
                brightness_count += 1
            elif ssim_streak >= CONSECUTIVE_STREAK_THRESHOLD:
                ssim_freeze_count += 1

            prev_img = gray
            prev_blur = blur
            prev_brightness = brightness
            prev_stddev = stddev

        cap.release()

        print(f"\n📊 Summary of Live Video Analysis")
        print(f"   Total frames: {total_frames}")
        print(f"   Black/white anomalies: {black_white_count}")
        print(f"   Blurry anomalies: {blur_count}")
        print(f"   Stddev glitches: {stddev_count}")
        print(f"   Brightness issues: {brightness_count}")
        print(f"   Frozen (SSIM): {ssim_freeze_count}\n")

        return {
            "total_frames": total_frames,
            "black_white_anomalies": black_white_count,
            "blurry_anomalies": blur_count,
            "stddev_glitches": stddev_count,
            "brightness_issues": brightness_count,
            "frozen_ssim": ssim_freeze_count
        }

    @keyword("Classify Live Video Quality")
    def classify_live_video_quality(self, port="/dev/video0", duration=20, iterations=5):
        results = []
        for i in range(iterations):
            result = self.analyze_live_video(port, duration)
            if result:
                result["iteration"] = i + 1
                results.append(result)
        return results
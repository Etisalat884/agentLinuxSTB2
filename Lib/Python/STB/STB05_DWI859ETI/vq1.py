import cv2
import numpy as np
import time
from skimage.metrics import structural_similarity as ssim
import warnings
import sys

warnings.filterwarnings("ignore", message=".*defaulting to CPU.*")
sys.stderr = sys.stdout  # Redirect stderr to stdout

# === CONFIG ===
SSIM_THRESHOLD = 0.90
BLUR_TOLERANCE = 10.0
STDDEV_TOLERANCE = 5.0
BRIGHTNESS_TOLERANCE = 4.0
BLACK_WHITE_RATIO = 0.80
CONSECUTIVE_STREAK_THRESHOLD = 2

# Thresholds
BLOCKING_THRESHOLD = 105.0
BANDING_THRESHOLD = 0.01
SSIM_FREEZE_THRESHOLD = 1
BRIGHTNESS_LIMIT = 5

class FullVideoQualityEvaluator:

    def is_black_or_white(self, img, threshold_ratio=BLACK_WHITE_RATIO):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        total_pixels = gray.size
        black_pixels = np.sum(gray <= 10)
        white_pixels = np.sum(gray >= 245)
        return (black_pixels / total_pixels >= threshold_ratio) or (white_pixels / total_pixels >= threshold_ratio)

    def is_consistent(self, val1, val2, tolerance):
        return abs(val1 - val2) < tolerance

    def calculate_blocking_rate(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        grad_mag = cv2.magnitude(grad_x, grad_y)
        _, thresholded = cv2.threshold(grad_mag, 30, 255, cv2.THRESH_BINARY)
        return np.sum(thresholded) / (thresholded.shape[0] * thresholded.shape[1])

    def calculate_banding_rate(self, frame):
        yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        y = yuv[:, :, 0]
        hist = cv2.calcHist([y], [0], None, [256], [0, 256])
        hist = hist / hist.sum()
        return np.sum(np.diff(hist.flatten())**2)

    def evaluate_full_video_quality(self, port="/dev/video0", duration=20):
        cap = cv2.VideoCapture(port)
        if not cap.isOpened():
            print(f"❌ Unable to open video source: {port}")
            print("Final Verdict: Script Error")
            return "Video Not Available"

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 25

        # Counters
        total_frames = 0
        black_white_count = 0
        blur_count = 0
        stddev_count = 0
        brightness_count = 0
        ssim_freeze_count = 0
        blocking_total = 0
        banding_total = 0

        # Trackers
        prev_img = None
        prev_blur = None
        prev_brightness = None
        prev_stddev = None
        blur_streak = 0
        bright_streak = 0
        stddev_streak = 0
        ssim_streak = 0
        bw_streak = 0

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
            bw_match = self.is_black_or_white(frame)

            blocking_total += self.calculate_blocking_rate(frame)
            banding_total += self.calculate_banding_rate(frame)

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

        avg_blocking = blocking_total / total_frames if total_frames else 0
        avg_banding = banding_total / total_frames if total_frames else 0

        print(f"\n📊 Final Metrics:")
        print(f"   Total frames: {total_frames}")
        print(f"   Black/white anomalies: {black_white_count}")
        print(f"   Blurry anomalies: {blur_count}")
        print(f"   Stddev glitches: {stddev_count}")
        print(f"   Brightness issues: {brightness_count}")
        print(f"   Frozen (SSIM): {ssim_freeze_count}")
        print(f"   Blocking Rate: {avg_blocking:.5f}")
        print(f"   Banding Rate: {avg_banding:.5f}")

        bad_flags = 0
        if avg_blocking > BLOCKING_THRESHOLD:
            bad_flags += 1
        if avg_banding > BANDING_THRESHOLD:
            bad_flags += 1
        if ssim_freeze_count >= SSIM_FREEZE_THRESHOLD:
            bad_flags += 1
        if brightness_count > BRIGHTNESS_LIMIT:
            bad_flags += 1
        if black_white_count > 5:
            bad_flags += 1
        if stddev_count > 475:
            bad_flags += 1
        if stddev_count > 400 and brightness_count < 5 and BANDING_THRESHOLD > 0.01:
            bad_flags += 1
        if BANDING_THRESHOLD > 0.04 and BLOCKING_THRESHOLD > 50:
            bad_flags += 1
        if bad_flags > 1:
            verdict = "Bad Quality Video"
            reason = "Multiple quality thresholds exceeded"
        elif bad_flags == 0:
            verdict = "Good Quality Video"
            reason = "Minor issue detected but overall quality acceptable"
        else:
            verdict = "Good Quality Video"
            reason = "All metrics within acceptable range"

        print(f"\n🎬 Final Verdict: {verdict}")
        print(f"📌 Reason: {reason}")
        print(f"📌 Verdict Factors → Blocking: {avg_blocking:.2f}, Banding: {avg_banding:.5f}, Brightness: {brightness_count}, SSIM Freeze: {ssim_freeze_count}, BW: {black_white_count}")
        return verdict

if __name__ == "__main__":
    try:
        evaluator = FullVideoQualityEvaluator()
        verdict = evaluator.evaluate_full_video_quality(port="/dev/video0", duration=20)
    except Exception as e:
        print(f"\n❌ Script crashed: {e}")
        print("Final Verdict: Script Error")
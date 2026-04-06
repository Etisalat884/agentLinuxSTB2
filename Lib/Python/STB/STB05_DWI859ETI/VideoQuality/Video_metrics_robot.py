import cv2
import numpy as np
import warnings

warnings.filterwarnings("ignore", message=".*defaulting to CPU.*")

def calculate_blocking_rate(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray_frame, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray_frame, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = cv2.magnitude(grad_x, grad_y)
    _, thresholded_grad = cv2.threshold(grad_mag, 30, 255, cv2.THRESH_BINARY)
    blocking_pixels = np.sum(thresholded_grad) / (thresholded_grad.shape[0] * thresholded_grad.shape[1])
    return blocking_pixels

def calculate_banding_rate(frame):
    yuv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    y_channel = yuv_frame[:, :, 0]
    hist = cv2.calcHist([y_channel], [0], None, [256], [0, 256])
    hist = hist / hist.sum()
    banding_score = np.sum(np.diff(hist.flatten())**2)
    return banding_score

def video_metrics(video_source, duration_seconds=20):
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        return 0, 0

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        cap.release()
        return 0, 0

    frame_limit = int(fps * duration_seconds)
    blocking_rate_total = 0
    banding_rate_total = 0
    frame_count = 0

    while frame_count < frame_limit:
        ret, frame = cap.read()
        if not ret:
            break

        blocking_rate_total += calculate_blocking_rate(frame)
        banding_rate_total += calculate_banding_rate(frame)
        frame_count += 1

    cap.release()

    if frame_count == 0:
        return 0, 0

    avg_blocking_rate = blocking_rate_total / frame_count
    avg_banding_rate = banding_rate_total / frame_count

    return avg_blocking_rate, avg_banding_rate
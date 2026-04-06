import cv2
import numpy as np
from datetime import datetime
import subprocess
import logging
import os

logging.basicConfig(level=logging.INFO)

def get_current_datetime():
    return datetime.now().strftime("%Y%m%d%H_%M_%S")

def captureImage(port, imgname):
    command = [
        "ffmpeg", "-y", "-f", "v4l2", "-input_format", "yuyv422",
        "-video_size", "1280x720",
        "-i", f"/dev/video{port}", "-vframes", "1", imgname
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def preprocess_for_match(image, prefix, debug_folder):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(debug_folder, f"{prefix}_gray.png"), gray)

    # Optional light blur
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    cv2.imwrite(os.path.join(debug_folder, f"{prefix}_blurred.png"), blurred)

    return blurred





def verifyimage(port, small_image_name):
    capture_image_path = '/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Images/Reference/Capture.png'
    small_image_path = f'/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Images/{small_image_name}.png'
    #     capture_image_path = '/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Images/Reference/Capture.png'
#     small_image_path = '/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Images/' + small_image_path + '.png'
    # Debug folder setup
    debug_folder = '/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Lib/Python/STB/agentLinuxSTB2/debug'
    os.makedirs(debug_folder, exist_ok=True)
    timestamp = get_current_datetime()

    # Capture new image
    captureImage(port, capture_image_path)

    # Load both images
    capture_image = cv2.imread(capture_image_path)
    small_image = cv2.imread(small_image_path)

    if capture_image is None or small_image is None:
        raise ValueError("Failed to load one or both images.")

    # Save raw inputs for debugging
    cv2.imwrite(os.path.join(debug_folder, f"{timestamp}_capture.png"), capture_image)
    cv2.imwrite(os.path.join(debug_folder, f"{timestamp}_reference.png"), small_image)

    # Preprocess both
    capture_gray = preprocess_for_match(capture_image,"capture" ,debug_folder)
    small_gray = preprocess_for_match(small_image,"reference" ,debug_folder)

    # Match template
    result = cv2.matchTemplate(capture_gray, small_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    threshold = 0.20
    logging.info(f"Match confidence: {max_val:.4f}")

    if max_val >= threshold:
        h, w = small_gray.shape
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(capture_image, top_left, bottom_right, (0, 255, 0), 2)
        # cv2.imshow('Result', capture_image)
        
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite(os.path.join(debug_folder, f"{timestamp}_matched_result.png"), capture_image)
        return True
    else:
        return False

def displayimage(port, imgname):
    path = imgname
    captureImage(port, path)
    return path
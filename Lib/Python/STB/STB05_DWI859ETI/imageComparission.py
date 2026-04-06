import cv2
import subprocess
from skimage.metrics import structural_similarity as ssim
import numpy as np

def captureImage(port, imgname):
    command = [
        "ffmpeg", "-y", "-f", "v4l2",
        "-input_format", "rgb24",
        "-video_size", "1920x1080",
        "-i", f"/dev/video{port}",
        "-vframes", "1",
        imgname
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def verify_image(port, reference_path, diff_path="/home/ltts/diff.png"):
    live_path = "/home/ltts/live.png"
    captureImage(port, live_path)

    img_live = cv2.imread(live_path)
    img_ref  = cv2.imread(reference_path)

    if img_live is None or img_ref is None:
        print("Error: Failed to load images")
        return False

    img_live_gray = cv2.cvtColor(img_live, cv2.COLOR_BGR2GRAY)
    img_ref_gray  = cv2.cvtColor(img_ref,  cv2.COLOR_BGR2GRAY)

    # Resize reference to match live
    img_ref_gray = cv2.resize(img_ref_gray, (img_live_gray.shape[1], img_live_gray.shape[0]))

    score, diff = ssim(img_live_gray, img_ref_gray, full=True)
    print("SSIM Score:", score)

    # Normalize diff to 0-255 for visualization
    diff = (diff * 255).astype(np.uint8)
    # Invert difference so differences are white
    diff_inv = cv2.bitwise_not(diff)

    # Convert single channel to BGR for saving
    diff_bgr = cv2.cvtColor(diff_inv, cv2.COLOR_GRAY2BGR)
    cv2.imwrite(diff_path, diff_bgr)

    if score > 0.65:
        print("Live image matches reference ✅")
        return True
    else:
        print("Live image does NOT match reference ❌")
        return False

if __name__ == "__main__":
    reference_img = "/home/ltts/frame2.png"
    verify_image(0, reference_img)

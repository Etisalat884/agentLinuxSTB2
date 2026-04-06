import cv2
import subprocess

def captureImage(port, imgname):
    """Capture a single frame from STB camera"""
    command = [
        "ffmpeg", "-y", "-f", "v4l2",
        "-input_format", "rgb24",        # match your STB format
        "-video_size", "1920x1080",      # match your STB resolution
        "-i", f"/dev/video{port}",
        "-vframes", "1", imgname
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def store_reference_roi(port, save_path, roi_center=None, roi_size=(200,100)):
    """Capture and store a reference ROI"""
    temp_path = "/home/ltts/live_temp.png"
    captureImage(port, temp_path)

    img = cv2.imread(temp_path)
    if img is None:
        print("Failed to capture image")
        return False

    # Default ROI center = screen center
    if roi_center is None:
        roi_center = (img.shape[1]//2, img.shape[0]//2)

    w, h = roi_size
    x_c, y_c = roi_center

    # Calculate ROI coordinates
    x1 = max(0, x_c - w//2)
    x2 = min(img.shape[1], x_c + w//2)
    y1 = max(0, y_c - h//2)
    y2 = min(img.shape[0], y_c + h//2)

    roi = img[y1:y2, x1:x2]
    cv2.imwrite(save_path, roi)
    print(f"Reference ROI saved to {save_path}")
    return True

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    store_reference_roi(
        port=0, 
        save_path="/home/ltts/reference_roi.png", 
        roi_center=None,      # center of the screen
        roi_size=(200,100)    # width x height of ROI
    )

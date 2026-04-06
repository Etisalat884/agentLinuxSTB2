import cv2
from PIL import Image
import numpy as np
import os
import subprocess
from matplotlib import pyplot as plt
import imagehash
from pathlib import Path
import os
import time
import time
import json
import pytesseract
from datetime import datetime, timedelta
# Get the base path dynamically, assuming script is inside LIB/PYTHON
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../Images"))  # Goes up to etisalatautomation/
REFERENCE_PATH = os.path.join(BASE_PATH, "Reference")

# Ensure the reference directory exists
os.makedirs(REFERENCE_PATH, exist_ok=True)

# Function to capture image using ffmpeg with 720p resolution
def capture_image_run(port=0, imgname="new_profile.jpg"):
    img_path = os.path.join(BASE_PATH, imgname)  # Save the captured image in BASE_PATH

    command = [
        "ffmpeg", "-y", "-f", "v4l2", "-input_format", "yuyv422",
        "-video_size", "1280x720",  # Set resolution to 720p
        "-i", f"/dev/video{port}", "-vframes", "1", img_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"Image saved as: {img_path}")
    return img_path

# Function to select and crop an image
def select_and_crop_image(image_path, cropped_name="cropped_image.jpg"):
    image = cv2.imread(image_path)
    print("Cropped Image Path:", image_path)
    if image is None:
        print("Error: Image not found.")
        return

    cropping = False
    x_start, y_start = -1, -1
    roi_image = None

    def select_roi(event, x, y, flags, param):
        nonlocal cropping, x_start, y_start, roi_image

        if event == cv2.EVENT_LBUTTONDOWN:
            cropping = True
            x_start, y_start = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            if cropping:
                temp_image = image.copy()
                cv2.rectangle(temp_image, (x_start, y_start), (x, y), (0, 255, 0), 2)
                cv2.imshow("Select ROI", temp_image)

        elif event == cv2.EVENT_LBUTTONUP:
            cropping = False
            x_end, y_end = x, y
            roi_image = image[y_start:y_end, x_start:x_end]
            print("x1:",x_start)
            print("x2:",x_end)
            print("y1:",y_start)
            print("y2:",y_end)
            if roi_image is not None and roi_image.shape[0] > 0 and roi_image.shape[1] > 0:
                cropped_path = os.path.join(REFERENCE_PATH, cropped_name)  # Save cropped image in REFERENCE_PATH
                cv2.imwrite(cropped_path, roi_image)
                print(f"Cropped image saved as: {cropped_path}")
                cv2.imshow("Cropped Image", roi_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    cv2.imshow("Select ROI", image)
    cv2.setMouseCallback("Select ROI", select_roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()






def capture_image(port, imgname):
    command = [
        "ffmpeg", "-y", "-f", "v4l2", "-input_format", "yuyv422",
        "-video_size", "1280x720",  # Set resolution to 720p
        "-i", f"/dev/video{port}", "-vframes", "1", imgname
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Function to perform template matching
def tempMatch(port, image1, image2):
    # base_path = "/home/ltts/Pictures/etisalatautomation/Images/"
    base_path = BASE_PATH
    path1 = os.path.join(base_path, f"{image1}.jpg")  # Captured image path
    path2 = os.path.join(base_path, "Reference", f"{image2}.jpg")  # Template image path
    
    # Capture an image from the camera
    capture_image(port, path1)

    # Load images
    template = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)
    img_rgb = cv2.imread(path1)

    if template is None:
        print(f"Error: Reference image '{image2}.jpg' not found.")
        return False

    if img_rgb is None:
        print(f"Error: Captured image '{image1}.jpg' not found.")
        return False

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    height, width = template.shape[:2]

    # Perform template matching
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    # Get the best match location
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Define threshold for matching
    threshold = 0.87
    print(f"Best match confidence: {max_val:.2f}")

    if max_val >= threshold:
        print(f"✅ Template match found in '{image1}.jpg'!")

        # Draw a rectangle at the best match location
        top_left = max_loc
        bottom_right = (top_left[0] + width, top_left[1] + height)
        cv2.rectangle(img_rgb, top_left, bottom_right, (0, 255, 0), 2)

        matched_img_path = os.path.join(base_path, f"Matched_{image1}.jpg")
        cv2.imwrite(matched_img_path, img_rgb)  # Save the matched image
        print(f"💾 Matched image saved as: {matched_img_path}")

        # Display the image with the matched template rectangle in real time
        # cv2.imshow("Matched Template", img_rgb)
        cv2.waitKey(0)  # Wait for a key press before closing the window
        cv2.destroyAllWindows()

        return True
    else:
        print("❌ No matched image found.")
        return False


# Capture an image and crop it
def capture_crop(crop_img_name):
    port = 0  # Change this if your camera is on a different port
    image_path = capture_image_run(port, "captured.jpg")  # Capture image with 720p resolution
    select_and_crop_image(image_path, crop_img_name+".jpg")  # Crop and save in the Reference folder















# capture_crop("Speaker")
# print(tempMatch(0, "comp_pause", "ref_pause"))





def get_crop_coordinates(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return None

    coords = {}

    def select_roi(event, x, y, flags, param):
        nonlocal coords, cropping, x_start, y_start

        if event == cv2.EVENT_LBUTTONDOWN:
            cropping = True
            x_start, y_start = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            if cropping:
                temp_image = image.copy()
                cv2.rectangle(temp_image, (x_start, y_start), (x, y), (255, 0, 0), 2)
                cv2.imshow("Get Coordinates", temp_image)

        elif event == cv2.EVENT_LBUTTONUP:
            cropping = False
            x_end, y_end = x, y
            coords = {
                "x1": min(x_start, x_end),
                "y1": min(y_start, y_end),
                "x2": max(x_start, x_end),
                "y2": max(y_start, y_end)
            }
            print("🧭 Coordinates:", coords)
            cv2.rectangle(image, (coords["x1"], coords["y1"]), (coords["x2"], coords["y2"]), (0, 255, 0), 2)
            cv2.imshow("Get Coordinates", image)

    cropping = False
    x_start, y_start = -1, -1

    cv2.imshow("Get Coordinates", image)
    cv2.setMouseCallback("Get Coordinates", select_roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return coords


def crop_with_coordinates_from_hdmi(coords, port=3, save_name="final_crop.jpg"):
    temp_capture_path = os.path.join(BASE_PATH, "temp_crop.jpg")
    capture_image_run(port, "temp_crop.jpg")

    image = cv2.imread(temp_capture_path)
    if image is None:
        print("Error: HDMI image not found.")
        return

    x1, y1, x2, y2 = coords["x1"], coords["y1"], coords["x2"], coords["y2"]
    cropped_img = image[y1:y2, x1:x2]

    if cropped_img.size == 0:
        print("Error: Empty cropped region.")
        return

    cropped_path = os.path.join(REFERENCE_PATH, save_name)
    cv2.imwrite(cropped_path, cropped_img)
    print(f"✅ Cropped HDMI image saved at: {cropped_path}")
    cv2.imshow("HDMI Cropped", cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()












# hdmi_image_path = capture_image_run(3, "capture_for_roi.jpg")
# coords = get_crop_coordinates(hdmi_image_path)
# if coords:
#     crop_with_coordinates_from_hdmi(coords, port=3, save_name="roi_hdmi_crop.jpg")





def crop_by_cord(x1,y1,x2,y2):
    path1 = 'D:/JC_4_Agent_4/agent4dut2/workspace/Appletv/Example/test.jpg'
    capture_image(2,path1)
    img = Image.open('D:/JC_5_Agent_8/agent8dut2/workspace/Appletv/Example/test.jpg')
    crop_img = img.crop((x1,y1,x2,y2))
    crop_img.save('D:/JC_5_Agent_8/agent8dut2/workspace/Appletv/Example/test_cropped.jpg')


def convert_image_time_text(port, c1, c2, c3, c4, img_name):
    capture_runFHD(port,c1, c2, c3, c4, img_name)
    time.sleep(2)
    img_name = img_name
    path = '/home/user/JC_5_Agent_8/agent8dut4/workspace/Comcast/IMAGES/Reference/'+img_name+'.jpg'
    # path = preprocess_image(path)
    img = Image.open(path)
    text = pytesseract.image_to_string(img, config=" --psm 6")
    print(text)
    return text

def test_image_to_text():
    time.sleep(3)
    img_name = 'CBS_News_Titles'
    path = '/home/user/JC_5_Agent_8/agent8dut4/workspace/Comcast/IMAGES/Reference/'+img_name+'.jpg'
    path = preprocess_image(path)
    img = Image.open(path)
    text = pytesseract.image_to_string(img, config=" --psm 6")
    print(text)
    return text

def test_image_to_texts():
    time.sleep(3)
    img_name = 'Add_New'
    path = '/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Images/Reference/'+img_name+'.jpg'
    path = preprocess_image(path)
    img = Image.open(path)
    text = pytesseract.image_to_string(img, config=" --psm 6")
    print(text)
    return text


def compareTime(port, coordinate_with_img_name):
    try:
    # Convert coordinate_with_img_name which comes as a string to List.
        result = json.loads(coordinate_with_img_name.replace("'", "\""))

        given_time_str = convert_image_time_text(port, result[0], result[1], result[2], result[3], result[4])
        pm_index = given_time_str.find("PM")

        # Remove characters after "PM" (including "PM")
        if pm_index != -1:
            given_time_str = given_time_str[:pm_index + 2]  # +2 to include "PM"

        print("Modified time:", given_time_str)
        # Convert the given time string to a datetime object
        given_time_obj = datetime.strptime(given_time_str, "%I:%M %p")

        # Current time
        current_time = datetime.now().time()

        # Create a datetime object for the current date with the given time
        current_datetime_with_given_time = datetime.combine(datetime.now().date(), given_time_obj.time())

        # Define the acceptable time difference (in minutes)
        acceptable_time_difference = 3

        # Calculate the time range
        lower_bound = current_datetime_with_given_time - timedelta(minutes=acceptable_time_difference)
        upper_bound = current_datetime_with_given_time + timedelta(minutes=acceptable_time_difference)
        print(upper_bound.time())
        print(datetime.now().time())
        # Compare the current time within the allowed range
        if lower_bound.time() <= datetime.now().time() <= upper_bound.time():
            return True
        else:
            return False
    except:
        return  "TError"


def preprocess_image(image_path):
    # Read image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Resize image
    scale_percent = 150  # percentage of original size
    width = int(thresh.shape[1] * scale_percent / 100)
    height = int(thresh.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_LINEAR)
    
    # Save preprocessed image temporarily
    
    cv2.imwrite(image_path, resized)
    
    return image_path

def cropImage_Compare(port, coordinate_with_img_name):
    try:
        result = json.loads(coordinate_with_img_name.replace("'", "\""))
        print(result)
        text = convert_image_time_text(port, result[0], result[1], result[2], result[3], result[4])
        return text
    except:
        return  "TError"
# convert_image_time_text()


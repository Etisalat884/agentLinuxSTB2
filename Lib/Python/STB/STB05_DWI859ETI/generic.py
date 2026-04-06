import cv2
import numpy as np
from PIL import Image
import imagehash
from pathlib import Path
import os
import datetime
from robot.api import logger
import requests
import subprocess
import base64
import signal
from skimage.metrics import structural_similarity as ssim

def compare_image(img1, img2):
    hash0 = imagehash.average_hash(Image.open(img1))
    hash1 = imagehash.average_hash(Image.open(img2))

    cutoff = 1  # maximum bits that could be different between the hashes.
    print(hash0-hash1)
    if hash0 - hash1 < cutoff:
        return True
    else:
        return False

def compare_ssim(img1, img2, threshold=0.98):
    """
    Compares two images using SSIM.
    Returns a tuple: (score, True if motion detected)
    """
    img1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
    score, _ = ssim(img1, img2, full=True)
    print(f"SSIM score between {img1} and {img2}: {score}")
    return score, score < threshold
# print(compare_image("/home/user/NBCPOC/IMAGES/ref1.jpg", "/home/user/NBCPOC/IMAGES/Reference/ComcastYouTubePage1.jpg"))



##### Commenting "Capture_image" and "capture_image_run", as opencv is not wokring properly while capturing image from capture card. 
##### Using FFMPEG to capture to capture image intead of opencv





# def capture_image(port, imgname):
#     camera = cv2.VideoCapture(port)
#     camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1980)
#     camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#     result = True
#     while (result):
#         ret, frame = camera.read()
#         imgloc = imgname
#         print(cv2.imwrite(imgloc, frame))
#         result = False
#     camera.release()
#     cv2.destroyAllWindows()



# def capture_image_run(port, imgname):
#     camera = cv2.VideoCapture(port)
#     camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#     camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#     result = True
#     while (result):
#         ret, frame = camera.read()
#         imgloc = imgname
#         cv2.imwrite(imgloc, frame)
#         result = False
#     camera.release()
#     cv2.destroyAllWindows()


def capture_image(port, imgname):
    command = [
        "ffmpeg", "-y", "-f", "v4l2", "-input_format", "yuyv422", "-i", f"/dev/video{port}",
        "-vframes", "1", imgname
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def capture_image_run(port, imgname):
    command = [
        "ffmpeg", "-y", "-f", "v4l2", "-input_format", "yuyv422",
        "-video_size", "854x480",  # Set resolution to 480p
        "-i", f"/dev/video{port}", "-vframes", "1", imgname
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def restore_ffmpeg(device="/dev/video0"):
    """
    Finds and kills all ffmpeg processes using the given video device.
    """
    try:
        result = subprocess.run(["lsof", "-t", device], capture_output=True, text=True, check=True)
        pids = result.stdout.strip().split('\n')
    except subprocess.CalledProcessError:
        print(f"No process is using {device}.")
        return

    for pid in pids:
        try:
            cmdline = open(f"/proc/{pid}/cmdline").read()
            if 'ffmpeg' in cmdline:
                os.kill(int(pid), signal.SIGKILL)
                print(f"Killed ffmpeg process with PID: {pid}")
        except FileNotFoundError:
            print(f"Process {pid} no longer exists.")
        except PermissionError:
            print(f"No permission to kill process {pid}.")
        except Exception as e:
            print(f"Failed to process PID {pid}: {e}")


def get_date_time():
    c_time = datetime.datetime.now()
    f_time = c_time.strftime("%Y_%m_%d_%H_%M_%S_%f")
    return f_time


def image_path(filename):
    file_name = os.path.basename(filename)
    #screenshot_path = '%s%s' % (f"./IMAGES/",file_name)
    screenshot_path = '%s%s' % (f"./",file_name)
    print(screenshot_path)
    logger.info('\n<a href="%s" target="_blank">%s</a><br><img src="%s">' % (screenshot_path,file_name, screenshot_path), html=True)
    return screenshot_path


def show_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
        extension = image_path.split('.')[-1]
        return f"<img src='data:image/{extension};base64,{encoded_string}'></img>"



def get_meta_data(data, parent_key, child_key, nested_keys):
    """
    Recursively traverse the nested JSON data to extract the values of the specified nested keys from a child key.
    """
    values = []
    if isinstance(data, dict):
        for k, v in data.items():
            if k == parent_key and isinstance(v, list):
                for item in v:
                    if child_key in item:
                        child_value = item[child_key]
                        if isinstance(child_value, dict):
                            for nested_key in nested_keys:
                                if nested_key in child_value:
                                    values.append(child_value[nested_key])
                        elif isinstance(child_value, list):
                            for child_item in child_value:
                                if isinstance(child_item, dict):
                                    for nested_key in nested_keys:
                                        if nested_key in child_item:
                                            values.append(child_item[nested_key])
            elif isinstance(v, (dict, list)):
                values.extend(get_meta_data(v, parent_key, child_key, nested_keys))

    elif isinstance(data, list):
        for item in data:
            values.extend(get_meta_data(item, parent_key, child_key, nested_keys))

    return values

def cbs_api_call():
    # Define the API endpoint URL
    api_url = 'https://www.cbsnews.com/video/xhr/collection/component/live-channels/?is_logged_in=0&edition=us'
    
    # Make a GET request to the API endpoint
    response = requests.get(api_url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
    
        # Specify the parent key, child key, and nested keys you want to extract values for
        parent_key = 'items'
        child_key = 'items'
        nested_keys = ['fulltitle']
    
        # Extract the values of the specified nested keys from the child key
        live_info = get_meta_data(data, parent_key, child_key, nested_keys)
    
        if live_info:
            print("Live Information:", live_info)
        else:
            print("No values found for the Live TV Information.")
        # text = []
        # text.append(live_info[2])
        # text.append(live_info[3])
        return live_info
    else:
        # If the request was not successful, print an error message
        print("Error:", response.status_code)
        return ['Error']





def check_cbs_list_items_string(list1, list2):
    new_texts = [f"CBS News {text}" for text in list1]  
    cleaned_texts = []
    for text in new_texts:
        cleaned_texts.append(text.strip())
    cleaned_texts = [item.lower() for item in cleaned_texts]
    list2 = [item.lower() for item in list2]

    print("On Screen Metadata:", cleaned_texts)
    print("API Metdata:", list2)
    flag = all(item in list2 for item in cleaned_texts)
    return flag




#print(compare_image("/home/user/NBCPOC/IMAGES/Reference/roku_allblkexit1.jpg","/home/user/NBCPOC/IMAGES/Reference/roku_allblkexit.jpg"))

#capture_image('3','/home/user/NBCPOC/IMAGES/Reference/.jpg')
# capture_image('4','/home/user/NBCPOC/IMAGES/Reference/samsungyoutubeexitpage.jpg')
# capture_image('2','/home/user/NBCPOC/IMAGES/Reference/Appleyoutubeexitpage.jpg')
# capture_image('2','/home/user/NBCPOC/IMAGES/Reference/apple2012page.jpg')
# capture_image('3','/home/user/NBCPOC/IMAGES/Reference/Youtubehomepage.jpg')
# capture_image('2','/home/user/NBCPOC/IMAGES/Reference/ref2_img.jpg')
# capture_image('0','/home/user/NBCPOC/IMAGES/Reference/youtubeexitpage.jpg')
# capture_image('3','/home/user/NBCPOC/IMAGES/Reference/AppleAllblkexitpag.jpg')

# capture_image(3,'/home/user/JC_5_Agent_8/agent8dut1/workspace/Rokutv/IMAGES/Reference/roku_youtubeexitpage.jpg')


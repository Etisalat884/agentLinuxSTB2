import subprocess

def capture_image(port, imgname):
    # Create the FFmpeg command to capture a frame
    command = [
        "ffmpeg", "-y", "-f", "v4l2", "-input_format", "yuyv422",
        "-video_size", "1280x720",  # Set resolution to 720p
        "-i", f"/dev/video{port}", "-vframes", "1", imgname  # Capture 1 frame
    ]

    # Run the FFmpeg command using subprocess
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Check if the command was successful
    if result.returncode == 0:
        print(f"Image saved to {imgname}")
        return imgname
    else:
        print("Error: FFmpeg failed to capture image.")
        return None

# Set the exact path to save the image
img_path = "/home/ltts2/Documents/agentLinuxSTB1/workspace/IMAGES/screenshotAPI.jpg"
port = 0  # Webcam port (usually 0 for the default webcam)

# Call capture_image to capture and save the image
captured_image = capture_image(port, img_path)

if captured_image:
    print(f"Image successfully captured and saved: {captured_image}")
else:
    print("Failed to capture the image.")

        

capture_image(0, "test.jpg")


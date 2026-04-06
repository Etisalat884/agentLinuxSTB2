import subprocess
from flask import Flask, jsonify, send_file
import tempfile
from flask_cors import cross_origin

app = Flask(__name__)

@app.route('/screenshot', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def screenshot():
    # Capture image using FFmpeg
    img = capture_image(0, "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Images/screenshotAPI.jpg")
    
    if img is not None:
        # Serve the saved image in the response
        return send_file(img, as_attachment=True)
    else:
        return jsonify({"Error": "Failed to capture image"}), 500


def capture_image(port, imgname):
    # FFmpeg command to capture a single frame from the webcam
    command = [
        "ffmpeg", "-y", "-f", "v4l2", "-input_format", "yuyv422",
        "-video_size", "1280x720",  # Set resolution to 720p
        "-i", f"/dev/video{port}", "-vframes", "1", imgname  # Capture 1 frame
    ]
    
    # Run the FFmpeg command using subprocess
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if result.returncode == 0:
        print(f"Image saved to {imgname}")
        return imgname  # Return the path to the saved image
    else:
        print("Error: FFmpeg failed to capture image.")
        return None


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3002)


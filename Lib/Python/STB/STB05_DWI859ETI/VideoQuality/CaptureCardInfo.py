import cv2

def get_capture_card_info(video_source=0):
    """
    Get full capture card parameters including resolution, FPS, and other settings.
    
    Args:
        video_source: int or str, index of the capture card or device path.
        
    Returns:
        dict: Dictionary of capture card parameters.
    """
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video source {video_source}")

    # Dictionary to hold parameter values
    params = {}

    # Dictionary of properties to query
    properties = {
        "frame_width": cv2.CAP_PROP_FRAME_WIDTH,
        "frame_height": cv2.CAP_PROP_FRAME_HEIGHT,
        "frame_rate": cv2.CAP_PROP_FPS,
        "fourcc": cv2.CAP_PROP_FOURCC,
        "brightness": cv2.CAP_PROP_BRIGHTNESS,
        "contrast": cv2.CAP_PROP_CONTRAST,
        "saturation": cv2.CAP_PROP_SATURATION,
        "hue": cv2.CAP_PROP_HUE,
        "gain": cv2.CAP_PROP_GAIN,
        "exposure": cv2.CAP_PROP_EXPOSURE
    }

    # Read each property
    for name, prop in properties.items():
        val = cap.get(prop)
        params[name] = val

    # Convert FOURCC to string
    fourcc = int(params["fourcc"])
    params["fourcc_str"] = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])

    cap.release()
    return params

# Example usage
if __name__ == "__main__":
    info = get_capture_card_info(video_source=0)
    print("Capture Card Parameters:")
    for k, v in info.items():
        print(f"{k}: {v}")

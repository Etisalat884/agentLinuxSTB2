from robot.api.deco import keyword
import cv2
import easyocr
import os

@keyword("Extract EPG Texts From Bottom Image")
def extract_epg_texts_from_bottom_image(image_path, bottom_ratio=0.3):
    if not isinstance(image_path, str):
        raise TypeError(f"Expected image path as string, got {type(image_path).__name__}")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Load and crop bottom portion
    image = cv2.imread(image_path)
    height = image.shape[0]
    bottom_crop = image[int(height * (1 - bottom_ratio)):, :]

    # Enhance contrast
    gray = cv2.cvtColor(bottom_crop, cv2.COLOR_BGR2GRAY)
    enhanced = cv2.equalizeHist(gray)

    # Save temporary enhanced image
    temp_path = "enhanced_bottom.png"
    cv2.imwrite(temp_path, enhanced)

    # OCR
    reader = easyocr.Reader(['en', 'ar'], gpu=False)
    results = reader.readtext(temp_path)

    # Extract readable texts
    texts = [text.strip() for _, text, _ in results if text.strip()]
    return texts
from robot.api.deco import keyword
import cv2
import pytesseract
from PIL import Image
import os
import re
import numpy as np
import yaml

# ✅ Load correction and phrase merging data from config file
CONFIG_PATH = "ocr_config.yaml"
CORRECTION_MAP = {}
MERGED_PHRASES = []

if os.path.exists(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)
            CORRECTION_MAP = config.get("correction_map", {})
            MERGED_PHRASES = config.get("merged_phrases", [])
            print("✅ OCR config loaded successfully.")
    except Exception as e:
        print(f"⚠️ Failed to load OCR config: {e}")
else:
    print("⚠️ OCR config file not found, using default settings.")

# ✅ Regex for time format (e.g. 01:23 or 01:23:45)
TIME_PATTERN = r'\d{1,2}:\d{2}(?::\d{2})?'

def preprocess_image(image_path):
    print(f"\n📂 Preprocessing: {image_path}")
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return None

    img = cv2.imread(image_path)
    if img is None:
        print("❌ Failed to read image.")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    contrast = cv2.convertScaleAbs(inverted, alpha=2.5, beta=50)
    denoised = cv2.medianBlur(contrast, 3)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    resized = cv2.resize(thresh, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    # Save debug image
    cv2.imwrite("debug_processed.jpg", resized)
    return resized

@keyword("Extract And Check Text")
def extract_and_check_text(image_path, expected_text):
    processed_img = preprocess_image(image_path)
    if processed_img is None:
        return False

    pil_img = Image.fromarray(processed_img)
    config = r'--oem 3 --psm 11'
    try:
        extracted_text = pytesseract.image_to_string(pil_img, config=config)
    except Exception as e:
        print(f"❌ OCR failed: {e}")
        return False

    print("📄 Extracted Text:\n------------------")
    print(extracted_text)
    print("------------------")

    if expected_text.lower() in extracted_text.lower():
        print(f"✅ Found '{expected_text}' in extracted text.")
        return True
    else:
        print(f"❌ '{expected_text}' not found in extracted text.")
        return False

@keyword("Extract Time From Image")
def extract_time_from_image(image_path):
    print(f"🕒 Extracting time from: {image_path}")
    if not os.path.exists(image_path):
        print("❌ File not found!")
        return ""

    img = cv2.imread(image_path)
    if img is None:
        print("❌ Failed to load image.")
        return ""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    enhanced = cv2.convertScaleAbs(gray, alpha=2.5, beta=45)
    blur = cv2.GaussianBlur(enhanced, (3, 3), 0)
    sharpen = cv2.addWeighted(enhanced, 1.5, blur, -0.5, 0)
    resized = cv2.resize(sharpen, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_LINEAR)
    cv2.imwrite("debug_processed_time.png", resized)

    config = r'--oem 3 --psm 6'
    pil_img = Image.fromarray(resized)
    text = pytesseract.image_to_string(pil_img, config=config)

    print("📄 OCR Output (Time Detection):")
    print(text.strip())

    match = re.search(TIME_PATTERN, text)
    if match:
        time_found = match.group(0)
        print(f"✅ Time Found: {time_found}")
        return time_found
    else:
        print("❌ No valid time found.")
        return ""

@keyword("Extract Clean OCR Text")
def extract_clean_ocr_text(image_path):
    print(f"\n🔍 Extracting from: {image_path}")
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return []

    def run_ocr_on_image(img):
        pil_img = Image.fromarray(img)
        config = r'--oem 3 --psm 6'
        try:
            text = pytesseract.image_to_string(pil_img, config=config)
        except Exception as e:
            print(f"❌ OCR error: {e}")
            return []
        return re.findall(r"\b[\w']+\b", text)

    all_words = []

    # Method 1: Preprocessed image
    img1 = preprocess_image(image_path)
    if img1 is not None:
        all_words += run_ocr_on_image(img1)

    # Method 2 & 3: Alternate processing
    img_orig = cv2.imread(image_path)
    if img_orig is not None:
        gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
        inverted = cv2.bitwise_not(gray)
        contrast = cv2.convertScaleAbs(inverted, alpha=2.5, beta=50)
        _, thresh = cv2.threshold(contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        resized_thresh = cv2.resize(thresh, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
        all_words += run_ocr_on_image(resized_thresh)

        high_contrast = cv2.convertScaleAbs(gray, alpha=2.7, beta=60)
        blur = cv2.GaussianBlur(high_contrast, (3, 3), 0)
        sharpened = cv2.addWeighted(high_contrast, 1.8, blur, -0.8, 0)
        sharpened_resized = cv2.resize(sharpened, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
        all_words += run_ocr_on_image(sharpened_resized)

    corrected_words = [CORRECTION_MAP.get(w, w) for w in all_words if len(w) > 2]
    full_text = " ".join(corrected_words)

    phrase_matches = []
    for phrase in MERGED_PHRASES:
        if re.search(re.escape(phrase), full_text, flags=re.IGNORECASE):
            phrase_matches.append(phrase)

    final_words = sorted(set(corrected_words + phrase_matches))
    print(f"📋 Total Unique Words Found: {len(final_words)}")
    for word in final_words:
        print(word)

    return final_words

@keyword("Extract Text As List")
def extract_text_as_list(image_path):
    processed_img = preprocess_image(image_path)
    if processed_img is None:
        return []

    pil_img = Image.fromarray(processed_img)
    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(pil_img, config=config)

    print("📄 Raw OCR Output:\n" + "-"*30 + f"\n{text}\n" + "-"*30)
    words = re.findall(r'\b[\w@.-]+\b', text)
    clean_words = [w for w in words if len(w) >= 3 and re.search(r'[a-zA-Z]', w)]
    print(f"✅ Filtered Word List: {clean_words}")
    return clean_words

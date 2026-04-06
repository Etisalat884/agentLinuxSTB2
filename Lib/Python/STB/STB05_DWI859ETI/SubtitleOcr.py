import os
import re
from collections import Counter

import easyocr
from langdetect import detect
from robot.api.deco import keyword

# Initialize EasyOCR once for English and Arabic
OCR_READER = easyocr.Reader(['en', 'ar'], gpu=False)

def is_meaningful_text(text):
    """
    Skip numbers, symbols, or very short strings.
    Keeps texts with letters (English or Arabic) and length > 1
    """
    return bool(re.search(r'[A-Za-z\u0600-\u06FF]', text)) and len(text.strip()) > 1

@keyword("Extract Subtitle Language")
def extract_subtitle_language(image_path, expected_lang="en", confidence_threshold=0.2):
    """
    Extracts subtitle text from an image and detects the language.

    :param image_path: Path to the image file
    :param expected_lang: Expected language code ('en' or 'ar')
    :param confidence_threshold: Minimum OCR confidence to consider
    :return: True if the majority of detected texts match the language, False otherwise
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    print(f"\nProcessing image: {image_path}")

    # Perform OCR
    try:
        result = OCR_READER.readtext(image_path)
    except Exception as e:
        print(f"OCR failed: {e}")
        return False

    detected_texts = []

    # Print raw OCR output and filter meaningful text
    print("Raw OCR results:")
    for detection in result:
        if len(detection) < 3:
            continue
        bbox, text, confidence = detection
        text = text.strip()
        print(f"Text: '{text}', Confidence: {confidence:.2f}")
        if confidence < confidence_threshold:
            continue
        if not is_meaningful_text(text):
            continue
        detected_texts.append(text)

    if not detected_texts:
        print("No meaningful text detected.")
        return False

    # Detect language per line and vote for majority
    try:
        langs = [detect(t) for t in detected_texts]
        detected_lang = Counter(langs).most_common(1)[0][0]
        print(f"Detected language: {detected_lang}")
    except Exception as e:
        print(f"Language detection failed: {e}")
        return False

    # Check if detected language matches expected
    match = detected_lang == expected_lang
    if match:
        print(f"✅ Language match for image: {image_path}")
    else:
        print(f"❌ Expected '{expected_lang}', but detected '{detected_lang}'")

    print(f"Detected texts: {detected_texts}")
    return match


# Example standalone run
if __name__ == "__main__":
    test_image = "path/to/your/image.png"
    extract_subtitle_language(test_image, expected_lang="en")

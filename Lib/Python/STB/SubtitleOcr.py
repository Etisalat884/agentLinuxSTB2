from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import easyocr
import os
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # For consistent detection



def normalize_language(lang_code: str) -> str:
    """Normalize detected language to English (en) or Arabic (ar)."""
    if lang_code == "fa":  # Persian misclassified as Arabic
        return "ar"
    return lang_code


@keyword("Validate OCR Language")
def validate_ocr_language(image_path, expected_language):
    """
    Extract text from a single image and check if it matches the expected language.
    Returns True if matched, raises AssertionError if not.
    Logs all detected texts to Robot Framework logs.
    """
    bi = BuiltIn()

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    reader = easyocr.Reader(['en', 'ar'], gpu=False)
    result = reader.readtext(image_path)

    detected_texts = [d[1].strip() for d in result if len(d) >= 2 and d[1].strip()]

    if not detected_texts:
        raise AssertionError(f"No text detected in image: {image_path}")

    # Log all detected texts in Robot Framework
    bi.log(f"📝 Texts detected from image {image_path}: {detected_texts}", level="INFO")

    for text in detected_texts:
        try:
            lang = detect(text)
        except:
            lang = "unknown"
        lang = normalize_language(lang)
        bi.log(f"Detected: '{text}' → {lang}", level="INFO")
        if lang != expected_language:
            # Log failed text before failing
            bi.log(f"❌ Expected '{expected_language}', but got '{lang}' for text: '{text}' in image: {image_path}'", level="ERROR")
            raise AssertionError(f"Language mismatch for text: '{text}' in image: {image_path}")

    bi.log(f"✅ Image {image_path} matches language: {expected_language}", level="INFO")
    return True

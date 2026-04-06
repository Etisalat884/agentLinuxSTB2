from robot.api.deco import keyword
from robot.api import logger
import pytesseract
import cv2
import os

# Language-specific letters for validation
NORDIC_LETTERS = {
    'fi': 'äöåÄÖÅ',
    'sv': 'åäöÅÄÖ',
    'no': 'æøåÆØÅ'
}

def normalize_text(text: str) -> str:
    """Remove non-alphabetic characters and trim spaces."""
    return ''.join(c for c in text if c.isalpha() or c.isspace()).strip()

def contains_language_letters(text: str, lang: str) -> bool:
    """Check if text contains letters specific to the language."""
    letters = NORDIC_LETTERS.get(lang, '')
    return any(c in letters for c in text)

@keyword("Extract Nordic Text From Image")
def extract_nordic_text_from_image(image_path, expected_language):
    """Use Tesseract to extract Finnish, Swedish, or Norwegian text."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    tesseract_lang = {'fi': 'fin', 'sv': 'swe', 'no': 'nor'}[expected_language]

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not loaded: {image_path}")

    text = pytesseract.image_to_string(img, lang=tesseract_lang)

    detected_texts = []
    for line in text.splitlines():
        clean_text = normalize_text(line)
        if len(clean_text) >= 2:
            detected_texts.append(clean_text)

    return detected_texts

@keyword("Repeat OCR And Validate Nordic Language")
def repeat_ocr_and_validate_nordic_language(image_path, expected_language):
    texts = extract_nordic_text_from_image(image_path, expected_language)

    if not texts:
        logger.console("No text detected in this frame.")
        return False

    for t in texts:
        logger.console(f"Extracted text: '{t}'")

    for text in texts:
        if contains_language_letters(text, expected_language):
            logger.console(f"Frame contains {expected_language.upper()} subtitle: '{text}'")
            return True

    return False

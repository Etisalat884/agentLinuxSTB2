from robot.api.deco import keyword
from robot.api import logger
import easyocr
import os

def normalize_text(text: str) -> str:
    return ''.join(c for c in text if c.isalnum() or c.isspace()).strip()

@keyword("Extract Program Info Text From Image")
def extract_program_info_text_from_image(image_path: str, min_confidence: float = 0.4):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    reader = easyocr.Reader(['en', 'ar'], gpu=False)
    results = reader.readtext(image_path)

    extracted_texts = []
    for detection in results:
        if len(detection) >= 3:
            bbox, text, conf = detection
            if conf < min_confidence:
                continue
            clean_text = normalize_text(text)
            if len(clean_text) >= 2:
                extracted_texts.append(clean_text)

    if extracted_texts:
        logger.console("📺 Program Info Texts:")
        for t in extracted_texts:
            logger.console(f"- {t}")
    else:
        logger.console("⚠️ No readable program info found in the image.")

    return extracted_texts


@keyword("Get Channel Number From Texts")
def get_channel_number_from_texts(texts):
    for text in texts:
        # Accept only if all characters are Western digits (0–9)
        if all(c in '0123456789' for c in text):
            return text
    return "UNKNOWN"
# import easyocr
# import os

# class OcrExtractText:
#     def __init__(self):
#         # Initialize EasyOCR reader only once
#         print("Initializing OCR...")
#         self.reader = easyocr.Reader(['en'], gpu=False)  # Force CPU to avoid CUDA issue

#     def extract_text_from_image(self, image_path):
#         """
#         Extracts text from the given image and returns a list of detected strings.
#         Usage in Robot Framework:
#         ${texts}=    Extract Text From Image    /path/to/image.png
#         """
#         # Check if file exists
#         if not os.path.exists(image_path):
#             raise FileNotFoundError(f"Image not found: {image_path}")
#         else:
#             print(f"Image found: {image_path}")

#         print("Reading text...")
#         result = self.reader.readtext(image_path)

#         detected_texts = []
#         print("\nDetected Text:")
#         for detection in result:
#             if len(detection) == 3:
#                 _, text, prob = detection
#                 print(f"{text} (confidence: {prob:.2f})")
#                 if prob > 0.3:  # Filter low-confidence text
#                     detected_texts.append(text)
#             else:
#                 _, text = detection
#                 print(f"{text} (confidence: unknown)")
#                 detected_texts.append(text)

#         return detected_texts


from robot.api.deco import keyword
import easyocr
import os

@keyword("Extract Text From Image")
def extract_text_from_image(image_path):
    """
    Extracts text from an image using EasyOCR and returns it as a list of lowercase strings.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    print(f"Image found: {image_path}")

    # Initialize EasyOCR
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image_path)

    # Extract and convert all detected text to lowercase
    detected_texts = []
    for detection in result:
        if len(detection) >= 2:  # Ensure (bbox, text) or (bbox, text, prob)
            detected_texts.append(detection[1].lower())

    return detected_texts






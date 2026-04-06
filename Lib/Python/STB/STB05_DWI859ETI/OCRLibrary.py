import easyocr

class OCRLibrary:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def extract_text_from_image(self, image_path):
        results = self.reader.readtext(image_path)
        return " ".join([text for _, text, _ in results])
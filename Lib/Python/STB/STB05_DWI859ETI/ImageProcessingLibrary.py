import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim
from datetime import datetime
import  re

class ImageProcessingLibrary:
    

    def crop_progress_bar(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # TEMP: Wider slice to locate red bar
        y_start = int(h * 0.68)
        y_end = int(h * 0.70)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.09)
        x_end = int(w * 0.14)


        cropped = img[y_start:y_end, 0:w]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path    
    def crop_progress_bar_On_Pause(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # TEMP: Wider slice to locate red bar
        y_start = int(h * 0.68)
        y_end = int(h * 0.70)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.50)
        x_end = int(w * 0.65)


        cropped = img[y_start:y_end, 0:w]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path    
    def crop_progress_bar_after(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.78)
        y_end = int(h * 0.80)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.09)
        x_end = int(w * 0.92)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path    
    def crop_subtitle_arabic(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.86)
        y_end = int(h * 0.92)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.09)
        x_end = int(w * 0.92)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def crop_subtitle_english(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.85)
        y_end = int(h * 0.92)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.09)
        x_end = int(w * 0.92)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path  
    def crop_Thumnail_More_Details(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # TEMP: Wider slice to locate red bar
        y_start = int(h * 0.60)
        y_end = int(h * 0.90)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.45)
        x_end = int(w * 0.55)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path   
    def crop_recording_type(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.65)
        y_end   = int(h * 0.70)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.02)
        x_end   = int(w * 0.10)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path

    def get_red_line_position(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 70, 50])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        coords = np.column_stack(np.where(mask > 0))
        if coords.size == 0:
            return -1  # No red line detected
        avg_x = int(np.mean(coords[:, 1]))
        return avg_x
    
    def compare_images_ssim(self, image_path1, image_path2):
        

        img1 = cv2.imread(image_path1)
        img2 = cv2.imread(image_path2)

        if img1 is None or img2 is None:
            raise ValueError("One or both images could not be loaded.")

        # Convert to grayscale for SSIM
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Resize if needed to match dimensions
        if gray1.shape != gray2.shape:
            gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))

        score, _ = ssim(gray1, gray2, full=True)
        return round(score, 4)
    
    def get_program_details(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # TEMP: Wider slice to locate red bar
        y_start = int(h * 0.20)
        y_end = int(h * 0.35)

        # # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.10)
        x_end = int(w * 0.12)

        cropped = img[y_start:y_end, 0:w]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}")
        return cropped_path
    
    def get_rounded_time_slots(self):   

        now = datetime.now()
        hour = now.hour

        # Format as HH:00 and HH:30
        slot_00 = f"{hour:02d}:00"
        slot_30 = f"{hour:02d}:30"

        return slot_00, slot_30
    
    def crop_channel_number(self, image_path):

            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Image not loaded: {image_path}")

            h, w = img.shape[:2]

            # TEMP: Wider slice to locate red bar
            y_start = int(h * 0.82)
            y_end = int(h * 0.95)

            # Horizontal padding: trim 5% from both sides
            x_start = int(w * 0.05)
            x_end = int(w * 0.4)


            cropped = img[y_start:y_end, 0:w]
            base, ext = os.path.splitext(image_path)
            cropped_path = f"{base}_progress_bar{ext}"
            cv2.imwrite(cropped_path, cropped)

            print(f"Image shape: {img.shape}")
            print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
            return cropped_path 
    
    def extract_first_number(self,  text):
        """
        Extracts the channel number from OCR text.
        Prioritizes number after '<' or before '>'.
        If both exist and are equal, returns either.
        Falls back to first numeric group if neither is found.
        """
        left_match = re.search(r'<\s*(\d+)', text)
        right_match = re.search(r'(\d+)\s*>', text)

        left = left_match.group(1) if left_match else ''
        right = right_match.group(1) if right_match else ''

        if left and right:
            if left == right:
                print(f"✅ Both match: {left}")
                return left
            else:
                print(f"🔀 Mismatch: after '<' = {left}, before '>' = {right}")
                return left  # or right, depending on your priority

        if left:
            print(f"✅ Extracted after '<': {left}")
            return left

        if right:
            print(f"✅ Extracted before '>': {right}")
            return right

        # Fallback: extract first numeric group
        number_list = re.findall(r'\d+', text)
        print(f"⚠️ Fallback numeric groups: {number_list}")
        return number_list[0] if number_list else ''
    
    def crop_channel_logo_top_right(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Adjusted vertical slice to start slightly higher
        y_start = int(h * 0.02)
        y_end   = int(h * 0.18)

        # Right-side horizontal slice
        x_start = int(w * 0.86)
        x_end   = int(w * 0.9)

        cropped = img[y_start:y_end, x_start:x_end]

        base, _ = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar.jpg"  # Force .jpg to avoid double extension
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped logo saved to: {cropped_path}")
        return cropped_path

    def extract_image_name(self, image_path):
        if not isinstance(image_path, str):
            raise TypeError(f"Expected image path as string, got {type(image_path).__name__}")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        return os.path.basename(image_path)


    def extract_image_name(self, image_path):
        if not isinstance(image_path, str):
            raise TypeError(f"Expected image path as string, got {type(image_path).__name__}")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        return os.path.basename(image_path)
    def Channel_Name_In_Recorder_Of_MyList(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.33)
        y_end   = int(h * 0.38)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.48)
        x_end   = int(w * 0.58)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Local_And_Cloud_Recording_Supported(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.47)
        y_end   = int(h * 0.60)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.44)
        x_end   = int(w * 0.58)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Check_For_Series_Recording(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.30)
        y_end   = int(h * 0.80)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.44)
        x_end   = int(w * 0.58)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Storage_Type_In_Recorder_List(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.33)
        y_end   = int(h * 0.38)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.17)
        x_end   = int(w * 0.30)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Channel_Name_From_EPG_Info_Bar(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.80)
        y_end   = int(h * 0.83)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.38)
        x_end   = int(w * 0.57)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Program_Time_From_EPG(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.48)
        y_end   = int(h * 0.52)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.43)
        x_end   = int(w * 0.49)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Catchup_Date_From_EPG(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

         # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.40)
        y_end   = int(h * 0.48)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.69)
        x_end   = int(w * 0.90)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path

    def Play_Side_Panel_Recorder(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.30)
        y_end   = int(h * 0.35)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.05)
        x_end   = int(w * 0.20)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    
    def Program_Name_From_EPG(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.48)
        y_end   = int(h * 0.52)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.48)
        x_end   = int(w * 0.57)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path

    def Channel_Name_From_Mosaic(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.48)
        y_end   = int(h * 0.51)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.06)
        x_end   = int(w * 0.26)


        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def Channel_Interface_Clock(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        y_start = int(h * 0.03)
        y_end   = int(h * 0.09)
        x_start = int(w * 0.92)
        x_end   = int(w * 0.98)


        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path

    def select_audio_language_pop_up(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.45)
        y_end   = int(h * 0.60)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.50)
        x_end   = int(w * 0.90)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def select_audio_language_First(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.60)
        y_end   = int(h * 0.65)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.60)
        x_end   = int(w * 0.92)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def select_audio_language_Second(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

         # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.65)
        y_end   = int(h * 0.70)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.74)
        x_end   = int(w * 0.92)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path


    def Channel_Title_From_EPG_Info_Bar(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.83)
        y_end   = int(h * 0.87)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.38)
        x_end   = int(w * 0.50)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    


       
    def cast_roi(self,image_path):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Approximate ROI for "Director" label and name
        # Adjust these numbers as needed after checking results visually
        y_start = int(h * 0.26)   # start a bit below the title "ARCTIC"
        y_end   = int(h * 0.31)   # cover the "Director: ..." line
        x_start = int(w * 0.05)   # left margin near where "Director" text starts
        x_end   = int(w * 0.85)   # end just past the director’s name

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_director_roi{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped director ROI saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path

    def Director_ROI_From_Info_Screen(self,image_path):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Approximate ROI for "Director" label and name
        # Adjust these numbers as needed after checking results visually
        y_start = int(h * 0.23)   # start a bit below the title "ARCTIC"
        y_end   = int(h * 0.28)   # cover the "Director: ..." line
        x_start = int(w * 0.05)   # left margin near where "Director" text starts
        x_end   = int(w * 0.35)   # end just past the director’s name

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_director_roi{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped director ROI saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path

    def Channel_Start_Time_From_EPG_Info_Bar(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.92)
        y_end   = int(h * 0.95)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.38)
        x_end   = int(w * 0.41)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Channel_Number_Program_Info_Bar(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.83)
        y_end   = int(h * 0.90)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.05)
        x_end   = int(w * 0.12)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Device_Information(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.83)
        y_end   = int(h * 0.90)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.05)
        x_end   = int(w * 0.12)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Channel_Second_Name_In_Recorder_Of_MyList(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.38)
        y_end   = int(h * 0.43)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.48)
        x_end   = int(w * 0.58)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_Profile_Name_Settings_page(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # TEMP: Wider slice to locate red bar
        y_start = int(h * 0.66)
        y_end = int(h * 0.69)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.79)
        x_end = int(w * 0.82)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_continue_watching_show_more_assets(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # TEMP: Wider slice to locate red bar
        y_start = int(h * 0.70)
        y_end = int(h * 0.83)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.43)
        x_end = int(w * 0.55)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_continue(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # TEMP: Wider slice to locate red bar
        y_start = int(h * 0.60)
        y_end = int(h * 0.90)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.45)
        x_end = int(w * 0.55)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path

    def Get_Device_Info_App_Version_key(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.20)
        y_end = int(h * 0.25)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.47)
        x_end = int(w * 0.75)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Device_Info_OctoADS_Version_key(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.25)
        y_end = int(h * 0.30)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.47)
        x_end = int(w * 0.75)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Device_Information_Sap_Version_key(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.30)
        y_end = int(h * 0.35)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.47)
        x_end = int(w * 0.75)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Device_Information_Firmware_key(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.35)
        y_end = int(h * 0.40)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.47)
        x_end = int(w * 0.75)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Device_Information_STB_Serial_Number_key(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.40)
        y_end = int(h * 0.44)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.47)
        x_end = int(w * 0.75)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Device_Information_Mac_Address_key(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.45)
        y_end = int(h * 0.50)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.47)
        x_end = int(w * 0.75)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Device_Information_Hard_Disk_key(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.48)
        y_end = int(h * 0.52)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.47)
        x_end = int(w * 0.75)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Device_Information_User_ID_key(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.54)
        y_end = int(h * 0.58)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.47)
        x_end = int(w * 0.75)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Device_Information_IP_Gateway_key(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.56)
        y_end = int(h * 0.60)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.47)
        x_end = int(w * 0.75)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Device_Information_Channel_Version_key(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.62)
        y_end = int(h * 0.67)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.47)
        x_end = int(w * 0.75)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Device_Information_STB_Model_key(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.65)
        y_end = int(h * 0.70)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.47)
        x_end = int(w * 0.75)
        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Program_Catchup_Schedules(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.01)
        y_end   = int(h * 0.49)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.56)
        x_end   = int(w * 0.61)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path

    def Program_Future_Schedules(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.49)
        y_end   = int(h * 0.98)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.56)
        x_end   = int(w * 0.61)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_Hide_Channel(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # TEMP: Wider slice to locate red bar
        y_start = int(h * 0.82)
        y_end = int(h * 0.98)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.03)
        x_end = int(w * 0.18)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_progress_bar_timeshift(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.73)
        y_end = int(h * 0.80)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.16)
        x_end = int(w * 0.865)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path

    def Get_Side_Pannel_Options(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.25)
        y_end   = int(h * 0.95)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.05)
        x_end   = int(w * 0.15)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def movie_name_from_transaction(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # TEMP: Wider slice to locate red bar
        y_start = int(h * 0.34)
        y_end = int(h * 0.39)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.30)
        x_end = int(w * 0.60)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def Daily_Side_Panel_Recorder(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.46)
        y_end   = int(h * 0.50)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.04)
        x_end   = int(w * 0.20)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def Date_Time_In_MyList(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.38)
        y_end   = int(h * 0.43)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.54)
        x_end   = int(w * 0.78)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def Time_Side_Panel_Recorder(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.63)
        y_end   = int(h * 0.70)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.04)
        x_end   = int(w * 0.20)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def Enddate_Side_Panel_Recorder(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.73)
        y_end   = int(h * 0.80)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.04)
        x_end   = int(w * 0.20)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def Channel_Name_From_Mosaic_With_Coords(self, image_path, x1f, x2f, y1f, y2f):
        """Crop specific mosaic region based on fractional coordinates"""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]
        x1, x2 = int(w * float(x1f)), int(w * float(x2f))
        y1, y2 = int(h * float(y1f)), int(h * float(y2f))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

        cropped = img[y1:y2, x1:x2]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_{x1}_{y1}{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped region saved: {cropped_path}")
        print(f"Coordinates: x=({x1},{x2}) y=({y1},{y2})")
        return cropped_path
    def crop_Assert_name(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        y_start = int(h * 0.42)
        y_end   = int(h * 0.48)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.55)
        x_end   = int(w * 0.85)


        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def crop_Assert_name_after_adding_to_list(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        y_start = int(h * 0.10)
        y_end   = int(h * 0.18)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.10)
        x_end   = int(w * 0.40)


        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_Rent_assert(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        y_start = int(h * 0.25)
        y_end   = int(h * 0.30)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.01)
        x_end   = int(w * 0.20)


        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_Transaction_rent(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        y_start = int(h * 0.32)
        y_end   = int(h * 0.39)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.30)
        x_end   = int(w * 0.53)


        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def Get_Side_Pannel_Options_Of_Filter(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.25)
        y_end   = int(h * 0.73)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.05)
        x_end   = int(w * 0.15)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_Assert_name_after_resume(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        y_start = int(h * 0.25)
        y_end   = int(h * 0.34)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.10)
        x_end   = int(w * 0.40)


        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_Assert_name_catchup(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        y_start = int(h * 0.03)
        y_end   = int(h * 0.08)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.01)
        x_end   = int(w * 0.40)


        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_Channel_Number_Hidden_Channel(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.52)
        y_end   = int(h * 0.56)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.07)
        x_end   = int(w * 0.11)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_Channel_Number_Fav_list(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
        y_start = int(h * 0.52)
        y_end   = int(h * 0.56)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.07)
        x_end   = int(w * 0.11)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    
    def crop_HD(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
      
        y_start = int(h * 0.40)
        y_end   = int(h * 0.50)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.01)
        x_end   = int(w * 0.20)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    def crop_rating(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: assuming thumbnails are mid-height
      
        y_start = int(h * 0.18)
        y_end   = int(h * 0.22)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.01)
        x_end   = int(w * 0.70)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def crop_subtitle_Danish(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.80)
        y_end = int(h * 0.92)


        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.09)
        x_end = int(w * 0.92)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def search_roi(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # Vertical slice: red bar region
        y_start = int(h * 0.25)
        y_end = int(h * 0.32)


        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.02)
        x_end = int(w * 0.22)

        cropped = img[y_start:y_end, x_start:x_end]
        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_progress_bar{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    def crop_Transaction_hd(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        y_start = int(h * 0.32)
        y_end   = int(h * 0.39)

        # Horizontal slice: second thumbnail (adjust as needed)
        x_start = int(w * 0.53)
        x_end   = int(w * 0.60)


        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
    
    
    def crop_Profile_Name_Settings_page_after_reboot(self, image_path):

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Image not loaded: {image_path}")

        h, w = img.shape[:2]

        # TEMP: Wider slice to locate red bar
        y_start = int(h * 0.40)
        y_end = int(h * 0.70)

        # Horizontal padding: trim 5% from both sides
        x_start = int(w * 0.50)
        x_end = int(w * 0.60)

        cropped = img[y_start:y_end, x_start:x_end]

        base, ext = os.path.splitext(image_path)
        cropped_path = f"{base}_second_thumbnail{ext}"
        cv2.imwrite(cropped_path, cropped)

        print(f"✅ Cropped second thumbnail saved to: {cropped_path}")
        print(f"Image shape: {img.shape}")
        print(f"Cropping from y={y_start} to y={y_end}, x={x_start} to x={x_end}")
        return cropped_path
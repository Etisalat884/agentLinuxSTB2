# import requests

# def upload_baseline():
#     url = "http://localhost:5000/banner-diff"

#     payload = {
#         "test_image_path": "http://192.168.1.101:5001/ref3_2026_03_05_09_52_39_478223.jpg",
#         "baseline_path": "http://192.168.1.101:9000/campaigns/LTTS/assets/baselines/LTTS%20Banner_9128175475999388_1771396322052_baseline.png"
#     }
      

#     headers = {
#         "Content-Type": "application/json"
#     }

#     response = requests.post(
#         url,
#         json=payload,
#         headers=headers,
#         timeout=30
#     )

#     print("Status Code:", response.status_code)
#     print("Response:", response.text)


# upload_baseline()


############################# API Function ##################################


# file: AdValidationLibrary.py
import requests
from robot.api.deco import keyword
def validate_ad(test_image_url, baseline_url,endpoint):
    """
    Calls the banner-diff API using HTTP URLs for images.
    Returns True if ad matches, else False.
    Prints decision reason.
    """
    url = f"http://localhost:5000/{endpoint}"
    print(url)
    # url = "http://localhost:5000/banner-diff"
    #url = "http://localhost:5000/l-shape-diff"
    payload = {
        "test_image_path": test_image_url,
        "baseline_path": baseline_url
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        summary = data.get("summary", {})
        ad_match = summary.get("ad_match", False)
        decision = summary.get("decision_reason", "No reason provided")
        threshold = summary.get("threshold_used", "N/A")

        print(f"Ad Match: {ad_match}, Reason: {decision}, Threshold: {threshold}")
        return ad_match

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return False

def get_diff_img(test_image_url, baseline_url,endpoint):
    """
    Calls the banner-diff API using HTTP URLs for images.
    Returns True if ad matches, else False.
    Prints decision reason.
    """
    url = f"http://localhost:5000/{endpoint}"
    print(url)
    # url = "http://localhost:5000/banner-diff"
    #url = "http://localhost:5000/l-shape-diff"

    payload = {
        "test_image_path": test_image_url,
        "baseline_path": baseline_url
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        outputs = data.get("outputs", {})
        diff_img = outputs.get("diff_image_url")

        print(f"diff_img URL: {diff_img}")
        return diff_img

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return False
    

def detect_ad(image_urls, endpoint):
    """
    Calls banner-detect API using multiple runtime images.
    Returns True if ad is present.
    """

    url = f"http://localhost:5000/{endpoint}"

    payload = {
        "image_paths": image_urls
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        summary = data.get("summary", {})
        ad_present = summary.get("ad_present", False)
        # reason = summary.get("decision_reason", "No reason")

        print(f"Ad Present: {ad_present}")

        return ad_present

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return False
    
import requests

def get_diff_detect_image(image_urls, endpoint):
    """
    Calls banner-detect API and returns the diff images public URL.
    """

    url = f"http://localhost:5000/{endpoint}"

    payload = {
        "image_paths": image_urls
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        folder = data.get("folder", {})
        public_url = folder.get("public_url", "")

        print(f"Diff Images URL: {public_url}")

        return public_url   # ✅ RETURN FROM HERE

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return ""
    

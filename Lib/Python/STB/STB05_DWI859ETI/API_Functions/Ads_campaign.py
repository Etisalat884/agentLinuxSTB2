import json
import requests

def load_campaign_json(json_url):
    response = requests.get(json_url)
    data = response.json()
    return data

# Function 1: Get Baseline Asset
def get_baseline_asset(json_file, ad_name):

    data = load_campaign_json(json_file)

    for ad in data.get("ads", []):
        if ad.get("name") == ad_name:
            return ad.get("Baseline_assets", [None])[0]

    return None


# Function 2: Get Trigger Details
def get_ad_details(json_file, ad_name):

    data = load_campaign_json(json_file)

    trigger_asset = None
    baseline_asset = None
    trigger_names = []
    trigger_types = []
    trigger_events = []

    content_ids = []
    content_names = []
    content_types = []

    for ad in data.get("ads", []):
        if ad.get("name") == ad_name:

            # trigger_asset = ad.get("assets", [None])[0]
            # baseline_asset = ad.get("Baseline_assets", [None])[0]

            for trigger in ad.get("triggers", []):

                trigger_names.append(trigger.get("triggerName"))
                trigger_types.append(trigger.get("triggeringType"))
                trigger_events.append(trigger.get("event"))

                for content in trigger.get("contents", []):
                    content_ids.append(content.get("contentId"))
                    content_names.append(content.get("contentName"))
                    content_types.append(content.get("contentType"))

            return  trigger_names, trigger_types, trigger_events, content_ids, content_names, content_types

    return None, None, [], [], [], [], [], []
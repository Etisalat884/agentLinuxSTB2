# import requests

# def test_image():
#     url = "http://192.168.0.111:5000/test"   # Linux server IP

#     payload = {
#         "file_path": "http://192.168.0.180:8000/ABRYSVO_TEST/Prolia_MR_ad1.png",
#         "project_name": "PP"
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


# test_image()



import requests
def test_image(image_url, project_name="PP"):
    url = "http://192.168.0.111:5000/test"   # replace ip with Linux server IP

    payload = {
        "file_path": image_url,
        "project_name": project_name
        
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=30
    )

    return response.status_code, response.text







    
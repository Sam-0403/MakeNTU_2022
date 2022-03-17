import os
import requests

# Only for localhost
# os.environ['NO_PROXY'] = '127.0.0.1'

url = 'http://127.0.0.1:8000/sendData'
email = 'sam22187212@gmail.com'
# post_data = requests.post('http://127.0.0.1:8000/sendData', data={"type": "一般垃圾"})

def send_data(url, data):
    if 'http://127.0.0.1' in url:
        os.environ['NO_PROXY'] = '127.0.0.1'
    post_data = requests.post(url, data=data)
    return post_data

if __name__ == '__main__':
    count = 1
    while True:
        type = input("Type{}: ".format(count))
        if type == "Q":
            break
        send_data(url, {"type": type, "email": email})
        count += 1


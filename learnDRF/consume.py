import requests


url = 'http://127.0.0.1:8000/api/notes/'
token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzNDc1Mzk2LCJpYXQiOjE3MDMyOTUzOTYsImp0aSI6IjNmYTJiYmY3NzVhZDQ2ZTRiNDgwYmVjOGM0OTg1Y2Y4IiwidXNlcl9pZCI6MX0.QTVc_AnOcWeCkgrb-tiDlqpqiRRSnhjuzds9uBT0ELY')
headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(url, headers=headers)

print(response.text)
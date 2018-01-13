import requests

artist_name = 'beck'
const_id = '3vbKDsSS70ZX9D2OcvbZmS'

request = requests.get('http://localhost:5555/artist-id/beck')

status_code = request.status_code

if status_code == 200:
    print('got 200 yaa')
else:
    print('shit something went wrong, status code is {}'.format(status_code))

if request.text == '3vbKDsSS70ZX9D2OcvbZmS':
    print('ids match')
else:
    print('something went wrong, the id is {}'.format(request.text))

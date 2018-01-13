import requests
from app import get_artist_id



def test_artist_id():
    artist_name = 'beck'
    const_id = '3vbKDsSS70ZX9D2OcvbZmS'

    request = requests.get('http://localhost:5555/artist-id/beck')

    status_code = request.status_code
    id = get_artist_id('beck')
    assert id == '3vbKDsSS70ZX9D2OcvbZmS'
    assert status_code == 200
    if status_code == 200:
        print('got 200 yaa')
    else:
        print('shit something went wrong, status code is {}'.format(status_code))

    if request.text == '3vbKDsSS70ZX9D2OcvbZmS':
        print('ids match')
    else:
        print('something went wrong, the id is {}'.format(request.text))
    
    


import requests

ids = []
estado = 'ERROR'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

for id in ids:
    r = requests.post('http://pinta.bicubi.co/set_status.php', data={'id': id, 'status': estado}, headers=headers)

    if r.status_code == 200:
        print(str(id), r.json())
    else:
        print(str(id), r.status_code)

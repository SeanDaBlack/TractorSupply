import requests

r = requests.get(
        'https://api.mail.tm/domains').json().get('hydra:totalItems')

print(r)
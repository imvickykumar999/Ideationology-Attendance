
from json import dumps
from httplib2 import Http

def chatting(url, text, bot_message):
    
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()

    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

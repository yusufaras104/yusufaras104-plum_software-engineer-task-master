from flask import Blueprint, request, jsonify
from flask_api import status
import requests
import pyshorteners
import validators

api = Blueprint('api', __name__)

@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    data = request.json
    # get url from data
    # get provider from data
    url = data.get('url')

    if url:
        print(f'Url is {url}')
    else:
        return "url is required", status.HTTP_400_BAD_REQUEST

    # check url is a valid url
    if validators.url(url) == False:
        return "url is not valid", status.HTTP_400_BAD_REQUEST
    
    provider = data.get('provider')
    print(f'Provider is {provider}')
    # check provider is [bit.ly] or [tinyurl.com]
    if provider == 'bit.ly':
        provider = 'bitly';
    elif provider == 'tinyurl.com':
        provider = 'tinyurl';
    else:
        return "provider is not valid, should be either 'bit.ly' or 'tinyurl.com'", status.HTTP_400_BAD_REQUEST

    response = shorten(url, provider);

    return jsonify(response)

def shorten(url, provider):
    tempUrl = url
    # switch provider
    if provider == 'tinyurl':
        tempUrl = tinyurlShortener(url)
    elif provider == 'bitly':
        tempUrl = bitlyShortener(url)
    
    return {'url':tempUrl, 'provider':provider}

def bitlyShortener(url):
    # bitly api call
    bitlyShortener = pyshorteners.Shortener(api_key='99b778a91b033bb2557f85a50dc245e99ea94798')
    url = bitlyShortener.bitly.short(url)

    return url

def tinyurlShortener(url):
    # tinyurl url
    res = requests.get('https://tinyurl.com/api-create.php?url=' + url)
    url = res.text

    return url
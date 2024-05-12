import requests


def test_proxy():
    proxy = {
        'http': 'http://localhost:7890',
        'https': 'http://localhost:7890'
    }
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxy)
        print('Proxy is working. Response:', response.text)
    except requests.exceptions.ProxyError as e:
        print('Proxy error:', e)
    except requests.exceptions.ConnectionError as e:
        print('Connection error:', e)


test_proxy()

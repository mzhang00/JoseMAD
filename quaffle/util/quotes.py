import urllib3
import json

http = urllib3.PoolManager()

def json2dict(jsonString):
    return json.loads(jsonString)

def dict2json(dict):
    return json.dump(dict)

def quotes():
    request = http.request("GET", "https://api.quotable.io/random")
    return request.data.decode('utf-8')

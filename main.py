import urllib, json
from framework import bottle
from framework.bottle import route, template, request, error, debug, response
from google.appengine.ext.webapp.util import run_wsgi_app

@route('/')
def index():
    return template('templates/home')

def main():
    debug(True)
    run_wsgi_app(bottle.default_app())


@route('/twilio', method='POST')
def ProcessSearch():
    UPC = request.POST.get('Body')
    url = "https://www.googleapis.com/shopping/search/v1/public/products?key=AIzaSyDhTDNo58Dt8Kx3Ig3eFDxyfKhv2MwvRv8&country=US&restrictBy=gtin:%s&rankBy=price:ascending" % UPC
    data = urllib.urlopen(url).read()
    d = json.loads(data)
    title = d["items"][0]["product"]["title"]
    price = d["items"][0]["product"]["inventories"][0]["price"]

    response.content_type = 'text/xml'

    values = {'title':title, 'price':price}

    return template('templates/twilio', data = values)


@error(403)
def Error403(code):
    return 'Get your codes right dude, you caused some error!'

@error(404)
def Error404(code):
    return 'Stop cowboy, what are you trying to find?'

if __name__=="__main__":
    main()
#coding: utf-8
from hashlib import sha1
from hmac import new as hmac
from xml.etree import ElementTree
import math
import os
import random
import requests
import datetime


URL = 'cidadao.sinesp.gov.br'
SECRET = '#8.1.0#g8LzUadkEHs7mbRqbX5l'


class RequestTimeout(Exception):
    pass

class InvalidResponse(Exception):
    pass

class SinespClient(object):
    """
    This makes possible to consult SINESP Cidadão database without needing
    to authenticate or fill captcha tests.

    SINESP Cidadão is a Brazilian public database of national vehicles. It's
    very useful to identify suspicious and stolen cars or motorcycles.

    We don't know why but government does not maintain a public API for this
    service. The only way to access this information is to access the SINESP
    site and answer captchas for every request. Hopefully they provide Android
    and iOS applications that make it possible to search for vehicles without
    needing to complete captcha tests. We have then reverse engineered their
    Android app APK file and discovered how to get our data without dealing
    with boring captchas.
    """
    def __init__(self, proxy_address=None, proxy_port=None, timeout=None):
        """
        SINESP only accepts national web requests. If you don't have a valid
        Brazilian IP address you could use a web proxy (SOCKS5).
        """
        self._proxies = None
        if proxy_address and proxy_port:
            self._proxies = {"https": "https://%s:%s" % (
                proxy_address, proxy_port)}

        # Read and store XML template for our HTTP request body.
        body_file = open(os.path.join(os.path.dirname(__file__), 'body.xml'))
        self._body_template = body_file.read()
        body_file.close()
        self._timeout = timeout


    def _token(self, plate):
        """Generates SHA1 token as HEX based on specified and secret key."""
        plate_and_secret = '%s%s' % (plate, SECRET)
        plate_and_secret = bytes(plate_and_secret.encode('utf-8'))
        plate = plate.encode('utf-8')
        hmac_key = hmac(plate_and_secret, plate, sha1)
        return hmac_key.hexdigest()


    def _rand_coordinate(self, radius=2000):
        """Generates random seed for latitude and longitude coordinates."""
        seed = radius/111000.0 * math.sqrt(random.random())
        seed = seed * math.sin(2 * 3.141592654 * random.random())
        return seed


    def _rand_latitude(self):
        """Generates random latitude."""
        return '%.7f' % (self._rand_coordinate() - 38.5290245)


    def _rand_longitude(self):
        """Generates random longitude."""
        return '%.7f' % (self._rand_coordinate() - 3.7506985)

    def _date(self):
        """Returns the current date formatted as yyyy-MM-dd HH:mm:ss"""
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    def _body(self, plate):
        """Populate XML request body with specific data."""
        token = self._token(plate)
        latitude = self._rand_latitude()
        longitude = self._rand_longitude()
        date = self._date()
        return self._body_template % (latitude, token, longitude, date, plate)

    def _captcha_cookie(self):
        """Performs a captcha request and return the cookie."""
        cookies = requests.get('https://sinespcidadao.sinesp.gov.br/sinesp-cidadao/captchaMobile.png', proxies=self._proxies, verify=False).cookies
        jsessionid = cookies.get('JSESSIONID')
        return {'JSESSIONID': jsessionid}


    def _request(self, plate):
        """Performs an HTTP request with a given content."""
        url = ('https://cidadao.sinesp.gov.br/sinesp-cidadao/'
               'mobile/consultar-placa/v4')
        data = self._body(plate)
        cookies = self._captcha_cookie()
        headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Cache-Control': 'no-cache',
            'Content-Length': '661',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'sinespcidadao.sinesp.gov.br',
            'User-Agent': 'SinespCidadao / 3.0.2.1 CFNetwork / 758.2.8 Darwin / 15.0.0',
            'Connection':'close',
        }
        return requests.post(url, data, headers, proxies=self._proxies, cookies=cookies, verify=False, timeout=self._timeout)


    def _parse(self, response):
        """Parses XML result from HTTP response."""
        body_tag = '{http://schemas.xmlsoap.org/soap/envelope/}Body'
        response_tag = ('{http://soap.ws.placa.service.sinesp.serpro.gov.br/}'
                        'getStatusResponse')
        return_tag = 'return'

        try:
            xml = response.decode('latin-1').encode('utf-8')
            xml = ElementTree.fromstring(xml)
            elements = xml.find(body_tag).find(response_tag).find(return_tag)
        except:
            raise InvalidResponse('Could not parse request response.')

        elements = dict(((element.tag, element.text) for element in elements))

        elements = dict(
            return_code=elements.get('codigoRetorno'),
            return_message=elements.get('mensagemRetorno'),
            status_code=elements.get('codigoSituacao'),
            status_message=elements.get('situacao'),
            chassis=elements.get('chassi'),
            model=elements.get('modelo'),
            brand=elements.get('marca'),
            color=elements.get('cor'),
            year=elements.get('ano'),
            model_year=elements.get('anoModelo'),
            plate=elements.get('placa'),
            date=elements.get('data'),
            city=elements.get('municipio'),
            state=elements.get('uf'),
        )

        return elements


    def search(self, plate):
        """
        Searchs for vehicle plate.

        If a vehicle with the specified plate was found, the server returns the
        followign information which we'll repass in a dictionary format:

        - return_code
        - return_message
        - status_code
        - status_message
        - chassis
        - model
        - brand
        - color
        - year
        - model_year
        - plate
        - date
        - city
        - state
        """
        response = self._request(plate).content
        if not response:
            return dict()

        return self._parse(response)

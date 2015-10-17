#coding: utf-8
from hashlib import sha1
from hmac import new as hmac
from xml.etree import ElementTree
import math
import os
import random
import socket
import socks

URL = 'sinespcidadao.sinesp.gov.br'
SECRET = 'shienshenlhq'

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
    def __init__(self, proxy_address=None, proxy_port=None):
        """
        SINESP only accepts national web requests. If you don't have a valid
        Brazilian IP address you could use a web proxy (SOCKS5).
        """
        if proxy_address and proxy_port:
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, 
                                  proxy_address, proxy_port)
            socket.socket = socks.socksocket
            # Web proxies may be slower than regular connections.
            socket.setdefaulttimeout(30)

        # Read and store XML template for our HTTP request body.
        body_file = open(os.path.join(os.path.dirname(__file__), 'body.xml'))
        self._body = body_file.read().replace('\n', ' ').replace('  ', '')
        body_file.close()


    def _token(self, plate):
        """Generates SHA1 token as HEX based on specified and secret key."""
        return hmac(SECRET, plate, sha1).digest().encode('hex')


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


    def _content(self, plate):
        """Generates HTTP request based on a given plate."""
        token = self._token(plate)
        latitude = self._rand_latitude()
        longitude = self._rand_longitude()
        # Filling our body template
        body = self._body % (token, latitude, longitude, plate)
        # General info
        header = 'POST /sinesp-cidadao/ConsultaPlacaNovo27032014 HTTP/1.1\n'
        host = 'Host: sinespcidadao.sinesp.gov.br\n'
        # Content info
        content_length = 'Content-Length: %d\n' % len(body)
        content_type = ('Content-Type: application/x-www-form-urlencoded; '
                        'charset=UTF-8\n\n')
        # Joining everyone and building our HTTP request
        return ''.join((header, host, content_length, content_type, body))


    def _request(self, content):
        """Performs an HTTP request with a given content."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((URL, 80))
        s.send(content)
        response = ''
        buf = s.recv(32)
        while len(buf):
            response += buf
            buf = s.recv(32)

        s.close()
        return response
        
        
    def _parse(self, response):
        """Parses XML result from HTTP response."""
        body_tag = '{http://schemas.xmlsoap.org/soap/envelope/}Body'
        response_tag = ('{http://soap.ws.placa.service.sinesp.serpro.gov.br/}'
                        'getStatusResponse')
        return_tag = 'return'

        try:
            xml = response.split('charset=UTF-8\r\n\r\n')[1]
            xml = ElementTree.fromstring(xml)
            elements = xml.find(body_tag).find(response_tag).find(return_tag)
        except:
            raise InvalidResponse('Could not parse request response.')

        return dict(((element.tag, element.text) for element in elements))


    def search(self, plate):
        """
        Searchs for vehicle plate.
        
        If a vehicle with the specified plate was found, the server returns the
        followign information which we'll repass in a dictionary format:
        
        - codigo_de_retorno (return code)
        - mensagem_de_retorno (return message)
        - codigo_da_situacao (situation code)
        - situacao (situation message)
        - modelo (vehicle model)
        - marca (vehicle brand)
        - cor (vehicle color)
        - ano (vehicle fabrication year)
        - ano_do_modelo (vehicle model year)
        - placa (vehicle plate)
        - data (consult date)
        - uf (Brazilian state/federal unity code)
        - municipio (Brazilian city)
        - chassi (vehicle chassis)
        """
        content = self._content(plate)

        try:
            response = self._request(content)
        except socket.timeout:
            raise RequestTimeout('Request has timed out.')
        
        if not response:
            return dict()

        return self._parse(response)

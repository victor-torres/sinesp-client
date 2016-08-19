# SINESP Client

SINESP Client makes possible to consult SINESP Cidadão database without needing to authenticate or fill captcha tests.

[![Make a donation](https://www.paypalobjects.com/pt_BR/BR/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=54V3L3LBX8VQU)


## What's SINESP

SINESP Cidadão is a Brazilian public database of national vehicles. It's very useful to identify suspicious and stolen cars or motorcycles.


## Available data

If a vehicle with the specified plate was found, the server returns the followign information which we'll repass in a dictionary format:

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


## Why build a SINESP client?

We don't know why but government does not maintain a public API for this service. The only way to access this information is accessing the SINESP site and answering captchas for every request.


## What have we done

Hopefully they provide Android and iOS applications that make it possible to search for vehicles without needing to complete captcha tests. We have then reverse engineered their Android app APK file and discovered how to get our data without dealing with boring captchas.


## Usage

### Installing

```shell
python setup.py install
```

### Normal usage

```python
from sinesp_client import SinespClient
sc = SinespClient()
result = sc.search('ABC1234')
```

### With proxy

SINESP may only accept national web requests. If you don't have a valid Brazilian IP address and you're dealing with some connection problems you can try to use a web proxy (SOCKS5).

```python
from sinesp_client import SinespClient
sc = SinespClient(proxy_address="127.0.0.1", proxy_port=8080)
result = sc.search('ABC1234')
```

Note: do use a valid SOCKS5 proxy address and port values.

## Author

Victor Torres <vpaivatorres@gmail.com>

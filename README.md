# SINESP Client [![PyPI Version](https://img.shields.io/pypi/v/sinesp-client.svg)](https://pypi.python.org/pypi/sinesp-client)

SINESP Client torna possível a consulta da base de dados do SINESP Cidadão sem a necessidade do preenchimento de captchas ou algum outro tipo de autenticação.

[![Make a donation](https://www.paypalobjects.com/pt_BR/BR/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=54V3L3LBX8VQU)


## O que é o SINESP

SINESP Cidadão é uma base de dados pública de veículos brasileiros. É muito útil para identificar carros ou motos roubados ou suspeitos.


## Informações disponíveis

Se um veículo com a placa especificada for encontrado, o servidor irá retornar as seguintes informações que serão repassadas através de um dicionário:

- return_code (código de retorno)
- return_message (mensagem de retorno)
- status_code (código do status)
- status_message (mensagem do status)
- chassis (chassi do veículo)
- model (modelo/versão)
- brand (marca/fabricante)
- color (cor/pintura)
- year (ano de fabricação)
- model_year (ano do modelo)
- plate (placa)
- date (data e hora da consulta)
- city (cidade)
- state (estado ou unidade federativa)


## Por que fazer um cliente do SINESP?

Não sabemos o porquê, mas o governo não mantém uma API pública para este serviço. A única maneira de acessar os dados é acessando o site do SINESP e respondendo a perguntas de verificação (captchas) para cada uma das requisições.


## O que nós fizemos

Felizmente as aplicações para Android e iOS permitem que a busca seja feita sem que seja preciso responder a nenhum teste captcha. Nós então fizemos uma engenharia reversa no aplicativo para que pudéssemos ter acesso a essas informações públicas sem que fosse preciso responder a esses captchas chatos.


## Utilizando

### Instalando

Através do PyPI

```shell
pip install sinesp-client
```

Ou a partir do código-fonte

```shell
python setup.py install
```

### Utilização normal

```python
from sinesp_client import SinespClient
sc = SinespClient()
result = sc.search('ABC1234')
```

### Com proxy

O SINESP pode bloquear conexões vindas de fora do país. Se acontecer de você estar enfrentando problemas de conexões você pode tentar utilizar um web proxy (SOCKS5), que podem ser encontrados gratuitamente na Internet.

```python
from sinesp_client import SinespClient
sc = SinespClient(proxy_address='127.0.0.1', proxy_port=8080)
result = sc.search('ABC1234')
```

Nota: Utilize valores de endereço e porta válidos.

### Chamando um script Python através do PHP

Atendendo a diversos pedidos que vêm chegando por e-mail, [neste artigo na Wiki do projeto](https://github.com/victor-torres/sinesp-client/wiki/Como-executar-o-código-Python-no-PHP) ensino a chamar um script simples feito em Python, que retorna os dados obtidos em formato JSON, e a acessar os dados obtidos através do PHP.

## Contribua

O livre acesso a esses dados públicos permite que diversas aplicações sejam desenvolvidas, muitas delas com um potencial benefício social envolvido como retorno. Ajude a contribuir com o projeto:

- [Faça uma doação](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=54V3L3LBX8VQU)
- Contribua com o código-fonte
- Se você for o governo, por favor, libere uma API pública para nós brasileiros

## Autor

- Victor Torres [@victor-torres](https://github.com/victor-torres)

## Contribuidores

- Giovani Generali [@giovanigenerali](https://github.com/giovanigenerali)
- Francesco Perrotti-Garcia [@fpg1503](https://github.com/fpg1503)
- William Monteiro [@monteirosk](https://github.com/monteirosk)
- Ricardo Tominaga [@ricardotominaga](https://github.com/ricardotominaga)
- Pedro Vilela [@pedrovilela](https://github.com/pedrovilela)
- Lúcio Corrêa [@luciocorrea](https://github.com/luciocorrea)
- Marcos Said

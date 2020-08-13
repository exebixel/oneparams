# ONEPARAMS

[![Pypi](https://img.shields.io/pypi/v/oneparams.svg?style=plastic)](https://pypi.org/project/oneparams/)

Uma CLI relativamente simples para automatizar os processos de parametrização dos sistemas [ONE BELEZA](https://onebeleza.com.br)


Instalação
----------

Para instalar o oneparams é necessario ter o Python com uma versão acima da 3.6 e o pip instalados no seu computador.

### Windows

Para instalar o Python e o pip no windowns [clique aqui](https://python.org.br/instalacao-windows/).

### Linux

Debian/Ubuntu:
```
$ sudo apt install python3 python3-pip
```

Fedora:
```
$ sudo yum install python3 python3-pip
```

### OneParams

Depois de instalar o python e o pip em seu sistema, abra um terminal e digite:
```
$ pip install oneparams
```


Como Usar
---------

O oneparams precisa do modo (o que ele vai fazer) o nome da empresa, email e senha se ela for diferente de 123456 e claro da planilha de parametrização que sera lida

O oneparams tem 4 modulos:

 - `serv`  para manipular serviços;

 - `cols`  para manipular os colaboradores;

 - `comm`  para manupular as comissões (sem suporte a comissões diferenciadas);

 - `card`  para manipular os cartões


Cada modulo precisa:
 -  do nome da empresa `--empresa` ou `-e`
 -  do email de login `--login` ou `-l`
 -  da senha `--password` ou `-p`, isso se a senha for diferente de 123456
 -  e claro da planilha de parametrização

Tambem existem algums parametros opcionais como: 
 - `--reset` ou `-R` que serve para deletar todos os cadastros do modulo (não disponivel para ` cols`)
 - `--app` ou `-a` que cria o cadastro dos colaboradores no app ONE BELEZA (disponivel apenas para o `cols`)

### Exemplos

Para deletar todos os serviços cadastrados e cadastrar os serviços na planilha
```
$ one serv -l emailteste@one.com -e "teste mmtools" planilha.xlsx -R
```

se quiser apenas cadastrar os serviços da planilha basta tirar o `-R`, assim:
```
$ one serv -l emailteste@one.com -e "teste mmtools" planilha.xlsx
```

e alterando o modulo `serv` para `cols`, `card` ou `comm` é possivel usar as outras funções do oneparams


Sobre mim
---------

Qualquer duvida podem entrar em contato comigo!

Telegram: [@exebixel](https://t.me/exebixel)

Email: ezequielnat7@gmail.com

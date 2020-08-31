# ONEPARAMS

[![Pypi](https://img.shields.io/pypi/v/oneparams.svg?style=plastic)](https://pypi.org/project/oneparams/)

Uma CLI relativamente simples para automatizar os processos de parametrização dos sistemas [ONE BELEZA](https://onebeleza.com.br)


Instalação
----------

Para instalar o Oneparams é necessário ter o Python com uma versão acima da 3.6 e o Pip instalados no seu computador.

### Windows

Para instalar o Python e o Pip no Windowns [clique aqui](https://python.org.br/instalacao-windows/).

### Linux

Debian/Ubuntu:
```
$ sudo apt install python3 python3-pip
```

Fedora:
```
$ sudo yum install python3 python3-pip
```
Depois só falta adicionar o diretório``~/.local/bin`` a sua variavel  ``PATH``, adicionando essa linha no seu ``~/.bashrc`` ou ``~/.zshrc``:
```
export PATH="$PATH:$HOME/.local/bin"
```

### OneParams

Depois de instalar o Python e o Pip em seu sistema, abra um terminal e digite:
```
$ pip install oneparams
```


Como Usar
---------

O Oneparams precisa do módulos (o que ele vai fazer) o nome da empresa, email e senha se ela for diferente da senha padrão e claro da planilha de parametrização que sera lida

O Oneparams tem 4 módulos:

 - `serv`  para manipular serviços;

 - `cols`  para manipular os colaboradores;

 - `comm`  para manipular as comissões (sem suporte a comissões diferenciadas);

 - `card`  para manipular os cartões


Cada módulo precisa:
 -  do nome da empresa `--empresa` ou `-e`
 -  do email de login `--login` ou `-l`
 -  da senha `--password` ou `-p`, isso se a senha for diferente da senha padrão
 -  e claro da planilha de parametrização

Também existem alguns parâmetros opcionais como: 
 - `--reset` ou `-R` que serve para deletar todos os cadastros do modulo (não disponível para ` cols`)
 - `--app` ou `-a` que cria o cadastro dos colaboradores no app ONE BELEZA (disponível apenas para o `cols`)

### Exemplos

Para deletar todos os serviços cadastrados e cadastrar os serviços na planilha
```
$ one serv -l emailteste@one.com -e "teste mmtools" planilha.xlsx -R
```

Se quiser apenas cadastrar os serviços da planilha basta tirar o `-R`, assim:
```
$ one serv -l emailteste@one.com -e "teste mmtools" planilha.xlsx
```

E alterando o modulo `serv` para `cols`, `card` ou `comm` é possível usar as outras funções do Oneparams


Sobre mim
---------

Qualquer duvida podem entrar em contato comigo!

Telegram: [@exebixel](https://t.me/exebixel)

Email: ezequielnat7@gmail.com

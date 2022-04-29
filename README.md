# ONEPARAMS

[![Pypi](https://img.shields.io/pypi/v/oneparams.svg?style=plastic)](https://pypi.org/project/oneparams/)

Uma CLI relativamente simples para automatizar os processos de parametrização dos sistemas [ONE BELEZA](https://onebeleza.com.br)


Instalação
----------

Para instalar o OneParams é necessário ter o Python com uma versão acima da 3.7 e o Pip instalados no seu computador.

### Windows

Para instalar o Python e o Pip no Windows [clique aqui](https://python.org.br/instalacao-windows/).

### Linux

Debian/Ubuntu:
```bash
$ sudo apt install python3 python3-pip
```

Fedora:
```bash
$ sudo dnf install python3 python3-pip
```
Depois só falta adicionar o diretório``~/.local/bin`` a sua variável  ``PATH``, adicionando essa linha no seu ``~/.bashrc`` ou ``~/.zshrc``:
```bash
export PATH="$PATH:$HOME/.local/bin"
```

### OneParams

Depois de instalar o Python e o Pip em seu sistema, abra um terminal e digite:
```bash
$ pip install oneparams
```


Como Usar
---------

O OneParams precisa do módulos (o que ele vai fazer) o nome da empresa, email e senha se ela for diferente da senha padrão e claro da planilha de parametrização que sera lida

O OneParams tem 6 módulos:

 - `serv`  para manipular serviços;

 - `cols`  para manipular os colaboradores;

 - `comm`  para manipular as comissões (sem suporte a comissões diferenciadas);

 - `card`  para manipular os cartões

 - `clis`  para manipular os clientes

 - `reset` para resetar senhas de emails


Cada módulo (exceto `reset`) precisa:
 -  do nome da empresa `--empresa` ou `-e`
 -  do email de login `--login` ou `-l`
 -  da senha `--password` ou `-p`, isso se a senha for diferente da senha padrão
 -  e claro da planilha de parametrização

Também existem alguns parâmetros opcionais como:
 - `--reset` ou `-R` que serve para deletar todos os cadastros do modulo (não disponível para ` cols`)
 - `--no-warning` ou `-W` onde você pode retirar os avisos (warnings) do OneParams
 - `--no-erros` ou `-E` que implementa uma forma mais simples que resolução automática de erros (disponível apenas para o `clis` e `comm`)
 - `--skip` ou `-S` que caso o nome do cadastro da planilha já exista no banco de dados do cliente, esse cadastro é "pulado" (disponível apenas para o `clis`)

### Exemplos

Para deletar todos os serviços cadastrados e cadastrar os serviços na planilha
```bash
$ one serv -l emailteste@one.com -e "nome da empresa" planilha.xlsx -R
```

Se quiser apenas cadastrar os serviços da planilha basta tirar o `-R`, assim:
```bash
$ one serv -l emailteste@one.com -e "nome da empresa" planilha.xlsx
```

E alterando o modulo `serv` para `cols`, `card`, `comm` ou `clis` é possível usar as outras funções do OneParams


Documentação
-------------

Para mais informações sobre o OneParams, veja a [wiki do projeto](https://github.com/exebixel/oneparams/wiki)

Sobre mim
---------

Qualquer duvida podem entrar em contato comigo!

Telegram: [@exebixel](https://t.me/exebixel)

Email: ezequielnat7@gmail.com

# ONEPARAMS

[![Pypi](https://img.shields.io/pypi/v/oneparams.svg?style=plastic)](https://pypi.org/project/oneparams/)

Uma CLI relativamente simples para automatizar os processos de parametrização dos sistemas [ONE BELEZA](https://onebeleza.com.br)


Instalação
----------

Para instalar o Oneparams é necessário ter o Python com uma versão acima da 3.6 e o Pip instalados no seu computador.

### Windows

Para instalar o Python e o Pip no Windows [clique aqui](https://python.org.br/instalacao-windows/).

### Linux

Debian/Ubuntu:
```
$ sudo apt install python3 python3-pip
```

Fedora:
```
$ sudo yum install python3 python3-pip
```
Depois só falta adicionar o diretório``~/.local/bin`` a sua variável  ``PATH``, adicionando essa linha no seu ``~/.bashrc`` ou ``~/.zshrc``:
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

O Oneparams tem 6 módulos:

 - `serv`  para manipular serviços;

 - `cols`  para manipular os colaboradores;

 - `comm`  para manipular as comissões (sem suporte a comissões diferenciadas);

 - `card`  para manipular os cartões

 - `clis`  para manipular os clientes (modulo beta)

 - `reset` para resetar senhas de emails


Cada módulo (exceto `reset`) precisa:
 -  do nome da empresa `--empresa` ou `-e`
 -  do email de login `--login` ou `-l`
 -  da senha `--password` ou `-p`, isso se a senha for diferente da senha padrão
 -  e claro da planilha de parametrização

Também existem alguns parâmetros opcionais como:
 - `--reset` ou `-R` que serve para deletar todos os cadastros do modulo (não disponível para ` cols`)
 - `--no-warning` ou `-W` onde você pode retirar os avisos (warnings) do Oneparams
 - `--no-erros` ou `-E` que implementa uma forma mais simples que resolução automática de erros (disponível apenas para o `clis`)
 - `--skip` ou `-S` que caso o nome do cadastro da planilha já exista no banco de dados do cliente, esse cadastro é "pulado" (disponível apenas para o `clis`)

### Exemplos

Para deletar todos os serviços cadastrados e cadastrar os serviços na planilha
```
$ one serv -l emailteste@one.com -e "teste mmtools" planilha.xlsx -R
```

Se quiser apenas cadastrar os serviços da planilha basta tirar o `-R`, assim:
```
$ one serv -l emailteste@one.com -e "teste mmtools" planilha.xlsx
```

E alterando o modulo `serv` para `cols`, `card`, `comm` ou `clis` é possível usar as outras funções do Oneparams

### Reset

Para utilização do modulo `reset` é necessario ter uma chave de acesso, essa chave deve ser definida como uma variavel de ambiente

Para definir a variavel de ambiente:

No Linux adicione a linha abaixo ao seu `~/.bashrc`:
``` code:sh
export ONE_RESET="<your-key>"
```

No Windows, abra o cmd como Administrator e utilize o comando abaixo:
```
setx ONE_RESET "<your-key>" /M
```

Depois de definida a chave de acesso, basta usar o comando abaixo para resetar a senha de um acesso
``` code:sh
one reset <email>

one reset teste@teste.com
```

Caso tudo dê certo, o comando deve retornar o nome, email e a nova senha do usuario

Sobre mim
---------

Qualquer duvida podem entrar em contato comigo!

Telegram: [@exebixel](https://t.me/exebixel)

Email: ezequielnat7@gmail.com

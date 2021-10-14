import click
import requests
import json
import re
import sys


def pw_reset(email, acess_key):

    r = re.compile(r'^[\w\.-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$',
                flags=re.ASCII)
    if r.search(email) == None:
        sys.exit("ERROR! email invalid!!");

    header = {
        'Content-Type': 'application/json',
        'Authorization': f'bearer {acess_key}'
    }

    try:
        response =  requests.patch("https://oneapicentraldecontrole.azurewebsites.net/api/UsuariosMob/RecuperarSenha",
                            headers=header,
                            data=json.dumps(email))
    except requests.exceptions.ConnectionError:
        sys.exit("Connection error!!\nCheck your internet connection")

    if response.ok:
        content = json.loads(response.content)
        if content["data"] != None:
            click.echo(f'Usuario: {content["data"]["nome"]}')
            click.echo(f'Email: {content["data"]["email"]}')
            click.echo("Senha: 123456")
    elif response.status_code == 401:
        click.echo("ERROR: 401 Unauthorized, You do not have permission to access this module.")
    else:
        click.echo(f'ERROR! {response.status_code}')
        click.echo(response.content)

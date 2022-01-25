import json
import re
import sys

import click
import requests


def pw_reset(email: str, acess_key: str) -> None:

    regex = re.compile(r'^[\w\.-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$',
                       flags=re.ASCII)
    if regex.search(email) is None:
        sys.exit("ERROR! email invalid!!")

    header = {
        'Content-Type': 'application/json',
        'Authorization': f'bearer {acess_key}'
    }

    try:
        response = requests.patch(
            "https://oneapicentraldecontrole.azurewebsites.net/api/UsuariosMob/RecuperarSenha",
            headers=header,
            data=json.dumps(email))
    except requests.exceptions.ConnectionError:
        sys.exit("Connection error!!\nCheck your internet connection")

    if response.ok:
        content = json.loads(response.content)
        if content["data"] is not None:
            click.echo(f'User: {content["data"]["nome"]}')
            click.echo(f'Email: {content["data"]["email"]}')
            click.echo("Password: 123456")
        else:
            click.echo(f"ERROR! Email {email} not registered in app")
    elif response.status_code == 401:
        click.echo(
            "ERROR: 401 Unauthorized, You do not have permission to access this module."
        )
    else:
        click.echo(f'ERROR! {response.status_code}')
        click.echo(response.content)

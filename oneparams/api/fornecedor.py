import json

from oneparams.api.base import BaseApi
from oneparams.utils import create_cel, create_email


class Fornecedor(BaseApi):
    """
    classe de gerenciamento de fornecedores da one,
    sua principal função é criar e pesquisar fornecedores
    """
    def __init__(self):
        self.__fornecedores = []
        self.all_fornecedores()

    def all_fornecedores(self):
        """
        Pega todos os fornecedores cadastrados no sistema,
        e preenche o atributo self.__fornecedores com nome e id
        """
        print("researching supplier")
        response = self.get("/CliForCols/ListaDetalhesFornecedores")
        self.status_ok(response)

        content = json.loads(response.content)
        for i in content:
            self.__fornecedores.append({
                "id": i["cliForColsId"],
                "nome": i["nomeCompleto"]
            })

    def get_id(self, nome):
        """
        Retorna o id de um fornecedor,
        o nome do fornecedor tem que ser exatamente igual,
        se não encontrar o id do fornecedor, retorna None
        """
        for i in self.__fornecedores:
            if i["nome"] == nome:
                return i["id"]
        return None

    def create(self, nome):
        """
        Cria um fornecedor,
        Dados de criação padrão:
        data={
            "ativoFornecedor": "true",
            "flagCliente": "false",
            "flagColaborador": "false",
            "email": gerado aleatoriamente,
            "celular": gerado aleatoriamente,
            "nomeCompleto": nome (parâmetro)
        }
        """
        print("creating {} supplier".format(nome))
        response = self.post("/OCliForColsUsuarioPerfil/CreateFornecedores",
                             data={
                                 "ativoFornecedor": "true",
                                 "flagCliente": "false",
                                 "flagColaborador": "false",
                                 "email": create_email(),
                                 "celular": create_cel(),
                                 "nomeCompleto": nome
                             })
        self.status_ok(response)
        content = json.loads(response.content)
        self.__fornecedores.append({"id": content["data"], "nome": nome})
        return content["data"]

    def get_for(self, nome):
        """
        Retorna o id de um fornecedor com base em seu nome,
        se o fornecedor não existir, ele será criado
        """
        for_id = self.get_id(nome)
        if for_id is None:
            for_id = self.create(nome)
        return for_id

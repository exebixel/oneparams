import json

from oneparams.api.base_diff import BaseDiff
from oneparams.utils import create_cel, create_email


class ApiFornecedor(BaseDiff):
    """
    classe de gerenciamento de fornecedores da one,
    sua principal função é criar e pesquisar fornecedores
    """
    items = {}
    first_get = False

    def __init__(self):
        super().__init__(
            key_id="fornecedorId",
            key_name="nomeCompleto",
            key_active="ativoFornecedor",
            item_name="supplier",
            url_get_all="/CliForCols/ListaDetalhesFornecedores",
            url_create="/OCliForColsUsuarioPerfil/CreateFornecedores"
        )

        if not ApiFornecedor.first_get:
            self.get_all()
            ApiFornecedor.first_get = True

    def get_all(self):
        """
        Pega todos os fornecedores cadastrados no sistema,
        e preenche o atributo self.__fornecedores com nome e id
        """
        print("researching supplier")
        response = self.get("/CliForCols/ListaDetalhesFornecedores")
        self.status_ok(response)

        content = json.loads(response.content)
        ApiFornecedor.items = {}
        for i in content:
            ApiFornecedor.items[i["cliForColsId"]] = {
                self.key_id: i["cliForColsId"],
                self.key_name: i[self.key_name],
                self.key_active: i[self.key_active],
                "email": i["email"],
                "celular": i["celular"]
            }

    def create(self, data: dict) -> int:
        if self.key_active not in data:
            data[self.key_active] = True
        if "flagCliente" not in data:
            data["flagCliente"] = False
        if "flagColaborador" not in data:
            data["flagColaborador"] = False
        if "email" not in data:
            data["email"] = create_email()
        if "celular" not in data:
            data["celular"] = create_cel()
        return super().create(data)

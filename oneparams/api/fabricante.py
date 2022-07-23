from typing import Dict
from oneparams.api.base_diff import BaseDiff


class ApiFabricante(BaseDiff):

    items: dict = {}
    list_details: dict = {}
    first_get: bool = False

    def __init__(self):
        super().__init__(
            key_id="fabricantesID",
            key_name="nomeFantasia",
            item_name="fabricante",
            url_get_all="/Fabricantes/ListaDetalhesFabricantes",
            url_get_detail="/Fabricantes/DetalhesFabricantes",
            url_create="/Fabricantes/CreateFabricantes",
            url_update="/Fabricantes/UpdateFabricantes",
            url_delete="/Fabricantes/DeleteFabricante",
            handle_errors={
                "API.FABRICANTES.DELETE.REFERENCE": "Cant delete fabricante..."
            }
        )

        if not ApiFabricante.first_get:
            self.get_all()
            ApiFabricante.first_get = True

    def get_all(self) -> Dict:
        items = super().get_all()
        ApiFabricante.items = {}
        for i in items:
            self.items[i[self.key_id]] = {
                self.key_id: i[self.key_id],
                self.key_name: i[self.key_name],
            }
        return self.items

    def add_item(self, data: dict, response: dict) -> int:
        data = {self.key_name: data[self.key_name]}
        return super().add_item(data, response)

    def create(self, data: dict) -> int:
        if "telefoneComercial" not in data:
            data["telefoneComercial"] = "00000000"
        if "cpF_CNPJ" not in data:
            data["cpF_CNPJ"] = "00000000000000"

        return super().create(data)

    def update(self, data: dict) -> int:
        if "telefoneComercial" not in data:
            telefone = self.details(data[self.key_id])["telefoneComercial"]
            data["telefoneComercial"] = telefone
        if "cpF_CNPJ" not in data:
            cpf_cnpj = self.details(data[self.key_id])["cpF_CNPJ"]
            data["cpF_CNPJ"] = cpf_cnpj

        return super().update(data)

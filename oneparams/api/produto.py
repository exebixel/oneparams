from oneparams.api.base_diff import BaseDiff
from oneparams.api.linha_produto import ApiLinhaProduto
from oneparams.api.grupo_produto import ApiGrupoProduto
from oneparams.api.fabricante import ApiFabricante


class ApiProdutos(BaseDiff):
    """
    Gerenciamento do produtos
    cria, atualiza, deleta e inativa produtos
    """
    items: dict = {}
    list_details: dict = {}
    first_get: bool = False
    name_list: dict = {}

    def __init__(self):
        super().__init__(key_id="produtosId",
                         key_name="descricao",
                         item_name="product",
                         keys_search=["descricao"],
                         url_create="/OProdutos/CreateProdutosOneParams",
                         url_update="/OProdutos/UpdateProdutosOneParams",
                         url_get_all="/OProdutos/ListaDetalhesProdutos",
                         url_get_detail="/OProdutos/DetalhesProdutosOneParams",
                         url_delete="/OProdutos/DeleteProduto",
                         url_inactive="/OProdutos/UpdateProdutosOneParams",
                         key_active="ativo",
                         submodules={
                             "linhasId": ApiLinhaProduto(),
                             "gruposId": ApiGrupoProduto(),
                             "fabricantesId": ApiFabricante()
                         },
                         handle_errors={
                             "API.OPRODUTOS.DELETE.REFERENCE":
                             "Cant delete product {id} - '{name}'..."
                         })

        if not ApiProdutos.first_get:
            self.get_all()
            ApiProdutos.first_get = True

    def get_all(self):
        ApiProdutos.items = {}
        ApiProdutos.name_list = {}
        return super().get_all()

    def add_item(self, data: dict, response: dict) -> int:
        data = {
            self.key_name: data[self.key_name],
            self.key_active: data[self.key_active]
        }
        return super().add_item(data, response)

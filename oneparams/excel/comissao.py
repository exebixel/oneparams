import oneparams.config as config
import pandas as pd
from alive_progress import alive_bar
from oneparams.api.colaborador import ApiColaboradores
from oneparams.api.commission import ApiCommission
from oneparams.api.profissao import Profissao
from oneparams.excel.excel import Excel
from oneparams.utils import get_names


class Comissao():
    def __init__(self, book, reset=False):
        self.erros = False
        if config.RESOLVE_ERROS:
            one = ApiCommission()
            one.cols.get_all_details()
        self.comissao(book=book, reset=reset)

    def comissao(self, book, reset=False):
        print("analyzing spreadsheet")

        ex = Excel(book, "servico")
        ex.add_column(key="servId", name="nome")
        ex.add_column(key="colsId", name="profissionais")
        ex.clean_columns()
        ex.add_row_column()

        one = ApiCommission()

        data_all = ex.data_all(check_final=self.checks_comm)

        len_data = len(data_all)

        if reset:
            one.get_all()
            len_data += one.len()

        config.config_bar()
        with alive_bar(len_data) as bar:
            if reset:
                for cols in list(one.items):
                    for serv in list(one.items[cols]):
                        one.delete(one.items[cols][serv])
                        bar()

            for row in data_all:
                one.comissao(row)
                bar()

    def checks_comm(self, self_excel, data: pd.DataFrame) -> pd.DataFrame:
        # retira linhas que não tenham colaboradores
        data = data.loc[data["colsId"].notnull()]
        # transforma o nome do serviço em id
        data = data.apply(self.get_serv_id, axis=1)

        final_data = pd.DataFrame()
        for i in data.iterrows():
            final_data = final_data.append(self.cols_names_to_id(i[1]))

        if self.erros:
            raise Exception
        return final_data

    def get_serv_id(self, data):
        api = ApiCommission()
        id = api.serv.item_id(
            {api.serv.key_name: data["servId"]})
        if id == 0:
            print("ERROR!! in line {}: Service {} not found".format(
                data["row"], data["servId"]))
            self.erros = True
        data["servId"] = id
        return data

    def cols_with_profession_name(self, profession_name: str) -> list:
        api_profession = Profissao()

        try:
            profession_id = api_profession.submodule_id(
                profession_name, min_similar=0.8)
        except ValueError as exp:
            raise ValueError(exp)

        cols = ApiColaboradores()
        ids = []
        for key in cols.items_active().keys():
            if cols.details(key)["profissaoId"] == profession_id:
                ids.append(key)
        return ids

    def cols_names_to_id(self, data: pd.DataFrame) -> pd.DataFrame:
        cols = get_names(data["colsId"])

        api = ApiCommission()

        ids = []
        for i in cols:
            try:
                ids.append(api.cols.search_item_by_name(i))
            except ValueError as exp:
                if not config.RESOLVE_ERROS:
                    print("ERROR!! in line {}: {}".format(data["row"], exp))
                    self.erros = True
                else:
                    try:
                        ids.extend(self.cols_with_profession_name(i))
                    except ValueError as exp:
                        print("ERROR!! in line {}: Collaborator/{}".format(
                            data["row"], exp))
                        self.erros = True

        if not self.erros:
            return pd.DataFrame({
                "servId": data["servId"],
                "colsId": ids,
                "row": data["row"]
            })

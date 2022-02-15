import random
import re
import string
import unicodedata
from datetime import datetime
from difflib import SequenceMatcher

from oneparams import config


def deemphasize(word: str) -> str:
    """
    Retorna os caracteres da string em seu equivalente em Latin,
    em outras palavras, tira os acentos da string
    """
    if word is None:
        return word
    word = str(word)
    nfkd = unicodedata.normalize('NFKD', word)
    word = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return word.lower()


def no_space(word: str) -> str:
    """
    Remove espaços em branco de uma string
    """
    return re.sub(r' ', '', word)


def string_normalize(word: str) -> str:
    """
    Retorna todos as letras e números de uma string
    """
    word = deemphasize(word)
    # Retornar a palavra apenas com números, letras e espaço
    return re.sub(r'[^a-zA-Z0-9 \\]', '', word)


def get_names(word: str) -> list:
    """
    Retorna um array de strings com as letras,
    entre caracteres especiais e números
    """
    if word is None:
        return []
    word = deemphasize(word)
    word = re.sub(r" e ", "/", word)
    names = re.findall(r"[a-z? *]+", word)
    for i in names:
        index = names.index(i)
        i = i.strip()
        names[index] = i
    return names


def get_float(srtnum: str) -> float:
    """ Retorna o número de uma string

    Caso a string tenha mais de um número,
    sejá separado por espaço ou algum outro caraptere,
    retorna ValueError
    """
    srtnum = str(srtnum).strip()
    nums = re.findall(r"[0-9?.?,]+", srtnum)
    if len(nums) == 1:
        if "," in nums[0]:
            nums[0] = re.sub(r",", ".", nums[0])
        try:
            nums = float(nums[0])
        except ValueError as exp:
            raise ValueError("No possible convert number") from exp
        return nums

    if len(nums) == 0:
        raise ValueError("Number not found")
    raise ValueError("Number is duplicated")


def get_time(strtime: str) -> list:
    """ Retorna uma lista com as posições de
    home, minuto e segundo da string passada por parametro

    Caso não consiga encontrar um horario valido na string,
    retorna uma Exception
    """
    strtime = str(strtime).strip()
    times = re.findall(r"(1[0-2]|0?[0-9]):([0-5][0-9])(:[0-5][0-9])?", strtime)
    if len(times) == 1:
        time_list = []
        for i in times[0]:
            try:
                i = int(i)
            except ValueError:
                i = 0
            time_list.append(i)
        return time_list

    if len(times) == 0:
        raise TypeError("Time not found")
    raise TypeError("Time is duplicated")


def get_date(strdate: str) -> datetime:
    """ Transforma uma string em datetime
    """
    strdate = str(strdate).strip()
    formats = [
        "%Y-%m-%d 00:00:00",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
    ]

    date = None
    for i in formats:
        try:
            date = datetime.strptime(strdate, i)
            break
        except ValueError:
            continue
    else:
        raise ValueError("Date not found")
    return date


def get_num(word: str) -> str:
    """
    Retorna todos os números de uma string
    """
    return str(''.join(ele for ele in word if ele.isdigit()))


def get_cel(word: str) -> str:
    """
    Retorna os números de uma string,
    verificando se existem 11 ou 9 números na string final,
    Se não tiver o 11 ou 9 números o programa é encerrado
    """
    word = re.sub(r'\.0$', '', str(word))
    cel = get_num(word)
    if len(cel) <= 11 and len(cel) >= 8:
        return cel

    raise ValueError(f"Invalid phone {word}")


def create_email() -> str:
    """
    Retorna um email no padrão,
    one_<alguma_coisa>@onebeleza.com
    onde <alguma_coisa> é composto por 6 caracteres aleatórios
    """
    char_set = string.ascii_lowercase + string.digits
    rand = ''.join(random.sample(char_set * 7, 7))
    return f'one_{rand}@onebeleza.com'


def check_email(email: str) -> str:
    """ Verifica se um email é valido
    """
    if email is None:
        return None
    regex = re.compile(r'^[\w\.-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$',
                       flags=re.ASCII)
    email = no_space(str(email)).lower()

    try:
        return regex.search(email).string
    except AttributeError:
        return None


def get_cpf(numbers: str) -> str:
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return None

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    if cpf == cpf[::-1]:
        return None

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return None
    return "".join(str(c) for c in cpf)


def create_cel() -> str:
    """ Cria uma string de 11 dígitos aleatórios
    """
    return ''.join(random.sample(string.digits * 11, 11))


def card_type(card: str) -> str:
    """
    Retorna 'C' ou 'D' dependendo do parâmetro (card),
    card pode ser 'credito' ou 'debito'
    """
    card = deemphasize(card)
    types = []
    if (re.search("credito", card) or re.search("^c$", card)):
        types.append("C")
    if (re.search("debito", card) or re.search("^d$", card)):
        types.append("D")

    if len(types) == 1:
        return types[0]
    if len(types) == 2:
        return "CD"

    raise TypeError(f"unrecognized card type '{card}'")


def get_bool(value: any) -> bool:
    """
    Recebe uma parâmetro (value) contendo "sim" ou "nao",
    e retorna True ou False
    """
    if isinstance(value, bool):
        return value

    if value == 1:
        return True
    if value == 0:
        return False

    if (string_normalize(value) == "sim" or string_normalize(value) == "s"
            or value == "True"):
        return True
    if (string_normalize(value) == "nao" or string_normalize(value) == "n"
            or value == "False"):
        return False
    return None


def get_sex(value: str) -> str:
    value = str(value).strip().upper()

    if re.search("^M", value):
        return "M"
    if re.search("^F", value):
        return "F"
    return None


def similar(word: str, word_diff: str) -> float:
    """ Retorna um número entre 0 e 1 que mostra o quão
    similar são as duas strings
    """
    return SequenceMatcher(None, word, word_diff).ratio()


def eprint(text: str) -> None:
    """ printa o texto passado caso a opção RESOLVE_ERROS for false
    """
    if not config.RESOLVE_ERROS:
        print(text)


def wprint(text: str) -> None:
    """ printa o texto passado caso a opção NO_WARNING for false
    """
    if not config.NO_WARNING:
        print(text)


def print_error(text: str) -> None:
    """ Caso a opção de RESOLVE_ERROS for false, printa um erro,
    se não caso a opção NO_WARNING for false, printa um warning
    """
    if not config.RESOLVE_ERROS:
        print("ERROR! " + text)
    elif not config.NO_WARNING:
        print("WARNING! " + text)


def print_warning(text: str) -> None:
    """ Printa um warning
    """
    if not config.NO_WARNING:
        print("WARNING! " + text)


def state_to_uf(state_name: str) -> str:
    """ Retorna o UF do estado
    """

    state_name = str(state_name)

    # é importante que o UF esteja em MAIUSCULO
    # # e o estado minusculo e sem acentos
    states = {
        'AC': 'acre',
        'AL': 'alagoas',
        'AP': 'amapa',
        'AM': 'amazonas',
        'BA': 'bahia',
        'CE': 'ceara',
        'DF': 'distrito federal',
        'ES': 'espirito santo',
        'GO': 'goias',
        'MA': 'maranhao',
        'MT': 'mato grosso',
        'MS': 'mato grosso do sul',
        'MG': 'minas gerais',
        'PA': 'para',
        'PB': 'paraiba',
        'PR': 'parana',
        'PE': 'pernambuco',
        'PI': 'piaui',
        'RJ': 'rio de janeiro',
        'RN': 'rio grande do norte',
        'RS': 'rio grande do sul',
        'RO': 'rondonia',
        'RR': 'roraima',
        'SC': 'santa catarina',
        'SP': 'sao paulo',
        'SE': 'sergipe',
        'TO': 'tocantins'
    }
    for uf_state, state in states.items():
        if (state == string_normalize(state_name)
                or string_normalize(uf_state) == string_normalize(state_name)):
            return uf_state

    raise ValueError(f"State {state_name} not found!")

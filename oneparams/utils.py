import random
import re
import string
import unicodedata
from difflib import SequenceMatcher
import oneparams.config as config


def deemphasize(word):
    """
    Retorna os caracteres da string em seu equivalente em Latin,
    em outras palavras, tira os acentos da string
    """
    if word is None:
        return word
    word = str(word)
    nfkd = unicodedata.normalize('NFKD', word)
    word = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return word.lower()


def no_space(word):
    """
    Remove espaços em branco de uma string
    """
    return re.sub(r' ', '', word)


def string_normalize(word):
    """
    Retorna todos as letras e números de uma string
    """
    word = deemphasize(word)
    # Retornar a palavra apenas com números, letras e espaço
    return re.sub(r'[^a-zA-Z0-9 \\]', '', word)


def get_names(word):
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


def get_float(srtnum):
    srtnum = str(srtnum).strip()
    nums = re.findall(r"[0-9?.?,]+", srtnum)
    if len(nums) == 1:
        if "," in nums[0]:
            nums[0] = re.sub(r",", ".", nums[0])
        try:
            nums = float(nums[0])
        except ValueError:
            raise ValueError("No possible convert number")
        return nums
    elif len(nums) == 0:
        raise ValueError("Number not found")
    else:
        raise ValueError("Number is duplicated")


def get_time(strtime):
    strtime = str(strtime).strip()
    times = re.findall(r"(1[0-2]|0?[0-9]):([0-5][0-9])(:[0-5][0-9])?", strtime)
    if len(times) == 1:
        t = []
        for i in times[0]:
            try:
                i = int(i)
            except ValueError:
                i = 0
            t.append(i)
        return t

    elif len(times) == 0:
        raise TypeError("Time not found")
    else:
        raise TypeError("Time is dupĺicated")


def get_num(word):
    """
    Retorna todos os números de uma string
    """
    return str(''.join(ele for ele in word if ele.isdigit()))


def get_cel(word):
    """
    Retorna os números de uma string,
    verificando se existem 11 ou 9 números na string final,
    Se não tiver o 11 ou 9 números o programa é encerrado
    """
    word = re.sub(r'\.0$', '', str(word))
    cel = get_num(word)
    if len(cel) <= 11 and len(cel) >= 8:
        return cel

    raise ValueError("Invalid phone {}".format(word))


def create_email():
    """
    Retorna um email no padrão,
    one_<alguma_coisa>@onebeleza.com
    onde <alguma_coisa> é composto por 6 caracteres aleatórios
    """
    char_set = string.ascii_lowercase + string.digits
    rand = ''.join(random.sample(char_set * 7, 7))
    return f'one_{rand}@onebeleza.com'


def check_email(email):
    if email is None:
        return False
    r = re.compile(r'^[\w\.-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$',
                   flags=re.ASCII)
    email = no_space(email)
    return r.search(email) is not None


def create_cel():
    """
    Cria uma string de 11 dígitos aleatórios
    """
    return ''.join(random.sample(string.digits * 11, 11))


def card_type(card):
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

    raise TypeError("unrecognized card type {}".format(card))


def get_bool(value):
    """
    Recebe uma parâmetro (value) contendo "sim" ou "nao",
    e retorna True ou False
    """
    if value == True or value == False:
        return value
    if value == 1:
        return True
    if value == 0:
        return False

    if value == "True":
        return True
    if value == "False":
        return False

    if (string_normalize(value) == "sim" or string_normalize(value) == "s"):
        return True
    if (string_normalize(value) == "nao" or string_normalize(value) == "n"):
        return False
    return None


def similar(word, word_diff):
    return SequenceMatcher(None, word, word_diff).ratio()


def eprint(text):
    if not config.RESOLVE_ERROS:
        print(text)


def wprint(text):
    if not config.NO_WARNING:
        print(text)

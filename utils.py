import unicodedata, re, sys
import random, string
from datetime import datetime

def string_normalize(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    palavra = re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)
    return palavra.lower()

def get_num(x):
    return str(''.join(ele for ele in x if ele.isdigit()))

def get_cel(x):
    x = re.sub('\.0$', '', x)
    cel = get_num(x)
    if len(cel) == 11:
        return cel[:11]
    elif len(cel) == 9:
        return cel[:9]
    else:
        print("invalid phone {}".format(x))
        sys.exit()


def create_email():
    char_set = string.ascii_lowercase + string.digits
    rand = ''.join(random.sample(char_set*7, 7))
    return f'one_{rand}@onebeleza.com.br'

def create_cel():
    return ''.join(random.sample(string.digits*11, 11))

def card_type(card):
    if ( re.search("credito", card, re.IGNORECASE) or
            re.search("^c$", card, re.IGNORECASE) ):
        return "C"
    elif ( re.search("debito", card, re.IGNORECASE) or
            re.search("^d$", card, re.IGNORECASE) ):
        return "D"
    else:
        print("unrecognized card type {}".format(card))
        sys.exit()

def get_bool(value):
    if value == True or value == False: return value

    if (string_normalize(value) == "sim" or
            string_normalize(value) == "s"):
        return True
    elif (string_normalize(value) == "nao" or
          string_normalize(value) == "n"):
        return False
    return None


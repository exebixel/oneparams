import unicodedata, re, sys
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

#encoding:utf8

from ply import lex

tokens = (
    'ENTITY',
    'SERIES',
)

# t_ENTITY = '[\u4e00-\u9fa5]+'
t_ENTITY = r"[\x80-\xff]+?"
t_SERIES = r'第\d'

lexer = lex.lex()

data = "精武门第2集"

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print tok


delimiter=r"\W?"

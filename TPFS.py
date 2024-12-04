import ply.lex as lex

reserved = {
    'actor': 'ACTOR',
    'usecase': 'USECASE',
    'package': 'PACKAGE',
    'as': 'AS',
    'includes': 'INCLUDES',
    'extends': 'EXTENDS',
}

tokens = [
    'AT_STARTUML',        
    'AT_ENDUML',          
    'COLON',
    'RIGHT_ARROW_1',
    'RIGHT_ARROW_2',
    'LBRACE',
    'RBRACE',
    'INHERIT',
    'EOL',
    'STRING',
    'STEREO',
    'ACTOR_TEXT',
    'USE_CASE_TEXT',
    'ID',
] + list(reserved.values())

t_AT_STARTUML = r'@startuml'
t_AT_ENDUML = r'@enduml'
t_COLON = r':'
t_RIGHT_ARROW_1 = r'--?>'
t_RIGHT_ARROW_2 = r'\.\.?>'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_INHERIT = r'<\|--'
t_STRING = r'"[^"]*"'
t_STEREO = r'<<[^>]*>>'
t_ACTOR_TEXT = r':[^\s:]+:'
t_USE_CASE_TEXT = r'\([^\)]+\)'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_EOL(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' a la ligne {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__":
    data = """
    @startuml System
      actor :User:
      usecase (Define travel)
      :User: --> (Define travel) : includes
    @enduml
    """
    lexer.input(data)
    for token in lexer:
        print(token)

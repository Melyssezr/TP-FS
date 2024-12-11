from ply import lex, yacc



# Déclaration des tokens
tokens = (
    "STARTUML", "ENDUML", "COLON", "RIGHT_ARROW_1", "RIGHT_ARROW_2", "ACTOR", "ID", "AS", 
    "USECASE", "STRING", "PACKAGE", "LBRACE", "RBRACE", "INHERIT", "STEREO", "INCLUDES", 
    "EXTENDS", "ACTOR_TXT", "USE_CASE_TXT", "EOL"
)

# Mots réservés
reserved = {
    "actor": "ACTOR",
    "as": "AS",
    "usecase": "USECASE",
    "package": "PACKAGE",
    "includes": "INCLUDES",
    "extends": "EXTENDS",
}

# Expressions régulières pour les tokens
t_STARTUML = r"@startuml"
t_ENDUML = r"@enduml"
t_COLON = r":"
t_RIGHT_ARROW_1 = r"-+>"
t_RIGHT_ARROW_2 = r"\.+>"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_INHERIT = r"<\|--"
t_EOL = r"\n"

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_STEREO(t):
    r"<<[a-zA-Z_][a-zA-Z_0-9]*>>"
    t.value = t.value[2:-2]
    return t

def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    if t.value in reserved.keys():
        t.type = reserved[t.value]
    return t

def t_ACTOR_TXT(t):
    r":[^ :\n][^\n:]*:"
    t.value = t.value[1:-1]
    return t

def t_USE_CASE_TXT(t):
    r"\([^ \(\n][^\n\)]*\)"
    t.value = t.value[1:-1]
    return t

# Ignorer les espaces et tabulations
t_ignore = " \t"

# Gestion des erreurs
def t_error(t):
    raise ValueError(f"Caractère inattendu : {t.value[0]} à la ligne {t.lineno}")

# Construction du lexer
lexer = lex.lex()



# def des regles syntaxiques
def p_start(p):
    """start : eols STARTUML name EOL defs ENDUML eols"""
    p[0] = {
        "type": "diagram",
        "name": p[3],
        "defs": p[5]
    }

def p_name(p):
    """name : ID
            | empty"""
    p[0] = p[1] if len(p) > 1 else None

def p_defs(p):
    """defs : one_def EOL
            | defs one_def EOL"""
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_one_def(p):
    """one_def : ACTOR def_act alias stereo
               | ACTOR_TXT alias stereo
               | USECASE def_uc alias stereo
               | USE_CASE_TXT alias stereo
               | var arrow var ucl_link
               | var INHERIT var
               | PACKAGE ID LBRACE defs RBRACE
               | empty"""
    if len(p) == 5:  #acteur ou cas dutilisation
        p[0] = {"type": "actor" if p[1] == "ACTOR" else "usecase", "name": p[2], "alias": p[3], "stereo": p[4]}
    elif len(p) == 7:  #package
        p[0] = {"type": "package", "name": p[2], "content": p[4]}
    elif len(p) == 4 and p[2] == "<|--":  #heritage
        p[0] = {"type": "inheritance", "parent": p[3], "child": p[1]}
    elif len(p) == 5:  #fleches
        p[0] = {"type": "link", "from": p[1], "to": p[3], "link": p[4]}
    else:
        p[0] = None  #vide

def p_def_act(p):
    """def_act : ID
               | ACTOR_TXT
               | STRING"""
    p[0] = p[1]

def p_def_uc(p):
    """def_uc : ID
              | USE_CASE_TXT
              | STRING"""
    p[0] = p[1]

def p_alias(p):
    """alias : AS ID
             | empty"""
    p[0] = p[2] if len(p) > 2 else None

def p_stereo(p):
    """stereo : STEREO
              | empty"""
    p[0] = p[1] if len(p) > 1 else None

def p_arrow(p):
    """arrow : RIGHT_ARROW_1
             | RIGHT_ARROW_2"""
    p[0] = p[1]

def p_ucl_link(p):
    """ucl_link : COLON EXTENDS
                | COLON INCLUDES
                | COLON ID
                | empty"""
    if len(p) > 1:
        p[0] = {"type": p[2], "link": p[3]} if len(p) == 4 else {"type": p[2]}

def p_var(p):
    """var : ID
           | USE_CASE_TXT
           | ACTOR_TXT"""
    p[0] = p[1]

def p_eols(p):
    """eols : EOL eols
            | empty"""
    p[0] = None

def p_empty(p):
    """empty :"""
    p[0] = None

#getsion des erreurs
def p_error(p):
    if p:
        raise SyntaxError(f"Erreur de syntaxe à la ligne {p.lineno} : {p.value}")
    else:
        raise SyntaxError("Erreur de syntaxe en fin de fichier.")

#construire le parser
parser = yacc.yacc()

#exemple de test
data = """@startuml
:Main Admin: as Admin <<Not-a-machine>>
(Use the application) as Use
User <|-- Admin
(Start) .> Use : extends
User .> Use
@enduml"""

lexer.input(data)
print("Tokens générés :")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

try:
    result = parser.parse(data)
    print("Arbre syntaxique abstrait :", result)
except SyntaxError as e:
    print(e)

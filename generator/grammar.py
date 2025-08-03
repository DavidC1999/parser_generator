from typing import List

class Type:
    STRING = 0
    NUMBER = 1

class TokenType:
    def __init__(self, name: str, value_type: str | None = None):
        self.name = name
        self.value_type = value_type

class Atom:
    def __init__(self, atom_type):
        self.atom_type = atom_type
    
    def is_token(self):
        return self.atom_type == "token"
    
    def is_repeat(self):
        return self.atom_type == "repeat"
    
    def is_noderef(self):
        return self.atom_type == "noderef"

class Field:
    def __init__(self, type: str, name: str):
        self.type = type
        self.name = name
    
class Token(Atom):
    def __init__(self, type: TokenType, binds_to: str | None = None):
        super().__init__("token")
        self.type = type
        self.binds_to = binds_to

noderegistrations = {}

class Node:
    def __init__(self, name: str, fields: List[Field], expression: List[Atom]):
        self.name = name
        self.fields = fields
        self.expression = expression

        noderegistrations[name] = self

class NodeReference(Atom):
    def __init__(self, name: str):
        super().__init__("noderef")
        self.name = name
    
    def get_node(self) -> Node:
        return noderegistrations[self.name]

class Repeat(Atom):
    def __init__(self, *atoms: List[Atom]):
        super().__init__("repeat")
        self.atoms = atoms

token_open_curly = TokenType("OPEN_CURLY")
token_close_curly = TokenType("CLOSE_CURLY")
token_comma = TokenType("COMMA")
token_colon = TokenType("COLON")
token_strlit = TokenType("STRLIT", "const char*")
token_intlit = TokenType("INTLIT", "int64_t")

grammar = [
    Node(
        name="object",
        fields = [],
        expression=[
           Token(token_open_curly),
           NodeReference("member"),
           Repeat(Token(token_comma), NodeReference("member")),
           Token(token_close_curly),
        ]
    ),
    Node(
        name="member",
        fields = [
           Field(name = "name", type = "const char*")
        ],
        expression = [
            Token(token_strlit, binds_to="name"),
            Token(token_colon),
            NodeReference("number")
        ]
    ),
    Node(
        name = "number",
        fields = [
            Field(name = "value", type = "int64_t")
        ],
        expression = [
            Token(token_intlit, binds_to="value")
        ]
    )
]
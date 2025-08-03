import sys
import os
from typing import List

print("Generating parser....")

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

parse_prototypes = ""
parse_functions = ""

def node_enum_name(node: Node):
    return f"NODE_{node.name.upper()}"

def parse_atom(indent_num:int, node: Node, atom: Atom):
    code = ""
    indent = " " * indent_num
    if atom.is_token():
        token: Token = atom
        code += f"{indent}expect_token(tokens, TOKEN_{token.type.name.upper()});\n"
        if token.binds_to != None:
            field = next(f for f in node.fields if f.name == token.binds_to)
            if (field.type.endswith("*")): # is pointer
                code += f"{indent}ret_val->{node.name}.{field.name} = ({field.type})current_token(tokens)->arg;\n"
            else:
                code += f"{indent}ret_val->{node.name}.{field.name} = *({field.type}*)current_token(tokens)->arg;\n"
        code += f"{indent}consume_token(tokens);\n"
    elif atom.is_noderef():
        referenced_node = atom.get_node()
        code += f"{indent}linked_list_append(&ret_val->{node.name}.children, parse_{referenced_node.name}(arena, tokens));\n"
    elif atom.is_repeat():
        if not atom.atoms[0].is_token():
            raise "First atom of repeat atom must be a token (for now)"
        token = atom.atoms[0]
        code += f"{indent}while (current_token(tokens)->id == TOKEN_{token.type.name.upper()}) {{\n"
        for repeated_atom in atom.atoms:
            code += parse_atom(indent_num + 4, node, repeated_atom)
        code += f"{indent}}}\n"
        
    return code


def generate_parse_method(node: Node):
    global parse_prototypes
    global parse_functions

    parse_prototypes += f"node* parse_{node.name}(memory_arena* arena, linked_list* tokens);\n"

    code =  f"node* parse_{node.name}(memory_arena* arena, linked_list* tokens) {{\n"
    code +=  "    node* ret_val = arena_alloc(arena, sizeof(node));\n"
    code += f"    ret_val->id = {node_enum_name(node)};\n"
    code += f"    linked_list_clear(&ret_val->{node.name}.children);\n"

    for atom in node.expression:
        code += parse_atom(4, node, atom)
        
    code += "    return ret_val;\n"
    code += "}\n\n"
    
    parse_functions += code


enum = "typedef enum {\n"

struct = """typedef struct node {
    struct node* next;
    node_id id;
    
    union {\n"""

for node in grammar:
    enum += f"    {node_enum_name(node)},\n"

    struct += "        struct {\n"
    for field in node.fields:
        struct += f"            {field.type} {field.name};\n"
    
    struct += f"            linked_list children;\n"
    struct += f"        }} {node.name};\n\n"

    generate_parse_method(node)


enum += "} node_id;\n"

struct += "    };\n"
struct += "} node;\n"

template_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = sys.argv[1]

with open(f"{template_dir}/template.c", "r") as f:
    template_c = f.read()

template_c = template_c.replace("[functions]", parse_functions)

with open(f"{output_dir}/parser.c", "w") as f:
    f.write(template_c)

with open(f"{template_dir}/template.h", "r") as f:
    template_h = f.read()

template_h = template_h.replace("[enum]", enum)
template_h = template_h.replace("[struct]", struct)
template_h = template_h.replace("[prototypes]", parse_prototypes)

with open(f"{output_dir}/parser.h", "w") as f:
    f.write(template_h)
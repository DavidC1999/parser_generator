import sys
import os
from typing import List

print("-------------------------------")
print("-------------------------------")
print("My awesome code generator")
print("-------------------------------")
print("-------------------------------")

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
    
    def children(self):
        return filter(lambda a: a.is_noderef(), self.expression)

    def child_count(self):
        return sum(type(e) == NodeReference for e in node.expression)

class NodeReference(Atom):
    def __init__(self, name: str):
        super().__init__("noderef")
        self.name = name
    
    def get_node(self) -> Node:
        return noderegistrations[self.name]

token_open_curly = TokenType("OPEN_CURLY")
token_close_curly = TokenType("CLOSE_CURLY")
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

def generate_parse_method(node: Node):
    global parse_prototypes
    global parse_functions

    parse_prototypes += f"node* parse_{node.name}(memory_arena* arena, token_list* tokens);\n"

    code =  f"node* parse_{node.name}(memory_arena* arena, token_list* tokens) {{\n"
    code +=  "    node* ret_val = arena_alloc(arena, sizeof(node));\n"
    code += f"    ret_val->id = {node_enum_name(node)};\n"

    child_counter = 0

    for atom in node.expression:
        if atom.is_token():
            token: Token = atom
            code += f"    expect_token(tokens, TOKEN_{token.type.name.upper()});\n"
            if token.binds_to != None:
                field = next(f for f in node.fields if f.name == token.binds_to)
                if (field.type.endswith("*")): # is pointer
                    code += f"    ret_val->{node.name}.{field.name} = ({field.type})tokens->it->arg;\n"
                else:
                    code += f"    ret_val->{node.name}.{field.name} = *({field.type}*)tokens->it->arg;\n"
            code += "    consume_token(tokens);\n"
        elif atom.is_noderef():
            referenced_node = atom.get_node()
            code += f"    ret_val->{node.name}.children[{child_counter}] = parse_{referenced_node.name}(arena, tokens);\n"
            child_counter += 1
        
    code += "    return ret_val;\n"
    code += "}\n\n"
    
    parse_functions += code


enum = "typedef enum {\n"

struct = """typedef struct node {
    node_id id;
    
    union {\n"""

for node in grammar:
    enum += f"    {node_enum_name(node)},\n"

    struct += "        struct {\n"
    for field in node.fields:
        struct += f"            {field.type} {field.name};\n"
    
    if (node.child_count() > 0):
        struct += f"            struct node* children[{node.child_count()}];\n"
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
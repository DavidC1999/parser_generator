from grammar import *
from name_generators import *

def parse_atom(indent_num:int, node: Node, atom: Atom):
    code = ""
    indent = " " * indent_num
    if atom.is_token():
        token: Token = atom
        code += f"{indent}expect_token(tokens, {token_enum_name(token)});\n"
        if token.binds_to != None:
            field = next(f for f in node.fields if f.name == token.binds_to)
            if (field.type.endswith("*")): # is pointer
                code += f"{indent}ret_val->{node.name}.{field.name} = ({field.type})current_token(tokens)->arg;\n"
            else:
                code += f"{indent}ret_val->{node.name}.{field.name} = *({field.type}*)current_token(tokens)->arg;\n"
        code += f"{indent}consume_token(tokens);\n"
    elif atom.is_noderef():
        referenced_node = atom.get_node()
        code += f"{indent}linked_list_append(&children, (list_item*)parse_{referenced_node.name}(arena, tokens));\n"
    elif atom.is_repeat():
        if not atom.atoms[0].is_token():
            raise "First atom of repeat atom must be a token (for now)"
        token = atom.atoms[0]
        code += f"{indent}while (current_token(tokens)->id == {token_enum_name(token)}) {{\n"
        for repeated_atom in atom.atoms:
            code += parse_atom(indent_num + 4, node, repeated_atom)
        code += f"{indent}}}\n"
        
    return code


def generate_parse_function(node: Node):
    code = ""

    code =  f"node* parse_{node.name}(memory_arena* arena, linked_list* tokens) {{\n"
    code +=  "    node* ret_val = arena_alloc(arena, sizeof(node));\n"
    code += f"    ret_val->id = {node_enum_name(node)};\n"
    code += f"    linked_list children;\n"
    code += f"    linked_list_clear(&children);\n"

    for atom in node.expression:
        code += parse_atom(4, node, atom)
    
    code += f"    ret_val->{node.name}.children = (node*)children.head;\n"
        
    code += "    return ret_val;\n"
    code += "}\n\n"
    
    return code